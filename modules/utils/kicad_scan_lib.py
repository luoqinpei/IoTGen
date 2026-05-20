'''
This module provides utilities to scan and organize KiCad symbol and footprint libraries. It can read .kicad_sym files to extract symbol definitions and their properties, as well as .kicad_mod files for footprint information. The gathered data is organized into structured dictionaries and can be saved/loaded as JSON for easy access. Additionally, it includes a caching mechanism using SQLite to store computed symbol contexts for faster retrieval in future runs.

This module is essential to create the jsonl symbol and footprint libraries for the symbol/footprint retrieval components in the schematic and PCB layout agents. It can be run as a standalone script under the project directory to perform the scanning and save the organized libraries to disk.
'''


import os
from pathlib import Path
import json
from threading import Lock
import sqlite3
from typing import Iterable, List, Tuple, Dict

if __name__ == "__main__":
    import sys
    # open config file to get the project path
    # with open("./configs/proj_folder_path.txt", "r") as f:
    #     lines = f.readlines()
    #     project_path = lines[0].strip()
    #     sys.path.append(project_path)
    project_path = os.environ["PROJECT_PATH"]
    sys.path.append(project_path)



from modules.utils.kicad_add_symbol import parse_sexp
from config import KICAD_SYMBOL_LIB_PATH, KICAD_FOOTPRINT_LIB_PATH


def read_sym_lib(path):
    return parse_sexp(path.read_text(encoding='utf-8'))


# Skip a few libraries not used. Not going to construct PCB from digital logic...
SKIP_LIB = [
    "4xxx",
    "4xxx_IEEE",
    "74xGxx",
    "74xx",
    "74xx_IEEE",
]


def gather_symbols_by_lib(lib_dir: str, fields: dict = None) -> dict:
    """
    Scan all .kicad_sym files under lib_dir.
    Return a dict: { library_name: [ {name, footprint, …}, … ], … }
    """
    if fields is None:
        fields = {
            'footprint': 'Footprint',
            'datasheet': 'Datasheet',
            'description': 'Description'
        }

    sym_paths = list(Path(lib_dir).glob('*.kicad_sym'))
    total_libs = len(sym_paths)
    result = {}

    for lib_idx, symfile in enumerate(sym_paths, start=1):
        lib_name = symfile.stem  # filename without extension
        sys.stdout.write(f"\rLib {lib_idx}/{total_libs}: {lib_name}         ")
        sys.stdout.flush()

        if lib_name in SKIP_LIB:
            print(f"Skipping library {lib_name}")
            continue

        lib = read_sym_lib(symfile)
        symbols = [item for item in lib
                   if isinstance(item, list) and item and item[0] == 'symbol']

        result[lib_name] = []
        total_syms = len(symbols)
        for sym_idx, item in enumerate(symbols, start=1):
            sys.stdout.write(f"\rLib {lib_idx}/{total_libs}: {lib_name} "
                             f"- symbol {sym_idx}/{total_syms}      ")
            sys.stdout.flush()

            info = {'name': item[1]}
            # if "AMS1117" in item[1]: # debugging symbol info
            #     pass
            for prop in item:
                if isinstance(prop, list) and prop:
                    if prop[0] == 'property':
                        key, val = prop[1], prop[2]
                        for out_key, want in fields.items():
                            if key == want or key == f'"{want}"':
                                info[out_key] = val
                    elif prop[0] == 'symbol':
                        # Get the spatial symbol definitions including sizes and pin locations
                        if 'symbol' not in info:
                            info['symbol'] = [prop]
                        else:
                            info['symbol'].append(prop)
                    elif prop[0] == 'extends':
                        # If the symbol extends another symbol -- share the same symbol definition info
                        info['extends'] = f"{prop[1]}"
                        info['symbol'] = f"This symbol extends symbol {prop[1]}, so refer to the symbol info of {prop[1]}."
                        # # if already parsed, we can just copy the symbol info
                        # BUt too long... skip it.
                        # for tmp_item in result[lib_name]:
                        #     if tmp_item['name'] == prop[1]:
                        #         if 'symbol' in tmp_item:
                        #             info['symbol'] = tmp_item['symbol'].copy()
                        #             # replace symbol name to the current one
                        #             for sym_def in info['symbol']:
                        #                 sym_def[1] = sym_def[1].replace(prop[1].replace('"', ''), item[1].replace('"', ''))
                        #         break

            result[lib_name].append(info)

        # clear line
        sys.stdout.write('\r' + ' ' * 80 + '\r')

    print("Done.")
    return result


