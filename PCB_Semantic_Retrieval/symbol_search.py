#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hybrid symbol search over JSONL produced by the KiCad symbol extractor.

Indexes:
  1) ANN (HNSW) over text embeddings of `text_flat`
  2) SQLite FTS5 (BM25) over lib_id, name, description, pins_text
  3) Pin-token inverted index from `pin_tokens`

Query:
  input: user natural-language request (e.g., "LED driven by 3.3V")
  output: list[str] of "lib_id:symbol_name"

Usage (build):
  python symbol_search.py build --input_jsonl symbol_index.jsonl --index_dir .cache_symbol_index

Usage (query):
  python symbol_search.py query --index_dir .cache_symbol_index --topk 20 \
      --q "I want a LED driven by 3.3V"

Requires:
  pip install hnswlib sentence-transformers
  (SQLite FTS5 is built-in on most platforms)
"""

import os
import sys
import json
import argparse
import sqlite3
import pickle
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Iterable

project_path = os.environ.get("PROJECT_PATH")
sys.path.append(project_path)

import numpy as np

# ===== Optional: choose your embedder =====
# Default: sentence-transformers MiniLM (fast, good)
try:
    from sentence_transformers import SentenceTransformer
    _EMBEDDER = SentenceTransformer('all-MiniLM-L6-v2')
    def embed_texts(texts: List[str]) -> np.ndarray:
        return np.array(_EMBEDDER.encode(texts, normalize_embeddings=True), dtype=np.float32)
except Exception:
    # Fallback: trivial hashing embedding (works but poor quality). Replace in production.
    import hashlib
    def _hash_vec(s: str, dim: int = 384) -> np.ndarray:
        rnd = np.random.RandomState(int(hashlib.md5(s.encode('utf-8')).hexdigest()[:8], 16))
        v = rnd.randn(dim).astype(np.float32)
        v /= np.linalg.norm(v) + 1e-12
        return v
    def embed_texts(texts: List[str]) -> np.ndarray:
        return np.stack([_hash_vec(t) for t in texts], axis=0)

import hnswlib  # ANN


PRIMARY_SEP = ":"  # join lib_id and symbol name


def primary_key(lib_id: str, name: str) -> str:
    return f"{lib_id}{PRIMARY_SEP}{name}"


def split_primary(pk: str) -> Tuple[str, str]:
    lib_id, name = pk.split(PRIMARY_SEP, 1)
    return lib_id, name


# -------- Pin aliasing & query parsing --------

PIN_ALIASES = {
    # power
    "vcc": "vdd", "vss": "gnd", "avcc": "vdd", "dvcc": "vdd", "agnd": "gnd", "dgnd": "gnd",
    "3v3": "vdd", "3.3v": "vdd", "5v": "vdd", "1v8": "vdd", "1.8v": "vdd",
    # serial busses
    "scl": "i2c", "sda": "i2c", "usart": "uart", "tx": "uart", "rx": "uart",
    "sclk": "spi", "sck": "spi", "mosi": "spi", "miso": "spi", "cs": "spi", "ssel": "spi",
    # ethernet
    "rmii": "ethernet", "mii": "ethernet", "phy": "ethernet", "mac": "ethernet",
    # generic
    "vin": "vdd", "vbat": "vdd",
}

SPLIT_RE = re.compile(r"[^a-z0-9]+")

def normalize_tokens(s: str) -> List[str]:
    toks = [t for t in SPLIT_RE.split(s.lower()) if t]
    return [PIN_ALIASES.get(t, t) for t in toks]

# Map some common user phrases to pin intents
QUERY_HINTS = {
    "ethernet": {"ethernet", "rmii", "mii"},
    "rmii": {"ethernet", "rmii"},
    "mii": {"ethernet", "mii"},
    "i2c": {"i2c"},
    "uart": {"uart"},
    "spi": {"spi"},
    "usb": {"usb"},
    "gpio": {"gpio"},
    "pwm": {"pwm"},
    "adc": {"adc"},
    "dac": {"dac"},
    "power": {"vdd", "gnd"},
    "3.3v": {"vdd"}, "3v3": {"vdd"},
    "5v": {"vdd"},
    "led": {"led"},      # heuristic tag; present if your pin_tokens include 'led'
    "sensor": {"sensor"},
    "module": {"module"},
}

def parse_query(query: str) -> Tuple[List[str], List[str]]:
    """
    Returns:
      lexical_terms: tokens for FTS
      pin_intents:   canonical pin-like intents
    """
    toks = normalize_tokens(query)
    lexical = toks[:]  # for FTS

    pin_intents = set()
    # heuristic: add intents from hints
    for k, intents in QUERY_HINTS.items():
        if k in toks:
            pin_intents |= intents

    # also treat power voltages in free text (e.g., "3.3v", "5v")
    for t in toks:
        if t in {"3v3", "3", "33v", "3.3v"}:
            pin_intents.add("vdd")
        if t in {"5v", "5"}:
            pin_intents.add("vdd")

    return lexical, sorted(pin_intents)


# --------- Index builder ----------

class IndexBuilder:
    def __init__(self, index_dir: Path):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.sqlite_path = self.index_dir / "fts.db"
        self.hnsw_path = self.index_dir / "ann_hnsw.bin"
        self.meta_path = self.index_dir / "meta.pkl"
        self.pin_postings_path = self.index_dir / "pin_postings.pkl"

    def _open_db(self):
        con = sqlite3.connect(self.sqlite_path)
        con.execute("PRAGMA journal_mode=WAL;")
        con.execute("PRAGMA synchronous=OFF;")
        # Create FTS table if not exist
        con.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS symbols_fts
            USING fts5(primary_key UNINDEXED, lib_id, name, description, pins_text);
        """)
        return con

    def build(self, jsonl_path: Path):
        # Load JSONL
        rows = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                o = json.loads(line)
                # expect fields: o["record"], o["text_flat"], o["pin_tokens"]
                r = o["record"]
                pk = primary_key(r["lib_id"], r["name"])
                pins_text = " ".join([p["name"] for p in r.get("pins", []) if p.get("name")])
                rows.append({
                    "pk": pk,
                    "lib_id": r["lib_id"],
                    "name": r["name"],
                    "description": r.get("description", "") or "",
                    "text_flat": o.get("text_flat", "") or "",
                    "pins_text": pins_text,
                    "pin_tokens": o.get("pin_tokens", []) or [],
                })

        if not rows:
            print("No rows loaded; abort.", file=sys.stderr)
            return

        # --------- Build ANN ---------
        texts = [row["text_flat"] for row in rows]
        vecs = embed_texts(texts).astype(np.float32)
        dim = vecs.shape[1]
        p = hnswlib.Index(space='cosine', dim=dim)
        p.init_index(max_elements=len(rows), ef_construction=200, M=32)
        p.add_items(vecs, ids=np.arange(len(rows), dtype=np.int64))
        p.set_ef(256)

        p.save_index(str(self.hnsw_path))

        # --------- Build FTS ---------
        con = self._open_db()
        with con:
            con.execute("DELETE FROM symbols_fts;")
            con.executemany(
                "INSERT INTO symbols_fts (primary_key, lib_id, name, description, pins_text) VALUES (?,?,?,?,?)",
                [(r["pk"], r["lib_id"], r["name"], r["description"], r["pins_text"]) for r in rows]
            )
        con.close()

        # --------- Build pin postings ---------
        # token -> sorted list of integer ids (row indices)
        token_to_ids: Dict[str, List[int]] = {}
        for idx, row in enumerate(rows):
            tokens = set(row["pin_tokens"])  # unique
            for t in tokens:
                token_to_ids.setdefault(t, []).append(idx)
        for t in token_to_ids:
            token_to_ids[t].sort()

        # --------- Save meta ---------
        meta = {
            "rows": [{"pk": r["pk"]} for r in rows],  # keep pk + index position mapping
        }
        with open(self.meta_path, "wb") as f:
            pickle.dump(meta, f)
        with open(self.pin_postings_path, "wb") as f:
            pickle.dump(token_to_ids, f)

        print(f"Built ANN({len(rows)}), FTS, and {len(token_to_ids)} pin-token postings into {self.index_dir}")


