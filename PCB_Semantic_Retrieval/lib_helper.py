'''
Helper classes for building and querying the global hybrid index.
'''
import os,sys
project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)


import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
import re

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors

from PCB_Semantic_Retrieval.symbol_extension import ExtendedSymbols


def make_primary_key(lib_id: str, name: str) -> str:
    """Create a stable key 'lib_id:name'."""
    return f"{lib_id}:{name}"



class GlobalHybridIndex:
    """
    Hybrid index over the *full* symbol library.

    - SQLite FTS5 table for lexical search on detailed_description
    - ANN index (embeddings) for semantic search
    """

    def __init__(
        self,
        symbol_lib_jsonl: str,
        sqlite_path: str,
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        """
        Args:
            symbol_lib_jsonl (str): Path to symbol_lib.jsonl (with detailed_description).
            sqlite_path (str): Path to the SQLite DB for FTS5.
            embedding_model_name (str): SentenceTransformer model name.
        """
        self.symbol_lib_jsonl = Path(symbol_lib_jsonl)
        self.sqlite_path = Path(sqlite_path)
        self.embedding_model = SentenceTransformer(embedding_model_name)

        # Will be filled in build()
        self.pk_list: List[str] = []        # index -> 'lib_id:name'
        self.lib_ids: List[str] = []        # index -> lib_id
        self.names: List[str] = []          # index -> symbol_name
        self.embeddings: np.ndarray | None = None
        self.ann_index: NearestNeighbors | None = None

    # ---------- FTS helpers ----------

    def _open_db(self) -> sqlite3.Connection:
        """Open or create SQLite DB with FTS5 table."""
        con = sqlite3.connect(self.sqlite_path)
        con.execute("PRAGMA journal_mode=WAL;")
        con.execute("PRAGMA synchronous=OFF;")
        con.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS detailed_fts
            USING fts5(
                primary_key UNINDEXED,
                lib_id,
                name,
                detailed_text
            );
            """
        )
        return con

    @staticmethod
    def _build_detailed_text(detailed: dict) -> str:
        """Concatenate all values from detailed_description dict."""
        if not isinstance(detailed, dict):
            return ""
        parts = []
        for v in detailed.values():
            if v is None:
                continue
            parts.append(str(v))
        return " ".join(parts)

    # ---------- main build ----------

    def build(self) -> None:
        """
        Build FTS and embedding index from symbol_lib.jsonl.
        Should be called once at startup.
        """
        con = self._open_db()
        cursor = con.cursor()
        cursor.execute("DELETE FROM detailed_fts;")

        texts: List[str] = []
        pk_list: List[str] = []
        lib_ids: List[str] = []
        names: List[str] = []

        with self.symbol_lib_jsonl.open("r", encoding="utf-8") as fin:
            for line in fin:
                line = line.strip()
                if not line:
                    continue

                obj = json.loads(line)
                rec = obj.get("record") or {}
                lib_id = rec.get("lib_id")
                name = rec.get("name")

                if not lib_id or not name:
                    continue

                pk = make_primary_key(lib_id, name)
                detailed = obj.get("detailed_description") or {}
                detailed_text = self._build_detailed_text(detailed)

                cursor.execute(
                    """
                    INSERT INTO detailed_fts (primary_key, lib_id, name, detailed_text)
                    VALUES (?, ?, ?, ?)
                    """,
                    (pk, lib_id, name, detailed_text),
                )

                pk_list.append(pk)
                lib_ids.append(lib_id)
                names.append(name)
                texts.append(detailed_text)

        con.commit()
        con.close()

        if not texts:
            raise RuntimeError("No valid entries found in symbol_lib_jsonl.")

        # Encode all texts into embeddings
        embeddings = self.embedding_model.encode(
            texts,
            batch_size=64,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,  # cos-sim == dot product
        )

        self.pk_list = pk_list
        self.lib_ids = lib_ids
        self.names = names
        self.embeddings = embeddings

        # Build ANN index (here: exact kNN; can later switch to faiss/hnswlib)
        index = NearestNeighbors(
            n_neighbors=min(50, len(embeddings)),
            metric="cosine",
            algorithm="auto",
        )
        index.fit(embeddings)
        self.ann_index = index

        print(f"[GlobalHybridIndex] Built with {len(self.pk_list)} entries.")

def min_max_normalize(values: Dict[str, float]) -> Dict[str, float]:
    """
    Min-max normalize a dict of scores.

    If all scores are equal, returns 0.5 for all keys.
    """
    if not values:
        return values
    scores = list(values.values())
    v_min = min(scores)
    v_max = max(scores)
    if v_max <= v_min:
        return {k: 0.5 for k in values}
    return {k: (v - v_min) / (v_max - v_min) for k, v in values.items()}

def build_query_from_extended_symbol(sym: ExtendedSymbols) -> str:
    """
    Build a search query string from one ExtendedSymbols object.

    We concatenate the different semantic fields to form a rich query.
    """
    parts = [
        sym.name,
        sym.footprint or "",
        sym.technical_specification or "",
        sym.function or "",
        sym.potential_application or "",
    ]
    # Filter out empty strings and join
    parts = [p for p in parts if p]
    return " ".join(parts)

class GlobalHybridSearcher:
    """
    Perform hybrid FTS + ANN search on the global library.
    """

    def __init__(
        self,
        index: GlobalHybridIndex,
        alpha: float = 0.5,
        fts_topn: int = 100,
        ann_topn: int = 100,
    ):
        """
        Args:
            index (GlobalHybridIndex): Already built hybrid index.
            alpha (float): Weight for lexical score in [0,1].
            fts_topn (int): Top N from FTS stage.
            ann_topn (int): Top N from ANN stage.
        """
        self.index = index
        self.alpha = alpha
        self.fts_topn = fts_topn
        self.ann_topn = ann_topn

        # Build the GlobalHybridIndex if not already built
        if not self.index.pk_list or self.index.embeddings is None:
            print("[GlobalHybridSearcher] Building index...")
            self.index.build()

    # ---- FTS search ----
    def fts_query_sanitize(self, q: str) -> str:

        # Only keep alphanumeric and underscore for FTS query, to avoid syntax issues.

        terms = re.findall(r"[A-Za-z0-9_]+", q)

        return " ".join(terms)

    def _fts_search(self, query: str) -> Dict[str, float]:
        """
        Run FTS query and return mapping primary_key -> lexical score.

        Uses FTS5 bm25(), which returns "lower is better", so we invert it.
        """

        query = self.fts_query_sanitize(query)
        con = sqlite3.connect(self.index.sqlite_path)
        cur = con.cursor()
        cur.execute(
            """
            SELECT primary_key, bm25(symbols_fts) AS rank
            FROM symbols_fts
            WHERE symbols_fts MATCH ?
            LIMIT ?;
            """,
            (query, self.fts_topn),
        )
        rows = cur.fetchall()
        con.close()

        scores: Dict[str, float] = {}
        for pk, bm25_score in rows:
            if bm25_score is None:
                continue
            score = 1.0 / (1.0 + bm25_score)  # invert: higher is better
            scores[pk] = score
        return scores

    # ---- ANN search ----

    def _ann_search(self, query: str) -> Dict[str, float]:
        """
        Run ANN search and return mapping primary_key -> similarity score.
        """
        if self.index.embeddings is None or self.index.ann_index is None:
            raise RuntimeError("GlobalHybridIndex has not been built properly.")

        # Encode query to embedding
        q_vec = self.index.embedding_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]

        distances, indices = self.index.ann_index.kneighbors(
            q_vec.reshape(1, -1),
            n_neighbors=min(self.ann_topn, len(self.index.embeddings)),
            return_distance=True,
        )
        distances = distances[0]
        indices = indices[0]

        scores: Dict[str, float] = {}
        for idx, dist in zip(indices, distances):
            sim = 1.0 - float(dist)  # cosine distance -> similarity
            pk = self.index.pk_list[int(idx)]
            scores[pk] = sim
        return scores

    # ---- Combined search ----

    def search(self, query: str, topk: int = 20) -> List[str]:
        """
        Perform hybrid search and return list of 'lib_id:symbol_name'.

        Args:
            query (str): The textual query.
            topk (int): Number of final results to return.

        Returns:
            List[str]: pk strings in the form 'lib_id:symbol_name'.
        """
        query = query.strip()
        if not query:
            return []

        fts_raw = self._fts_search(query)  # pk -> score
        ann_raw = self._ann_search(query)  # pk -> score

        fts_norm = min_max_normalize(fts_raw)
        ann_norm = min_max_normalize(ann_raw)

        all_pks = set(fts_norm.keys()) | set(ann_norm.keys())
        if not all_pks:
            return []

        final_scores: List[Tuple[str, float]] = []
        for pk in all_pks:
            lex = fts_norm.get(pk, 0.0)
            ann = ann_norm.get(pk, 0.0)
            score = self.alpha * lex + (1.0 - self.alpha) * ann
            final_scores.append((pk, score))

        final_scores.sort(key=lambda x: x[1], reverse=True)
        final_scores = final_scores[:topk]
        return [pk for pk, _ in final_scores]