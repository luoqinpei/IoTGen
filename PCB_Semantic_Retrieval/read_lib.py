#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build minimal symbol records from KiCad .kicad_sym files and derive:
- record: {lib_id, name, description, pins:[{name,type}]}
- text_flat: "lib_id name description pin_names..."
- pin_tokens: normalized tokens derived from pin names/types

Usage:
  python build_symbol_index.py
"""
import os, sys
project_path = os.environ.get("PROJECT_PATH")
sys.path.append(project_path)

from config import KICAD_SYMBOL_LIB_PATH, KICAD_FOOTPRINT_LIB_PATH

import json
import re
from pathlib import Path
from typing import List, Tuple, Any, Dict, Iterable, Union


OUT_JSONL = Path(project_path) / "PCB_Semantic_Retrieval" / "symbol_index.jsonl"
OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)

# --------------------
# S-expression parser
# --------------------
# Minimal, KiCad-friendly: handles (), atoms, quoted strings with escapes.

_TOKEN_RE = re.compile(
    r'''\s*(?:
        (?P<lpar>\()|
        (?P<rpar>\))|
        (?P<str>"([^"\\]|\\.)*")|
        (?P<atom>[^()\s"]+)
    )''',
    re.VERBOSE | re.DOTALL,
)

def _unescape_qstring(q: str) -> str:
    # q includes the surrounding quotes
    s = q[1:-1]
    # KiCad uses typical escapes for quotes/backslashes; keep it simple:
    return bytes(s, "utf-8").decode("unicode_escape")

def tokenize(s: str) -> Iterable[Tuple[str, str]]:
    for m in _TOKEN_RE.finditer(s):
        kind = m.lastgroup
        yield kind, m.group(kind)

def parse_sexpr(s: str) -> Any:
    tokens = list(tokenize(s))
    pos = 0

    def parse_list() -> List[Any]:
        nonlocal pos
        assert tokens[pos][0] == "lpar"
        pos += 1
        lst = []
        while pos < len(tokens) and tokens[pos][0] != "rpar":
            lst.append(parse_any())
        if pos >= len(tokens) or tokens[pos][0] != "rpar":
            raise ValueError("Unbalanced parentheses while parsing.")
        pos += 1
        return lst

    def parse_any() -> Any:
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("Unexpected end of tokens.")
        kind, val = tokens[pos]
        if kind == "lpar":
            return parse_list()
        elif kind == "rpar":
            raise ValueError("Unexpected ')'")
        elif kind == "str":
            pos += 1
            return _unescape_qstring(val)
        elif kind == "atom":
            pos += 1
            return val
        else:
            pos += 1
            return val

    ast = []
    while pos < len(tokens):
        ast.append(parse_any())
    return ast

# --------------------
# Helpers
# --------------------

def to_str(x: Any) -> str:
    if isinstance(x, str):
        return x
    return str(x)

def is_list(x: Any) -> bool:
    return isinstance(x, list)

def walk_nodes(node: Any) -> Iterable[Any]:
    """Yield all list nodes in the s-expression tree."""
    if is_list(node):
        yield node
        for el in node:
            yield from walk_nodes(el)

def find_top_level_symbols(ast: List[Any]) -> List[List[Any]]:
    """
    In a .kicad_sym file, top-level is usually:
      (kicad_symbol_lib ... (symbol "NAME" ...) (symbol "NAME2" ...))
    Return the list nodes that begin with 'symbol' at top-level depth=1..2.
    """
    # The root may be a flat list; locate `(kicad_symbol_lib ...)`
    tops = []
    for n in ast:
        if is_list(n) and len(n) >= 1 and n[0] == "kicad_symbol_lib":
            # symbols are children inside this node
            for child in n[1:]:
                if is_list(child) and len(child) >= 2 and child[0] == "symbol" and isinstance(child[1], str):
                    tops.append(child)
    # Fallback: sometimes files are flattened; still try to catch top-level 'symbol'
    if not tops:
        for n in ast:
            if is_list(n) and len(n) >= 2 and n[0] == "symbol" and isinstance(n[1], str):
                tops.append(n)
    return tops

def extract_description(sym_node: List[Any]) -> str:
    """
    Inside the symbol node, find (property "Description" "....")
    Return empty string if not found.
    """
    desc = ""
    for node in walk_nodes(sym_node):
        if is_list(node) and len(node) >= 3 and node[0] == "property":
            key = to_str(node[1])
            if key == "Description" and isinstance(node[2], str):
                desc = node[2]
                break
    return desc

def extract_pins(sym_node: List[Any]) -> List[Dict[str, str]]:
    """
    Collect pins by scanning for nodes like:
      (pin <type> line (at ...) (length ...) (name "XXX" ...) (number "N" ...))
    If pin name == "~", replace it with pin number.
    If still unnamed, assign sequential number starting from 1.
    """
    pins = []
    seq_counter = 1
    for node in walk_nodes(sym_node):
        if is_list(node) and len(node) >= 2 and node[0] == "pin":
            ptype = to_str(node[1]) if len(node) > 1 else ""
            pname = ""
            pnum = ""
            for sub in node:
                if is_list(sub) and len(sub) >= 2 and sub[0] == "name" and isinstance(sub[1], str):
                    pname = sub[1]
                if is_list(sub) and len(sub) >= 2 and sub[0] == "number" and isinstance(sub[1], str):
                    pnum = sub[1]

            # --- new behavior ---
            if pname == "~" or not pname:
                if pnum:
                    pname = pnum
                else:
                    pname = str(seq_counter)
                    seq_counter += 1
            # ---------------------

            pins.append({"name": pname, "type": ptype})
    return pins

_SPLIT_RE = re.compile(r"[^a-z0-9]+")

PIN_ALIASES = {
    # simple, useful normalizations
    "vcc": "vdd",
    "vss": "gnd",
    "avcc": "vdd",
    "dvcc": "vdd",
    "agnd": "gnd",
    "dgnd": "gnd",
    "3v3": "vdd",
    "5v": "vdd",
    # interface hints
    "tx": "uart",
    "rx": "uart",
    "scl": "i2c",
    "sda": "i2c",
    "miso": "spi",
    "mosi": "spi",
    "sclk": "spi",
    "sck": "spi",
    "cs": "spi",
    "rmii": "ethernet",
    "mii": "ethernet",
}

def normalize_tokens(s: str) -> List[str]:
    toks = [t for t in _SPLIT_RE.split(s.lower()) if t]
    return toks

def canonicalize_pin_token(tok: str) -> str:
    return PIN_ALIASES.get(tok, tok)

def derive_pin_tokens(pins: List[Dict[str, str]]) -> List[str]:
    toks = []
    for p in pins:
        for raw in (p.get("name",""), p.get("type","")):
            for t in normalize_tokens(raw):
                toks.append(canonicalize_pin_token(t))
    # uniq while preserving order
    seen = set()
    out = []
    for t in toks:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out

def derive_text_flat(lib_id: str, name: str, description: str, pins: List[Dict[str, str]]) -> str:
    pin_names = " ".join(p["name"] for p in pins if p.get("name"))
    fields = [lib_id, name, description, pin_names]
    return " ".join(f for f in fields if f).strip()

# --------------------
# Main build
# --------------------

def build_from_file(path: Path) -> List[Dict[str, Union[str, list, dict]]]:
    lib_id = path.stem  # filename without extension as lib_id (per your convention)
    text = path.read_text(encoding="utf-8", errors="replace")
    ast = parse_sexpr(text)
    symbols = find_top_level_symbols(ast)

    out = []
    for sym in symbols:
        # sym = ['symbol', 'NAME', ...]
        if not (is_list(sym) and len(sym) >= 2 and isinstance(sym[1], str)):
            continue
        name = sym[1]
        # The top-level symbol often has nested 'symbol' units; we still extract pins by walking the subtree.
        description = extract_description(sym)
        pins = extract_pins(sym)
        record = {
            "lib_id": lib_id,
            "name": name,
            "description": description,
            "pins": [{"name": p["name"], "type": p["type"]} for p in pins],
        }
        text_flat = derive_text_flat(lib_id, name, description, pins)
        pin_tokens = derive_pin_tokens(pins)
        out.append({
            "record": record,
            "text_flat": text_flat,
            "pin_tokens": pin_tokens,
        })
    return out

DEBUG = False

skip_libs = {
    "Driver_Tec",
    "MCU_STC",
    "MCU_WCH_CH32V0",
    "MCU_WCH_CH32V2",
    "MCU_WCH_CH32V3",
    "MCU_WCH_CH32X0",
    "Interface_Telecom",
    "MCU_Texas_SimpleLink",
    "4xxx_IEEE",
    "Diode_Laser",
    "Diode_Bridge",
    "Valve",
    "CPU_PowerPC",
    "Amplifier_Video",
    "Fiber_Optic",
    "MCU_NXP_ColdFire",
    "MCU_Puya",
    "4xxx",
    "Graphic",
    "74xx",
    "74xGxx",
    "74xx_IEEE"
}
FPGA_FILTER = re.compile(r'^(FPGA|CPLD|GAL|EPM|MAX|XC|ATF|LCMX|ICE40|Lattice|Altera|Xilinx|MachXO)', re.IGNORECASE)

def main():
    base = Path(KICAD_SYMBOL_LIB_PATH)
    if not base.is_dir():
        print(f"Error: KICAD_SYMBOL_LIB_PATH '{base}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    all_rows = []

    if DEBUG:
        test_file = base / "Device.kicad_sym"
        rows = build_from_file(test_file)
        all_rows.extend(rows)
    else:
        for p in base.rglob("*.kicad_sym"):
            try:
                # Match the lib file name with skip list and FPGA filter
                lib_name = p.stem
                if lib_name in skip_libs or FPGA_FILTER.match(lib_name):
                    print(f"[INFO] Skipping library '{lib_name}'", file=sys.stderr)
                    continue
                rows = build_from_file(p)
                all_rows.extend(rows)
            except Exception as e:
                print(f"[WARN] Failed to parse {p}: {e}", file=sys.stderr)

    # write JSONL cache and also print to stdout
    with open(OUT_JSONL, "w", encoding="utf-8") as f:
        for row in all_rows:
            line = json.dumps(row, ensure_ascii=False)
            f.write(line + "\n")
            print(line)

    print(f"\nWrote {len(all_rows)} symbols to {OUT_JSONL}", file=sys.stderr)

if __name__ == "__main__":
    main()