# --------- Searcher ----------

class SymbolSearcher:
    def __init__(self, index_dir: Path):
        self.index_dir = Path(index_dir)
        self.sqlite_path = self.index_dir / "fts.db"
        self.hnsw_path = self.index_dir / "ann_hnsw.bin"
        self.meta_path = self.index_dir / "meta.pkl"
        self.pin_postings_path = self.index_dir / "pin_postings.pkl"

        # load meta
        with open(self.meta_path, "rb") as f:
            self.meta = pickle.load(f)
        self.pk_by_idx = [row["pk"] for row in self.meta["rows"]]

        # load ANN
        # infer dim from embedder (or a tiny probe)
        test_vec = embed_texts(["probe"]).astype(np.float32)
        dim = int(test_vec.shape[1])
        self.ann = hnswlib.Index(space='cosine', dim=dim)
        self.ann.load_index(str(self.hnsw_path))
        self.ann.set_ef(256)

        # open FTS
        self.con = sqlite3.connect(self.sqlite_path)
        self.con.execute("PRAGMA query_only=ON;")

        # pin postings
        with open(self.pin_postings_path, "rb") as f:
            self.pin_postings: Dict[str, List[int]] = pickle.load(f)

    def _fts_candidates(self, terms: List[str], k: int = 200) -> List[int]:
        if not terms:
            return []
        q = " ".join(terms)
        cur = self.con.cursor()
        # Return primary_keys and map to ann indices by lookup table
        cur.execute(
            "SELECT primary_key FROM symbols_fts WHERE symbols_fts MATCH ? LIMIT ?",
            (q, k)
        )
        pks = [row[0] for row in cur.fetchall()]
        # map pk -> ann index
        idxs = []
        # O(n) map is fine if we precompute a dict:
        self._pk_to_idx = getattr(self, "_pk_to_idx", None)
        if self._pk_to_idx is None:
            self._pk_to_idx = {pk: i for i, pk in enumerate(self.pk_by_idx)}
        for pk in pks:
            i = self._pk_to_idx.get(pk)
            if i is not None:
                idxs.append(i)
        return idxs

    def _ann_candidates(self, query: str, k: int = 200) -> List[int]:
        qv = embed_texts([query]).astype(np.float32)
        labels, _ = self.ann.knn_query(qv, k=k)
        return list(map(int, labels[0]))

    def _pin_candidates(self, pin_intents: List[str]) -> List[int]:
        if not pin_intents:
            return []
        sets = []
        for t in pin_intents:
            hit = self.pin_postings.get(t, [])
            if hit:
                sets.append(set(hit))
        if not sets:
            return []
        # strict AND; caller may relax later
        s = sets[0]
        for z in sets[1:]:
            s = s & z
        return sorted(s)

    @staticmethod
    def _cosine(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))

    def search(self, query: str, topk: int = 20,
               ann_k: int = 200, fts_k: int = 200,
               w_sem: float = 0.45, w_fts: float = 0.25,
               w_pin: float = 0.25, w_exact: float = 0.05) -> List[str]:

        lexical_terms, pin_intents = parse_query(query)

        # Candidates from each index
        cand_ann = set(self._ann_candidates(query, k=ann_k))
        cand_fts = set(self._fts_candidates(lexical_terms, k=fts_k))
        cand_pin = set(self._pin_candidates(pin_intents))

        C = cand_ann | cand_fts | cand_pin
        if not C:
            return []

        # Precompute query vector for semantic score
        qv = embed_texts([query]).astype(np.float32)[0]

        # Optional exact-boost tokens (substring in pk)
        exact_terms = set(t for t in lexical_terms if len(t) >= 3)

        # For a lightweight BM25 proxy, reuse FTS hit presence as 0/1
        fts_set = cand_fts

        # Compute pin coverage weight per candidate (0..1)
        def pin_coverage(idx: int) -> float:
            if not pin_intents:
                return 0.0
            cov = 0
            # we only stored postings, so coverage==1 if in AND set; else estimate via relaxed hits
            if idx in cand_pin:
                return 1.0
            # relaxed: count how many intents include this idx
            hits = 0
            for t in pin_intents:
                lst = self.pin_postings.get(t, [])
                # binary search would be better; set() also fine here
                if idx in set(lst):
                    hits += 1
            return hits / max(1, len(pin_intents))

        ranked = []
        # For semantic score, approximate by re-embedding pk (cheap) or reusing ann internal? We'll embed pk text for speed.
        # Better: cache vectors in meta next time. Here: embed primary key text as proxy (quick).
        for idx in C:
            pk = self.pk_by_idx[idx]

            # semantic similarity via re-embed of pk (fast) + small boost; or skip and assign proxy by ann membership
            # A better approach: persist item vectors at build time; we omitted to keep meta small.
            # We'll approximate: if from ANN, give base sem score 0.8..1.0 range ranking by proximity using another query.
            # Simpler: compute cosine between query vector and the item vector via ann.get_items([idx]) is not exposed.
            # So do a quick text embedding of pk (acceptable).
            item_vec = embed_texts([pk]).astype(np.float32)[0]
            vscore = self._cosine(qv, item_vec)

            fscore = 1.0 if idx in fts_set else 0.0
            pscore = pin_coverage(idx)
            escore = 0.0
            if exact_terms:
                key_lc = pk.lower()
                escore = 1.0 if any(t in key_lc for t in exact_terms) else 0.0

            score = w_sem * vscore + w_fts * fscore + w_pin * pscore + w_exact * escore
            ranked.append((score, idx))

        ranked.sort(key=lambda x: x[0], reverse=True)

        # De-duplicate by primary key, return lib_id:symbol_name
        out = []
        seen = set()
        for _, idx in ranked:
            pk = self.pk_by_idx[idx]
            if pk not in seen:
                seen.add(pk)
                out.append(pk)
            if len(out) >= topk:
                break
        return out


# --------- CLI ----------

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="Build indexes from JSONL")
    b.add_argument("--input_jsonl", required=True, type=Path)
    b.add_argument("--index_dir", required=True, type=Path)

    q = sub.add_parser("query", help="Query indexes")
    q.add_argument("--index_dir", required=True, type=Path)
    q.add_argument("--q", required=True, type=str)
    q.add_argument("--topk", type=int, default=20)

    args = ap.parse_args()

    if args.cmd == "build":
        IndexBuilder(args.index_dir).build(args.input_jsonl)
    elif args.cmd == "query":
        searcher = SymbolSearcher(args.index_dir)
        results = searcher.search(args.q, topk=args.topk)
        for r in results:
            print(r)
    else:
        ap.print_help()

if __name__ == "__main__":
    main()