def count_symbol_per_lib(org_lib: dict, target_lib_name: str = None) -> dict:
    """
    Count the number of symbols in each library.
    Return a dict: { library_name: symbol_count, … }
    """
    result = {}
    total_ct = 0
    for lib_name, symbols in org_lib.items():
        if target_lib_name and lib_name != target_lib_name:
            continue
        result[lib_name] = len(symbols)
        print(f"{lib_name}: {result[lib_name]} symbols")

        total_ct += result[lib_name]

    print(f"Total: {total_ct} symbols")
    return result

def save_organized_lib(org_lib: dict, out_dir: str) -> None:
    """
    Save the organized library to a file.
    """
    out_path = Path(out_dir) / 'organized_lib.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(org_lib, f, indent=4, ensure_ascii=False)
    print(f"Organized library saved to {out_path}")

def save_organized_fp(org_lib: dict, out_dir: str) -> None:
    """
    Save the organized footprint library to a file.
    """
    out_path = Path(out_dir) / 'organized_fp.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(org_lib, f, indent=4, ensure_ascii=False)
    print(f"Organized footprint library saved to {out_path}")

def load_organized_lib(path: str = "./export/organized_lib.json") -> dict:
    """
    Load the organized library from a file.
    """
    if not Path(path).exists():
        print(f"File {path} does not exist.")
        return {}

    with open(path, 'r', encoding='utf-8') as f:
        org_lib = json.load(f)
    return org_lib

def load_organized_fp(json_path: Path) -> dict:
    """
    Load the organized footprint index from JSON.
    Expected shape (as produced by gather_footprints_by_lib):
      {
        "LibraryNickname": [
          {"name": "...", "descr": "...", "tags": "...", "attr": [...], ...},
          ...
        ],
        ...
      }
    Returns the same dict, but without modification.
    """
    if not json_path.exists():
        raise FileNotFoundError(f"Footprint JSON not found: {json_path}")
    with json_path.open('r', encoding='utf-8') as f:
        org_fp = json.load(f)
    return org_fp

_SYM_CACHE_WRITE_LOCK = Lock()

