# ========= 1) Fixed hierarchy (closed world) =========
# CATEGORIES: List[str] = [
#     "Digital", "Mixed-Signal", "Analog", "Power", "Interface/Connectivity",
#     "RF/Microwave", "Sensors", "Memory/Storage", "Timing/Clock",
#     "Discrete Semiconductors", "Passive", "Isolation",
#     "Opto/Display/Output", "Electromechanical", "Protection", "Other"
# ]

# FUNCTIONS_BY_CATEGORY: Dict[str, List[str]] = {
#     "Digital": ["MCU", "CPU/SoC", "FPGA/CPLD", "Logic", "Memory Controller"],
#     "Mixed-Signal": ["ADC", "DAC", "Audio Codec/ADC/DAC", "Clock Generator/Buffer"],
#     "Analog": ["Amplifier", "Comparator", "Analog Switch/Multiplexer", "Voltage Reference", "Active Filter"],
#     "Power": ["Regulator", "Battery Management", "Gate/Power Driver", "Motor Driver", "Power Monitor/Supervisor"],
#     "Interface/Connectivity": ["USB", "Ethernet", "Serial (I2C)", "Serial (SPI)", "Serial (UART/RS-232)", "Serial (RS-485/LIN/CAN)", "PCIe/MIPI/HDMI"],
#     "RF/Microwave": ["RF Transceiver", "LNA/PA/Mixer/PLL/RF-Switch/Balun"],
#     "Sensors": ["Gas", "Current", "Temperature", "Pressure", "Motion", "Proximity", "Humidity", "Optical", "Touch", "Energy"],
#     "Memory/Storage": ["Flash/EEPROM/FRAM", "SRAM/DRAM"],
#     "Timing/Clock": ["Crystal/Resonator", "Oscillator", "RTC"],
#     "Discrete Semiconductors": ["Diode", "Transistor/MOSFET/IGBT/Thyristor"],
#     "Passive": ["Resistor/Network", "Capacitor/Network", "Inductor", "Transformer", "EMI Filter/Bead/CMC"],
#     "Isolation": ["Optocoupler", "Digital Isolator/Isolated Amp"],
#     "Opto/Display/Output": ["LED/LED Driver", "Display Driver", "Audio Power Amplifier"],
#     "Electromechanical": ["Connector", "Switch/Button/Encoder", "Relay/Buzzer"],
#     "Protection": ["ESD/Surge Protection", "Fuse/PTC/Surge"],
#     "Other": ["Uncategorized"]
# }

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Top-down pseudo-hierarchical clustering builder:
  Category (grown dynamically) -> Function (grown per-category) -> lib_id -> [symbol names]

Input: JSONL lines like
{"record": {"lib_id": "...", "name": "...", "description": "...", "pins":[...]}, "text_flat": "...", "pin_tokens":[...]}

Output:
  component_repository.json  (Category -> Function -> lib_id -> [names, ...])

Usage:
  python categorize_lib.py ./PCB_Semantic_Retrieval/symbol_index.json --out component_repository.json
