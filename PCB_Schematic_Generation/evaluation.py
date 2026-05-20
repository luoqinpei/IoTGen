'''
This script evaluates the performance of trained models (e.g., gpt-oss-20b-pcb-schematic_raw) on a test set of module/schematic pairs. For each pair, it generates code using the model, runs the code to produce a KiCad schematic, and then evaluates the generated schematic against the reference using a custom evaluation function. Results are saved in both JSONL and CSV formats for analysis.

This script is only for testing of generating schematic in the code format.
'''
## Evaluate different models on a common test set
import torch
from pathlib import Path
import sys
import os
project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)
import re
from typing import Union
from datasets import load_dataset
import random
import json
import csv
import tqdm
from datetime import datetime
# Set random seed for reproducibility
SEED = 20250919
random.seed(SEED)
try:
    import numpy as np
    np.random.seed(SEED)
except Exception:
    pass
try:
    import torch
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
except Exception:
    pass

project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)

torch.manual_seed(42)
from transformers import Mxfp4Config
from modules.utils.kicad_scan_lib import get_sym_context_with_cache, load_organized_lib, to_lib_name_tuples
from modules.sch_evaluation import SchematicVerifier, extract_meta_info, evaluation

MAX_TOKENS = 13312
model_names = ["SchGen"]
reasoning_level = "medium"
RANDOM_SAMPLING = True

def get_final_python(decoded: str) -> Path:
    """
    Extract the 'final' section from a decoded model output, strip trailing

    Returns
    -------
    Path
        The path where the Python code was saved.
    """

    # 1) Extract content after <|channel|>final<|message|> and before next marker/end
    final_block_re = re.compile(
        r"<\|channel\|>\s*final\s*<\|message\|>(.*?)(?:(?:<\|channel\|>|<\|end\|>|$))",
        re.S | re.I
    )
    m = final_block_re.search(decoded)
    segment = m.group(1) if m else decoded

    # 2) Remove trailing <|return|> markers (possibly repeated) and trim spaces
    return_suffix_re = re.compile(r'(?:\s*<\|return\|>\s*)+$', re.S)
    segment = return_suffix_re.sub('', segment).strip()

    # 3) Remove Markdown code fences like ```python ... ``` or ``` ... ```
    code_fence_re = re.compile(r"^\s*```(?:[Pp]ython)?\s*\n|\n\s*```\s*$", re.S)
    code_text = code_fence_re.sub("", segment).strip()

    return code_text


# Load trained model
from transformers import AutoModelForCausalLM, AutoTokenizer, Mxfp4Config
from peft import PeftModel

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("openai/gpt-oss-20b")

# load a modified chat template from a file ({% generation %} and {% endgeneration %} addded for assistant_only_loss)
if reasoning_level == "high":
    new_chat_template_path = Path(project_path) / "PCB_Schematic_Generation" / "modified_chat_template_rl_high.txt"
else:
    new_chat_template_path = Path(project_path) / "PCB_Schematic_Generation" /"modified_chat_template.txt"

with new_chat_template_path.open("r", encoding="utf-8") as f:
    new_chat_template = f.read()

tokenizer.chat_template = new_chat_template

def save_jsonl(path: str, items):
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

