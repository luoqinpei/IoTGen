'''
Extend the basic symbol information with detailed descriptions using LLM inference. This script is designed to be resume-friendly, allowing you to stop and restart without losing progress. It uses a ThreadPoolExecutor for concurrent processing and tqdm for live progress tracking.
'''
from pydantic import BaseModel, Field
import argparse
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from tqdm import tqdm


class ExtendedSymbols(BaseModel):
    name: str = Field(description="Human-readable name of the device / symbol")
    footprint: str = Field(description="Suggested package / footprint name")
    technical_specification: str = Field(
        alias="technical specification",
        description="Short technical description of the device capabilities and interfaces"
    )
    function: str = Field(description="High-level function of this device in a circuit")
    potential_application: str = Field(
        alias="potential application",
        description="Typical end applications / use cases"
    )

    model_config = {
        "validate_by_name": True,
        "populate_by_name": True,
    }


def build_local_msg(line_obj: dict) -> list[dict]:
    return [
        {
            "role": "system",
            "content": (
                "You are an expert in PCB design and KiCad symbol libraries. "
                "Given a symbol record, summarize it into a concise JSON object with the "
                "following fields: name, footprint, technical specification, function, "
                "and potential application."
            ),
        },
        {
            "role": "user",
            "content": (
                "Here is one symbol entry from my index. "
                "Please infer the requested fields:\n\n"
                f"{json.dumps(line_obj, ensure_ascii=False)}"
            ),
        },
    ]


import os, sys
project_path = os.environ.get("PROJECT_PATH", "")
if project_path:
    sys.path.append(project_path)

from modules.utils.llm_interface import GetLLMInterface

llm = GetLLMInterface(model_name="gpt-5", model_provider="OpenRouter")


# -----------------------------------------------------
# Load names already processed
# -----------------------------------------------------
def load_processed_names(out_path: Path) -> set[str]:
    processed = set()
    if not out_path.exists():
        return processed

    with out_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue

            name = None
            dd = obj.get("detailed_description", {})
            if isinstance(dd, dict):
                name = dd.get("name")

            if not name:
                name = obj.get("name")

            if name:
                processed.add(name)

    print(f"[INFO] Loaded {len(processed)} processed symbol names.")
    return processed


# -----------------------------------------------------
# Process one symbol entry
# -----------------------------------------------------
def _process_one_entry(ln: str) -> Optional[tuple[str, str]]:
    ln = ln.strip()
    if not ln:
        return None

    try:
        entry = json.loads(ln)
    except Exception as e:
        print(f"[WARN] Bad JSON: {e}")
        return None

    name = entry.get("name")
    if not name and isinstance(entry.get("record"), dict):
        name = entry["record"].get("name")
    if not name:
        print("[WARN] No 'name' found, skipping.")
        return None

    msgs = build_local_msg(entry)

    try:
        raw, desc_obj = llm.get_json_response_retry(msgs, ExtendedSymbols)
    except Exception as e:
        print(f"[WARN] LLM error for {name}: {e}")
        return None

    try:
        entry["detailed_description"] = desc_obj.dict(by_alias=True)
        return name, json.dumps(entry, ensure_ascii=False)
    except Exception as e:
        print(f"[WARN] Serialization error for {name}: {e}")
        return None


# -----------------------------------------------------
# Main enhance function (with tqdm!)
# -----------------------------------------------------
def enhance_symbol_jsonl(input_jsonl: str, output_jsonl: str, num_workers: int = 4):

    in_path = Path(input_jsonl)
    out_path = Path(output_jsonl)

    # Load processed names
    processed_names = load_processed_names(out_path)

    # Load input
    with in_path.open("r", encoding="utf-8") as fin:
        input_lines = fin.readlines()

    # Filter remaining work
    work_items = []
    for ln in input_lines:
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        name = obj.get("name")
        if not name and isinstance(obj.get("record"), dict):
            name = obj["record"].get("name")
        if name and name not in processed_names:
            work_items.append(ln)

    print(f"[INFO] {len(processed_names)} already done, {len(work_items)} to process.")

    if not work_items:
        print("[INFO] Nothing to do.")
        return

    # Write mode append
    with out_path.open("a", encoding="utf-8") as fout:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = {executor.submit(_process_one_entry, ln): ln for ln in work_items}

            # Use tqdm to show live progress
            with tqdm(total=len(futures), desc="Processing", ncols=100) as pbar:
                for future in as_completed(futures):
                    res = future.result()
                    if res is not None:
                        name, enhanced_json = res
                        fout.write(enhanced_json + "\n")
                        fout.flush()
                        processed_names.add(name)
                    pbar.update(1)


# -----------------------------------------------------
# CLI
# -----------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhance symbol JSONL with detailed descriptions (resume-friendly).")
    parser.add_argument("--input_jsonl", type=str, required=True)
    parser.add_argument("--output_jsonl", type=str, required=True)
    parser.add_argument("--num-workers", type=int, default=32)
    args = parser.parse_args()

    # make sure output dir exists
    Path(args.output_jsonl).parent.mkdir(parents=True, exist_ok=True)

    enhance_symbol_jsonl(
        args.input_jsonl,
        args.output_jsonl,
        args.num_workers,
    )