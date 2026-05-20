'''

'''

# Load the model
import torch
from pathlib import Path
import sys
import os
project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)
torch.manual_seed(42)
from transformers import Mxfp4Config
import re
from typing import Union
import argparse
import json

import sys as _sys
_argv_backup = _sys.argv[:]
_sys.argv = [_sys.argv[0]]

try:
    from make_dataset import prepare_context
    from datasets import load_dataset
    from modules.utils.kicad_scan_lib import (
        get_sym_context_with_cache, load_organized_lib, to_lib_name_tuples
    )
    from modules.sch_evaluation import extract_meta_info
finally:
    _sys.argv = _argv_backup

project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)

MAX_TOKENS = 13312

def save_final_python(decoded: str, out_path: Union[str, Path] = "generated.py") -> Path:
    """
    Extract the 'final' section from a decoded model output, strip trailing
    <|return|> markers and Markdown code fences, then save as a .py file.

    Parameters
    ----------
    decoded : str
        Full decoded text from the model (DO NOT skip special tokens before calling).
    out_path : str | Path, optional
        Destination .py path. Defaults to "./generated.py".

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

    # 4) Write to file
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(code_text, encoding="utf-8")

    return out_path

# Test Inference

# Load trained model
from transformers import AutoModelForCausalLM, AutoTokenizer, Mxfp4Config
from peft import PeftModel

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("openai/gpt-oss-20b")

# load a modified chat template from a file ({% generation %} and {% endgeneration %} addded for assistant_only_loss)
new_chat_template_path = Path(project_path) / "modified_chat_template.txt"
with new_chat_template_path.open("r", encoding="utf-8") as f:
    new_chat_template = f.read()

tokenizer.chat_template = new_chat_template


# Load the original model first
quantization_config = Mxfp4Config(dequantize=True)
model_kwargs = dict(attn_implementation="flash_attention_2", torch_dtype=torch.bfloat16, use_cache=False, device_map="cuda", quantization_config=quantization_config)
model = AutoModelForCausalLM.from_pretrained("openai/gpt-oss-20b", **model_kwargs)

# Merge fine-tuned weights with the base model
# peft_model_id = Path(project_path) / "models" / "gpt-oss-20b-pcb-finetune-L1"
# model = PeftModel.from_pretrained(base_model, peft_model_id)
# model = model.merge_and_unload()

# model.eval()

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Test model inference with raw request or dataset sample.")
    g = p.add_mutually_exclusive_group(required=True)  # Force user to choose one
    g.add_argument("--test_raw", action="store_true", help="Test with a raw user request.")
    g.add_argument("--test_dataset", type=str, help="Test with a sample from the dataset.")
    p.add_argument("--prompt", type=str, default="I would like to add a USB_B connector interface in the schematic, exporting two labels, namely D+ and D-. Make the schematic as simple as possible.", help="Optional prompt for --test_raw.")
    p.add_argument("--index", type=int, default=0, help="Sample index for --test_dataset.")
    p.add_argument("--debug", action="store_true", help="Enable debug mode.")
    return p

def run_raw_test(prompt: str | None):
    if prompt is None:
        prompt = input("Enter prompt: ")
    print(f"[RAW] prompt={prompt}")

    from sch_editor import SchematicEditor
    editor = SchematicEditor(model="o4")
    editor.sch_request = prompt
    editor.img_ref_path = None # Avoid trigger error

    msg_list = prepare_context(definite_wires=0)
    symbol_list, symbol_list_info = editor.load_related_symbols()
    symbol_list = to_lib_name_tuples(symbol_list)
    symbol_context = get_sym_context_with_cache(symbol_list, symbol_list_info, editor, Path(project_path) / ".cache" / "sym_contexts.sqlite")

    msg_list.append({"role": "user", 
                    "content": f"""
                    The user request is: {editor.sch_request}
                    ###
                        We have the following symbols and their related context information as listed below: {symbol_context}
                    ###
                        When determining the rotation and mirror of a symbol, REMEMBER to refer to the symbol information and compare it with the actual connections. When determining the connections, remember to refer to the pin location of symbols you have put on the schematic before.
                        Limit your thinking process less than 1000 words.
                    """})
    
    return msg_list

def run_dataset_sample_test(index: int, dataset: str):
    
    print(f"[DATASET] index={index}")
    ds = load_dataset("json", data_files={"train": dataset})["train"]
    msg_list = ds[index]["messages"][:2] # only take system and use msg as input.
    print("Loaded dataset sample messages:", msg_list[1])

    REASONING_LANGUAGE = "Spanish"
    SYSTEM_PROMPT = f"reasoning language: {REASONING_LANGUAGE}"
    USER_PROMPT = "What is the national symbol of Canada?"

    msg_list = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ]
    return msg_list

def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.debug:
        print("[DEBUG] mode on")

    if args.test_raw:
        msg_list = run_raw_test(args.prompt)
    else:
        msg_list = run_dataset_sample_test(args.index, args.test_dataset)

    # Apply Chat template
    input_ids = tokenizer.apply_chat_template(
        msg_list,
        add_generation_prompt=True,
        return_tensors="pt",
        reasoning_effort="high"
    ).to(model.device)

    # Test with trained model
    output_ids = model.generate(input_ids, max_new_tokens=MAX_TOKENS, attention_mask=torch.ones_like(input_ids))
    # Use newly-generated tokens only
    gen_only = output_ids[:, input_ids.shape[-1]:]
    response = tokenizer.batch_decode(gen_only, skip_special_tokens=False)[0]

    # Save as the python code
    path = save_final_python(response)

    print(response)
    print(f"Saved generated code to {path}")


if __name__ == "__main__":
    main()