def run_batch_evaluation(
    jsonl_path: str,
    out_dir: str = "eval_runs",
    model_name: str = None,
):

    # Load the original model first
    quantization_config = Mxfp4Config(dequantize=True)
    model_kwargs = dict(attn_implementation="flash_attention_2", torch_dtype=torch.bfloat16, use_cache=False, device_map="auto", quantization_config=quantization_config)
    base_model = AutoModelForCausalLM.from_pretrained("openai/gpt-oss-20b", **model_kwargs).cuda()
    # Merge fine-tuned weights with the base model
    if model_name == None:
        model = base_model
        model.eval()
    else:
        peft_model_id = f"microsoft/{model_name}" # Published fine-tuned model on HuggingFace
        model = PeftModel.from_pretrained(base_model, peft_model_id)
        model = model.merge_and_unload()
        model.eval()

    CODE_PATH = Path(project_path) / "export" / f"test_code_{model_name}"
    Path(CODE_PATH).mkdir(parents=True, exist_ok=True)

    def save_csv(path: str, items):
        if not items:
            return
        rows = []
        # Store netlist_evaluation as JSON string to avoid nested structure in CSV
        for it in items:
            row = dict(it)
            nle = row.pop("netlist_evaluation", None)
            row["netlist_evaluation_json"] = json.dumps(nle, ensure_ascii=False) if nle is not None else ""
            rows.append(row)
        fieldnames = sorted({k for r in rows for k in r.keys()})
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Santize model name for file naming
    model_name_sanitized = model_name.replace("/", "_").replace("\\", "_")

    out_jsonl = os.path.join(out_dir, f"eval_results_seed_{model_name_sanitized}.jsonl")
    out_csv   = os.path.join(out_dir, f"eval_results_seed_{model_name_sanitized}.csv")

    # Check if out_csv already exists
    if os.path.exists(out_csv):
        print(f"Skipping existing evaluation for model {model_name}.")
        return

    ds = load_dataset("json", data_files=jsonl_path, split="train")
    results = []
    passed_cnt = 0
    total_errors = 0

    for i in tqdm.tqdm(range(len(ds)), desc=f"Evaluating {model_name}"):

        module_name, schematic_name, meta = extract_meta_info(ds[i])
        line = ds[i]
        msg_list = ds[i]["messages"][:2] # only take system and use msg as input.

        code_path = Path(CODE_PATH) / f"{module_name}_{schematic_name}_test.py"
        
        # Check if code already exists
        # if code_path.exists():
        #     print(f"[{i+1}/{len(ds)}] Skipping existing code: {code_path}")
        #     code = code_path.read_text(encoding="utf-8")
        # Disable reading existing code
        if 0 == 1:
            pass
        else:
            # Apply Chat template
            input_ids = tokenizer.apply_chat_template(
                msg_list,
                add_generation_prompt=True,
                return_tensors="pt",
            ).to(model.device)

            # Test with trained model
            output_ids = model.generate(input_ids, max_new_tokens=MAX_TOKENS, attention_mask=torch.ones_like(input_ids))
            # Use newly-generated tokens only
            gen_only = output_ids[:, input_ids.shape[-1]:]
            response = tokenizer.batch_decode(gen_only, skip_special_tokens=False)[0]
            code = get_final_python(response)

            code_path.parent.mkdir(parents=True, exist_ok=True)
            code_path.write_text(code, encoding="utf-8")

        try:
            ev = evaluation(line, code_path, code)  
            ev = ev if isinstance(ev, dict) else {"passed": 0}
        except Exception as e:
            print("ERROR: ", e)
            ev = {"passed": 0, "netlist_evaluation": None, "errors": None, "exception": str(e)}

        # Get the evaluation results
        passed_cnt += int(bool(ev.get("passed", 0)))

        if ev["passed"] == 0:
            rec = {
                "test_idx": i,                 # Sampling order from 1..k
                "module_name": module_name,
                "schematic_name": schematic_name,
                "passed": int(bool(ev.get("passed", 0))),
                "errors": ev.get("errors", None),
                "netlist_evaluation": ev.get("netlist_evaluation", None),
            }
            results.append(rec)
            continue

        if isinstance(ev.get("errors", 0), int):
            total_errors += ev["errors"]

        # One Record
        rec = {
            "test_idx": i,                 # Sampling order from 1..k
            "module_name": module_name,
            "schematic_name": schematic_name,
            "passed": int(bool(ev.get("passed", 0))),
            "errors": ev.get("errors", None),
            "netlist_evaluation": ev.get("netlist_evaluation", None),
        }
        results.append(rec)

    # 5) Save results
    save_jsonl(out_jsonl, results)
    save_csv(out_csv, results)

    # 6) Summary
    print(f"  Passed: {passed_cnt}/{len(ds)}  ({passed_cnt / len(ds):.1%})")
    print(f"  Sum(errors): {total_errors}")
    print(f"  Results JSONL: {out_jsonl}")
    print(f"  Results CSV  : {out_csv}")

    return {
        "passed": passed_cnt,
        "sum_errors": total_errors,
        "out_jsonl": out_jsonl,
        "out_csv": out_csv,
        "results": results,
    }


if __name__ == "__main__":

    eval_path = Path(project_path) / "gptoss_training" / "new_eval_runs"
    for i in range(len(model_names)):
        run_batch_evaluation(jsonl_path = str(Path(project_path) / "jsonl_dataset" / "new_form" / f"finetune_dataset_sch_int_rl_medium.test.jsonl"), out_dir=eval_path, model_name=model_names[i])