def _open_sym_cache(db_path: Path) -> sqlite3.Connection:
    """Open (and initialize) the symbol context cache database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path.as_posix(), timeout=30.0, check_same_thread=False)
    # Better concurrency for many readers / few writers
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sym_cache (
            key         TEXT PRIMARY KEY,
            lib         TEXT NOT NULL,
            name        TEXT NOT NULL,
            context     TEXT NOT NULL,
            meta_json   TEXT,
            updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return conn

def _sym_key(lib: str, name: str) -> str:
    """Build a stable cache key for a symbol definition (library + symbol name)."""
    return f"{lib}::{name}"

def _get_ctx_from_cache(conn: sqlite3.Connection, key: str) -> str | None:
    row = conn.execute("SELECT context FROM sym_cache WHERE key=?", (key,)).fetchone()
    return row[0] if row else None

def _put_ctx_into_cache(conn: sqlite3.Connection, key: str, lib: str, name: str,
                        context: str, meta: dict | None = None) -> None:
    meta_json = json.dumps(meta or {}, ensure_ascii=False)
    with _SYM_CACHE_WRITE_LOCK:
        conn.execute(
            """
            INSERT INTO sym_cache(key, lib, name, context, meta_json)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                context=excluded.context,
                meta_json=excluded.meta_json,
                updated_at=CURRENT_TIMESTAMP
            """,
            (key, lib, name, context, meta_json),
        )
        conn.commit()

def get_sym_context_with_cache(
    sym_list, sym_infos, editor, cache_db: Path
) -> str:
    """
    For each symbol in sym_list:
      - read context from cache if present
      - otherwise compute (using editor.describe_symbol_info), then cache it
    Return a single concatenated sym_context string in the order of sym_list.
    """
    conn = _open_sym_cache(cache_db)
    try:
        ordered_contexts: list[str] = []

        for sym_ref, sym_info in zip(sym_list, sym_infos):
            # Extract library/name from your sym_infos structure.
            # Adjust the field names below to match your actual data schema.
            info = sym_infos[sym_ref] if isinstance(sym_infos, dict) else sym_ref
            lib, name = sym_ref
            if lib is None or name is None:
                raise ValueError(f"Missing library/name for symbol {sym_ref}: {info}")

            key = _sym_key(lib, name)
            
            # 1) Try cache
            ctx = _get_ctx_from_cache(conn, key)
            if ctx is None:
                # 2) Not cached -> compute just for THIS symbol, then cache
                #    If your describe function only accepts full lists,
                #    we pass a singleton view.
                single_sym_list = [sym_ref]
                single_sym_infos = [sym_info]

                ctx = editor.describe_symbol_info(single_sym_list, single_sym_infos)
                _put_ctx_into_cache(conn, key, lib, name, ctx, meta=info)

            ordered_contexts.append(ctx)

        # 3) Combine all symbol contexts into one final block
        return "\n".join(ordered_contexts)

    finally:
        conn.close()

def to_lib_name_tuples(
    symbols,
    remap: Dict[Tuple[str, str], Tuple[str, str]] | None = None,
    extras: Iterable[Tuple[str, str]] | None = None,
) -> List[Tuple[str, str]]:
    """
    Convert [SymbolInfo] -> [(lib, name)], with optional remapping and extra entries.

    remap: map from (lib, name) -> (new_lib, new_name)
    extras: extra tuples to append at the end
    """
    remap = remap or {}
    out: List[Tuple[str, str]] = []
    for s in symbols:
        tup = (s.lib_name, s.name)
        out.append(remap.get(tup, tup))
    if extras:
        out.extend(extras)
    return out


# Below part is designed for handling the footprint library in a similar way.
# Optional: skip some library directories by nickname
import re

SKIP_LIB = set()

# ------------ Regex helpers (tolerant parsing for .kicad_mod) ------------
RE_FOOTPRINT_NAME = re.compile(r'\(\s*footprint\s+"([^"]+)"', re.S)
RE_LAYER          = re.compile(r'\(\s*layer\s+"([^"]+)"\s*\)', re.S)
RE_DESCR          = re.compile(r'\(\s*descr\s+"([^"]*)"', re.S)
RE_TAGS           = re.compile(r'\(\s*tags\s+"([^"]*)"', re.S)
RE_ATTR           = re.compile(r'\(\s*attr\s+([^)]+)\)', re.S)
RE_VERSION        = re.compile(r'\(\s*version\s+(\d+)\s*\)')
RE_GENERATOR      = re.compile(r'\(\s*generator\s+"([^"]+)"\s*\)')
RE_GEN_VER        = re.compile(r'\(\s*generator_version\s+"?([^"\)]+)"?\s*\)')

# property "Reference"/"Value" blocks with (at x y rot)
RE_PROP_BLOCK = re.compile(
    r'\(\s*property\s+"(Reference|Value)"\s+"([^"]*)".*?\(\s*at\s+([-\d\.eE]+)\s+([-\d\.eE]+)(?:\s+([-\d\.eE]+))?\s*\)',
    re.S
)

# 3D model block
RE_MODEL_PATH = re.compile(r'\(\s*model\s+"([^"]+)"', re.S)
RE_MODEL_OFFSET = re.compile(r'\(\s*offset\s*\(\s*xyz\s+([-\d\.eE]+)\s+([-\d\.eE]+)\s+([-\d\.eE]+)\s*\)\s*\)', re.S)
RE_MODEL_SCALE  = re.compile(r'\(\s*scale\s*\(\s*xyz\s+([-\d\.eE]+)\s+([-\d\.eE]+)\s+([-\d\.eE]+)\s*\)\s*\)', re.S)
RE_MODEL_ROT    = re.compile(r'\(\s*rotate\s*\(\s*xyz\s+([-\d\.eE]+)\s+([-\d\.eE]+)\s+([-\d\.eE]+)\s*\)\s*\)', re.S)

# Pad blocks (captures: name, type, shape, at-x, at-y, size-x, size-y, layers list, roundrect_rratio)
RE_PAD = re.compile(
    r'\(\s*pad\s+"([^"]*)"\s+(\w+)\s+(\w+)'
    r'.*?\(\s*at\s+([-\d\.eE]+)\s+([-\d\.eE]+)(?:\s+[^\)]*)?\)'
    r'(?:.*?\(\s*size\s+([-\d\.eE]+)\s+([-\d\.eE]+)\s*\))?'
    r'(?:.*?\(\s*layers\s+([^\)]+)\))?'
    r'(?:.*?\(\s*roundrect_rratio\s+([-\d\.eE]+)\s*\))?',
    re.S
)

def _first(regex, text, default=None):
    m = regex.search(text)
    return m.group(1) if m else default

def _prop_positions(text):
    """Return dict like {'Reference': {'text': 'REF**', 'x':..., 'y':..., 'rot':...}, 'Value': {...}}"""
    out = {}
    for m in RE_PROP_BLOCK.finditer(text):
        kind, val, x, y, rot = m.groups()
        out[kind] = {
            'text': val,
            'x': float(x),
            'y': float(y),
            'rot': float(rot) if rot is not None else 0.0
        }
    return out

def _model_block(text):
    path = _first(RE_MODEL_PATH, text)
    if not path:
        return None
    off = RE_MODEL_OFFSET.search(text)
    scl = RE_MODEL_SCALE.search(text)
    rot = RE_MODEL_ROT.search(text)
    to_floats = lambda g: tuple(float(x) for x in g.groups()) if g else (0.0, 0.0, 0.0)
    return {
        'path': path,
        'offset_xyz': to_floats(off),
        'scale_xyz':  to_floats(scl) if scl else (1.0, 1.0, 1.0),
        'rotate_xyz': to_floats(rot)
    }

def _pads(text):
    pads = []
    for m in RE_PAD.finditer(text):
        name, ptype, shape, ax, ay, sx, sy, layers, rrr = m.groups()
        pads.append({
            'name': name,                  # can be "" for paste/stencil pads
            'type': ptype,                 # smd/thru_hole/np_thru_hole/etc.
            'shape': shape,                # rect/roundrect/circle/etc.
            'at':   (float(ax), float(ay)),
            'size': (float(sx) if sx else None, float(sy) if sy else None),
            'layers': [s.strip('"') for s in (layers.split() if layers else [])],
            'roundrect_rratio': float(rrr) if rrr else None
        })
    return pads

def read_mod_text(path: Path) -> str:
    """Read a .kicad_mod file as raw text."""
    return path.read_text(encoding='utf-8', errors='ignore')

def parse_footprint_text(text: str) -> dict:
    """Parse a single .kicad_mod text into a footprint info dict."""
    name = _first(RE_FOOTPRINT_NAME, text, default="")
    info = {
        'name': name,
        'version': _first(RE_VERSION, text),
        'generator': _first(RE_GENERATOR, text),
        'generator_version': _first(RE_GEN_VER, text),
        'layer': _first(RE_LAYER, text),
        'descr': _first(RE_DESCR, text, default=""),
        'tags':  _first(RE_TAGS, text, default=""),
        'attr':  (_first(RE_ATTR, text, default="") or "").split(),
        'properties': _prop_positions(text),
        'model': _model_block(text),
        'pads': _pads(text)
    }
    return info

def gather_footprints_by_lib(lib_dir: str) -> dict:
    """
    Scan all *.pretty directories under lib_dir and parse *.kicad_mod files.
    Return a dict:
      {
        library_nickname: [
            { name, version, generator, generator_version, layer, descr, tags, attr,
              properties: { 'Reference': {'text','x','y','rot'}, 'Value': {...} },
              model: {'path','offset_xyz','scale_xyz','rotate_xyz'} or None,
              pads: [ {name,type,shape,at(size),layers,roundrect_rratio}, ... ]
            },
            ...
        ],
        ...
      }
    Notes:
      - 'library_nickname' defaults to the *.pretty folder name.
      - No external dependencies; robust regex parsing of common KiCad constructs.
    """
    root = Path(lib_dir)
    pretty_dirs = list(root.glob('*.pretty'))
    total_libs = len(pretty_dirs)
    result = {}

    for lib_idx, pdir in enumerate(pretty_dirs, start=1):
        lib_name = pdir.stem  # folder name without .pretty
        sys.stdout.write(f"\rLib {lib_idx}/{total_libs}: {lib_name}         ")
        sys.stdout.flush()

        if lib_name in SKIP_LIB:
            print(f"\nSkipping library {lib_name}")
            continue

        mods = list(pdir.glob('*.kicad_mod'))
        result[lib_name] = []
        total_mods = len(mods)

        for mod_idx, mpath in enumerate(mods, start=1):
            sys.stdout.write(f"\rLib {lib_idx}/{total_libs}: {lib_name} "
                             f"- footprint {mod_idx}/{total_mods}      ")
            sys.stdout.flush()
            try:
                text = read_mod_text(mpath)
                info = parse_footprint_text(text)
                # Attach raw path for traceability
                info['__file__'] = str(mpath)
                result[lib_name].append(info)
            except Exception as e:
                # Fail-soft: keep going
                result[lib_name].append({
                    'name': mpath.stem,
                    'error': f'ParseError: {e}',
                    '__file__': str(mpath)
                })

        # clear progress line
        sys.stdout.write('\r' + ' ' * 80 + '\r')

    print("Done.")
    return result



if __name__ == '__main__':

    lib_dir = Path(KICAD_SYMBOL_LIB_PATH)

    sym_lib_dict = gather_symbols_by_lib(lib_dir)

    save_organized_lib(sym_lib_dict, "./export")

    sym_lib_dict = load_organized_lib("./export/organized_lib.json")

    count_symbol_per_lib(sym_lib_dict)

    footprint_dir = Path(KICAD_FOOTPRINT_LIB_PATH)
    footprint_lib_dict = gather_footprints_by_lib(footprint_dir)
    save_organized_fp(footprint_lib_dict, "./export")