#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge duplicated function labels in taxonomy + lib_tree.

Typical issue:
  "Thyristor": ["SCR", "SCR.", "AC power control", "AC power control."]

We canonicalize function labels (strip punctuation/whitespace etc.) and
merge entries that normalize to the same canonical label.

Inputs:
  taxonomy_path: lib_tree.taxonomy.json
    {
      "categories": [...],
      "functions_by_category": {
        "Thyristor": ["SCR", "SCR.", "AC power control", "AC power control."],
        ...
      }
    }

  tree_path: lib_tree.json
    {
      "Thyristor": {
        "SCR":        { "lib1": ["symA", ...], ... },
        "SCR.":       { "lib2": ["symB", ...], ... },
        "AC power control":  {...},
        "AC power control.": {...}
      },
      ...
    }

Usage:
  python merge_taxonomy_tree_duplicates.py \
      --taxonomy component_repository.taxonomy.json \
      --tree component_repository.json \
      --out-taxonomy component_repository.taxonomy.clean.json \
      --out-tree component_repository.clean.json
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, Any


def canonicalize_label(label: str) -> str:
    """
    Canonical form for labels:
      - strip leading/trailing whitespace
      - lowercase
      - remove trailing punctuation like '.' or ',' etc.
      - collapse internal whitespace
      - strip other non-alnum to spaces
    This maps "SCR." and "scr" to the same slug, and
    "AC power control." and "AC-power control" -> "ac power control".
    """
    s = label.strip()
    # remove trailing punctuation (.,;: etc.)
    s = re.sub(r"[.,;:\s]+$", "", s)
    s = s.lower()
    # replace non-alphanumeric with space
    s = re.sub(r"[^a-z0-9]+", " ", s)
    # collapse spaces
    s = re.sub(r"\s+", " ", s)
    return s or ""


def merge_taxonomy_and_tree(
    taxonomy_path: str,
    tree_path: str,
    out_taxonomy_path: str = None,
    out_tree_path: str = None,
) -> None:
    taxonomy_path = Path(taxonomy_path)
    tree_path = Path(tree_path)

    if out_taxonomy_path is None:
        out_taxonomy_path = taxonomy_path
    else:
        out_taxonomy_path = Path(out_taxonomy_path)

    if out_tree_path is None:
        out_tree_path = tree_path
    else:
        out_tree_path = Path(out_tree_path)

    # ----- Load files -----
    with taxonomy_path.open("r", encoding="utf-8") as f:
        taxonomy = json.load(f)
    with tree_path.open("r", encoding="utf-8") as f:
        tree = json.load(f)

    functions_by_category: Dict[str, Any] = taxonomy.get("functions_by_category", {})

    # ----- Process each category -----
    for category, func_list in list(functions_by_category.items()):
        if not isinstance(func_list, list):
            continue

        # 1) Build canonical mapping: slug -> canonical_label (first seen)
        slug_to_label: Dict[str, str] = {}
        # Also map original_label -> canonical_label
        original_to_canonical: Dict[str, str] = {}

        for f in func_list:
            if not isinstance(f, str):
                continue
            slug = canonicalize_label(f)
            if not slug:
                # keep weird ones as-is
                canonical = f
            else:
                if slug in slug_to_label:
                    canonical = slug_to_label[slug]
                else:
                    # first time we see this slug; choose this as canonical
                    canonical = f.strip()
                    slug_to_label[slug] = canonical
            original_to_canonical[f] = canonical

        # 2) Rebuild function list for this category = unique canonical labels
        uniq_funcs = list(dict.fromkeys(original_to_canonical.values()))
        functions_by_category[category] = uniq_funcs

        # 3) Fix the tree for this category, merging function keys as needed
        if category in tree and isinstance(tree[category], dict):
            func_dict = tree[category]  # old: func -> lib_map
            new_func_dict: Dict[str, Dict[str, list]] = {}

            for old_func, lib_map in func_dict.items():
                if not isinstance(old_func, str):
                    continue
                canonical = original_to_canonical.get(old_func, old_func.strip())
                # ensure canonical exists even if function not in taxonomy list
                if canonical not in uniq_funcs:
                    uniq_funcs.append(canonical)
                    functions_by_category[category] = uniq_funcs

                # merge lib maps under canonical label
                dest = new_func_dict.setdefault(canonical, {})
                if isinstance(lib_map, dict):
                    for lib_id, names in lib_map.items():
                        # names may be list of symbol names
                        dest_names = dest.setdefault(lib_id, [])
                        if isinstance(names, list):
                            dest_names.extend(names)
                        else:
                            dest_names.append(names)

            # dedup & sort names per lib_id
            for canonical, lib_map in new_func_dict.items():
                for lib_id, names in lib_map.items():
                    # make unique, preserve stable order
                    seen = set()
                    uniq = []
                    for nm in names:
                        if nm not in seen:
                            seen.add(nm)
                            uniq.append(nm)
                    lib_map[lib_id] = uniq

            tree[category] = new_func_dict

    # ----- Save outputs -----
    taxonomy["functions_by_category"] = functions_by_category

    out_taxonomy_path.parent.mkdir(parents=True, exist_ok=True)
    out_tree_path.parent.mkdir(parents=True, exist_ok=True)

    with out_taxonomy_path.open("w", encoding="utf-8") as f:
        json.dump(taxonomy, f, ensure_ascii=False, indent=2)

    with out_tree_path.open("w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)

    print(f"✓ Cleaned taxonomy written to: {out_taxonomy_path}")
    print(f"✓ Cleaned tree written to: {out_tree_path}")


def parse_args():
    ap = argparse.ArgumentParser(description="Merge duplicated function labels in taxonomy + lib_tree.")
    ap.add_argument("--taxonomy", required=True, help="Path to lib_tree.taxonomy.json")
    ap.add_argument("--tree", required=True, help="Path to lib_tree.json")
    ap.add_argument("--out-taxonomy", default=None, help="Output taxonomy path (default: overwrite input)")
    ap.add_argument("--out-tree", default=None, help="Output tree path (default: overwrite input)")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    merge_taxonomy_and_tree(
        taxonomy_path=args.taxonomy,
        tree_path=args.tree,
        out_taxonomy_path=args.out_taxonomy,
        out_tree_path=args.out_tree,
    )