"""

import os, sys
project_path = os.environ.get("PROJECT_PATH")
sys.path.append(project_path)

import json, re, argparse
from collections import defaultdict
from typing import Dict, Any, List, Tuple, Optional
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from pydantic import BaseModel

from modules.utils.llm_interface import GetLLMInterface

llm = GetLLMInterface(model_name="gpt-5", model_provider="OpenRouter")

# ========= 1) Dynamic hierarchy (initially empty) =========
CATEGORIES: List[str] = []                      # grows as we see new symbols
FUNCTIONS_BY_CATEGORY: Dict[str, List[str]] = {}  # cat -> [functions]

# Locks to protect shared taxonomy structures
taxonomy_lock = Lock()
# Optional: lock llm calls if you suspect underlying client is not thread-safe
# llm_lock = Lock()


# ========= 4) Utility: text blob from record =========
def _blob_from_record(rec: Dict[str, Any], obj: Dict[str, Any]) -> str:
    name = (rec.get("name") or "")
    desc = (rec.get("description") or "")
    pins = rec.get("pins") or []
    pin_text = " ".join(f"{p.get('name','')} {p.get('type','')}" for p in pins)
    return " ".join([name, desc, pin_text]).lower()


# ========= LLM helpers =========

def get_category(blob: str, categories: List[str]) -> str:
    """
    Ask LLM to choose the best category from a *non-empty* list.
    Returns an element of `categories` if any match is found in response,
    otherwise proposes a new category.
    """
    query = (
        f"Given the record from a KiCAD symbol library:\n"
        f"\"{blob}\"\n\n"
        f"Extract information from online if needed and think carefully. Read the following options:\n"
        f"{', '.join(categories)}.\n"
        f"If you find a perfect match, reply with ONLY the category name."
        f"If not, assume that you are organizing electronic components into high-level categories "
        f"for PCB design (e.g. 'Power', 'Passive', 'RF', 'Sensor', etc.), please propose a new category instead, with the category name ONLY."
    )
    messages = [{"role": "user", "content": query}]
    # with llm_lock:
    response = llm.get_string_response(messages)
    return response


def get_function(blob: str, funcs: List[str]) -> str:
    """
    Ask LLM to choose the best function from a *non-empty* list.
    Returns an element of `funcs` if any match is found in response, othwise proposes a new function.
    """
    query = (
        f"Given the record from a KiCAD symbol library:\n"
        f"\"{blob}\"\n\n"
        f"Extract information from online if needed and think carefully. Read the following options:\n"
        f"{', '.join(funcs)}.\n"
        f"If you find a perfect match, reply with ONLY the function name."
        f"If not, assume that you are organizing electronic components into high-level categories "
        f"for PCB design (e.g. for power, power protection, power regulation and etc), please propose a new function instead, with the function name ONLY."
    )
    messages = [{"role": "user", "content": query}]
    # with llm_lock:
    response = llm.get_string_response(messages)
    return response


# ========= 7) Category, then Function (dynamic, LLM-driven) =========

def classify_category(obj: Dict[str, Any]) -> str:
    """
    1. Take a snapshot of current CATEGORIES.
    2. If any exist, ask LLM to pick from them.
    3. If no match or list empty, ask LLM to propose a new category,
       then add it to the global list (thread-safe).
    """
    rec = obj.get("record", {})
    blob = _blob_from_record(rec, obj)

    # Step 1: snapshot current categories
    with taxonomy_lock:
        existing_cats = list(CATEGORIES)

    # Step 2: try to pick an existing one
    choice = get_category(blob, existing_cats)

    with taxonomy_lock:
        # check if someone else already added an equivalent category
        for cat in CATEGORIES:
            if cat.lower() == choice.lower():
                return cat
        CATEGORIES.append(choice)
        FUNCTIONS_BY_CATEGORY.setdefault(choice, [])
        return choice


def classify_function(obj: Dict[str, Any], category: str) -> str:
    """
    For the given category:
    1. Snapshot current function list for this category.
    2. If any exist, ask LLM to pick from them.
    3. If no match or list empty, ask LLM to propose a new function,
       then add it to the list for this category (thread-safe).
    """
    rec = obj.get("record", {})
    blob = _blob_from_record(rec, obj)

    with taxonomy_lock:
        existing_funcs = list(FUNCTIONS_BY_CATEGORY.get(category, []))

    # Step 2: try to pick an existing function
    choice = get_function(blob, existing_funcs)

    with taxonomy_lock:
        funcs = FUNCTIONS_BY_CATEGORY.setdefault(category, [])
        # avoid duplicates with case-insensitive compare
        for f in funcs:
            if f.lower() == choice.lower():
                return f
        funcs.append(choice)
        return choice


# ========= 8) Multithreaded tree building =========

FourLevelTree = Dict[str, Dict[str, Dict[str, set]]]

def _new_tree() -> FourLevelTree:
    return defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

def _merge_trees(dst: FourLevelTree, src: FourLevelTree) -> None:
    """Merge src into dst in-place."""
    for cat, funcs in src.items():
        for func, libs in funcs.items():
            for lib_id, names in libs.items():
                dst[cat][func][lib_id].update(names)


def _process_lines(lines: List[str]) -> Tuple[FourLevelTree, List[Dict[str, Any]]]:
    """
    Worker: process a batch of JSONL lines -> partial tree records.
    Uses global classify_category/function which mutate the global taxonomy
    under locks.
    """
    tree = _new_tree()
    for line in lines:
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        rec = obj.get("record", {}) or {}
        lib_id = rec.get("lib_id")
        name = rec.get("name", "") or ""
        if not lib_id:
            continue

        category = classify_category(obj)
        function = classify_function(obj, category)

        tree[category][function][lib_id].add(name)

    return tree


def build_tree_mt(
    jsonl_path: str,
    out_json_path: str,
    workers: int = 8,
    chunk_size: int = 5000,
) -> None:
    """Multi-threaded build of the 4-level tree."""
    # Read all lines once; for very large files you can stream in rolling chunks instead
    with open(jsonl_path, "r", encoding="utf-8") as fin:
        all_lines = fin.readlines()

    # Partition into chunks
    chunks: List[List[str]] = [all_lines[i:i+chunk_size] for i in range(0, len(all_lines), chunk_size)]

    merged_tree = _new_tree()

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(_process_lines, chunk) for chunk in chunks]
        for fut in as_completed(futures):
            part_tree = fut.result()
            _merge_trees(merged_tree, part_tree)

    # Convert sets -> sorted lists for a stable JSON
    out_tree = {
        cat: {
            func: {
                lib_id: sorted(list(names))
                for lib_id, names in libs.items()
            }
            for func, libs in funcs.items()
        }
        for cat, funcs in merged_tree.items()
    }

    # Ensure output directory exists
    out_json_path = Path(out_json_path)
    out_json_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(out_tree, f, ensure_ascii=False, indent=2)

    print(f"✓ wrote 4-level tree to {out_json_path}", file=sys.stderr)

    # Optionally, dump the learned taxonomy itself
    with taxonomy_lock:
        taxonomy = {
            "categories": list(CATEGORIES),
            "functions_by_category": {k: list(v) for k, v in FUNCTIONS_BY_CATEGORY.items()},
        }
    tax_path = out_json_path.with_suffix(".taxonomy.json")
    with open(tax_path, "w", encoding="utf-8") as tf:
        json.dump(taxonomy, tf, ensure_ascii=False, indent=2)
    print(f"✓ wrote learned taxonomy to {tax_path}", file=sys.stderr)


def parse_args():
    ap = argparse.ArgumentParser(description="Multi-threaded pseudo-hierarchical Category->Function->lib_id->name tree builder.")
    ap.add_argument("input_jsonl", help="Input JSONL path")
    ap.add_argument("--out", default=Path(project_path) / "export" / "component_repository.json", help="Output tree JSON")
    ap.add_argument("--workers", type=int, default=8, help="Thread pool size")
    ap.add_argument("--chunk-size", type=int, default=5000, help="Lines per worker task")
    return ap.parse_args()


def main():
    args = parse_args()
    build_tree_mt(
        jsonl_path=args.input_jsonl,
        out_json_path=args.out,
        workers=args.workers,
        chunk_size=args.chunk_size,
    )


if __name__ == "__main__":
    main()