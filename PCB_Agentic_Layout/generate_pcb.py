#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Automatically generate PCB files from KiCAD schematic files using the kicad-cli and netlist_to_skidl tools.
# For each schematic file (sch_*.kicad_sch), the script exports a netlist, converts it to skidl code, appends a call to generate_pcb() in the generated main.py, and runs it to produce a .kicad_pcb file. The script also keeps track of processed files and handles errors gracefully, providing a summary of the results at the end. This automation streamlines the workflow of converting schematics to PCB layouts, ensuring consistency and efficiency in the PCB generation process.
'''

import os
import re, pathlib
import sys
import shlex
import subprocess, platform, shutil
from pathlib import Path
from typing import Optional
import argparse

project_path = os.environ.get("PROJECT_PATH")
if project_path is None:
    raise EnvironmentError("PROJECT_PATH environment variable is not set.\n Use export PROJECT_PATH=")
sys.path.append(project_path)

from config import KICAD_SYMBOL_LIB_PATH, KICAD_FOOTPRINT_LIB_PATH

definite_location = 0# Set to 1, use definite locations for all symbols
definite_wires = 0 # Set to 1, use definite locations for all symbols and wires

if definite_wires == 1:
    definite_location = 1

# schematic pattern match
SCH_PATTERN = re.compile(r"^sch_(\d+)_(\d+)\.kicad_sch$", re.IGNORECASE)
BLOCK_PATTERN = re.compile(r"^block[_\-]?\d+\.kicad_sch$", re.IGNORECASE)

BASE_DIR = Path(project_path) / "dataset"

def sanitize_sexp_netlist(path):
    p = pathlib.Path(path)
    txt = p.read_text(encoding="utf-8")
    # Ensure all (property (name "...") ...) have a (value "...")
    txt2 = re.sub(
        r'\(property\s+\(name\s+"([^"]+)"\)\s*\)',
        r'(property (name "\1") (value ""))',
        txt
    )
    if txt2 != txt:
        p.write_text(txt2, encoding="utf-8")
        return True
    return False

def _find_kicad_cli() -> str:
    """
    Return the full path to kicad-cli, or just 'kicad-cli' if it’s on PATH.
    Adjusts for typical install dirs on macOS and Windows.
    """
    exe = "kicad-cli.exe" if platform.system() == "Windows" else "kicad-cli"
    cli = shutil.which(exe)
    if cli:
        return cli

    if platform.system() == "Darwin":   # macOS default bundle path
        return "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"  # :contentReference[oaicite:0]{index=0}
    else:                               # Windows default
        return r"C:\Program Files\KiCad\8.0\bin\kicad-cli.exe"

from typing import Optional, Union, Sequence


def run(
    cmd: Union[str, Sequence[str]],
    cwd: Optional[Path] = None,
    timeout: Optional[int] = None,
):
    """Run a command in a subprocess. Supports both string and list commands."""
    print(f"▶ {cmd} (cwd={cwd})")

    if isinstance(cmd, str):
        cmd_args = shlex.split(cmd)
    else:
        cmd_args = [str(x) for x in cmd]

    res = subprocess.run(
        cmd_args,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout,
        check=False,
    )

    if res.returncode != 0:
        print(res.stdout)
        raise RuntimeError(f"Command failed with code {res.returncode}: {cmd}")

    if res.stdout.strip():
        print(res.stdout)

    return res.stdout


def ensure_generate_pcb_line(main_py: Path, pcb_path: Path, fp_libs: str):
    """If main.py does not already contain generate_pcb(...), append it."""
    line = (
        f'generate_pcb(file_="{str(pcb_path)}",'
        f'fp_libs="{fp_libs}")\n'
    )
    txt = main_py.read_text(encoding="utf-8", errors="ignore")
    if "generate_pcb(" in txt:
        return False
    with main_py.open("a", encoding="utf-8") as f:
        f.write("\n" + line)
    return True


def export_netlist(sch, out_file, pages=None):
    """Use KiCad's sch command to export a schematic to a netlist file."""
    cmd = [_find_kicad_cli(), "sch", "export", "netlist", str(sch), "-o", str(out_file)]
    if pages:
        cmd += ["--pages", pages]
    run(" ".join(shlex.quote(c) for c in cmd))
    return Path(out_file)


def process_one_sch(sch_path: Path, fp_libs: str) -> str:
    """
    For one sch_*.kicad_sch file, do the following:
      1) export_netlist -> .net
      2) netlist_to_skidl -> skidl files (in subdir <stem>)
      3) Append generate_pcb(...)
      4) run main.py to generate .kicad_pcb
    return "ok"/"skipped"
    """
    stem = sch_path.stem  # e.g., sch_0_0
    module_dir = sch_path.parent

    if sch_path.name.endswith("_out.kicad_sch"):
        return "skipped"

    # 1) export netlist
    net_file = module_dir / f"{stem}.net"
    export_netlist(sch_path, net_file)

    # Sanitize the netlist to ensure all properties have values
    sanitize_sexp_netlist(net_file)
    # 2) generate skidl files (in subdir <stem>)
    out_dir = module_dir / stem
    cmd = f"netlist_to_skidl -i {shlex.quote(str(net_file))} -o {shlex.quote(stem)} -w"
    run(cmd, cwd=module_dir)

    # 3) Append generate_pcb(...) (if not already present)
    main_py = out_dir / "main.py"
    if not main_py.exists():
        raise FileNotFoundError(f"Not Found {main_py}, check netlist_to_skidl step?")

    pcb_out = module_dir / f"{stem}.kicad_pcb" 
    appended = ensure_generate_pcb_line(main_py, pcb_out, fp_libs)
    if appended:
        print(f"✓ Append generate_pcb(...) to {main_py.name}")

    # 4) run main.py to generate .kicad_pcb
    #    Use the same Python interpreter, set cwd to the subdir to ensure relative imports/paths work
    run(f"{shlex.quote(sys.executable)} {shlex.quote(str(main_py))}", cwd=out_dir)

    if pcb_out.exists():
        print(f"✅ Generated PCB: {pcb_out}")
        return "ok"
    else:
        raise RuntimeError(f"Not Found PCB file: {pcb_out}")
    
import json
def load_processed_modules(jsonl_path):
    """Load existing modules from OUTPUT_JSONL."""
    processed = set()
    if not os.path.exists(jsonl_path):
        print(f"[Info] No existing JSONL file found at {jsonl_path}. Starting fresh.")
        return processed

    with open(jsonl_path, "r", encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if "module_dir" in data:
                    processed.add(data["module_dir"] + "/" + data["module"])
            except:
                pass  # ignore malformed lines

    return processed

DEBUG = False
REFERENCE_JSONL = os.path.join(project_path, "pcb_layout", "layout_scores.jsonl")

def main():


    if not BASE_DIR.exists():
        print(f"[Error] Base dir not found: {BASE_DIR}")
        sys.exit(1)

    print(f"[Info] PROJECT_PATH = {project_path}")
    print(f"[Info] BASE_DIR     = {BASE_DIR}")
    print(f"[Info] FP_LIBS      = {KICAD_FOOTPRINT_LIB_PATH}")

    total_files = 0
    ok_files = 0
    skipped_files = 0
    failed_files = 0
    processed = load_processed_modules(REFERENCE_JSONL)
    if DEBUG:
        # sch_path = BASE_DIR / "15335_9DoF_Schematic" / "block_0.kicad_sch"
        sch_path = Path("")
        print(f"\n---- [Debug] ----")
        try:
            status = process_one_sch(sch_path, KICAD_FOOTPRINT_LIB_PATH)
            print(f"Status: {status}")
        except Exception as e:
            print(f"❌ Failed: {e}")
    else:
        flag = 1
        for module_dir in sorted(p for p in BASE_DIR.iterdir() if p.is_dir()):
            if (str(module_dir.stem) + "/" + "module") not in processed:
                print(f"[SKIP not already processed] {module_dir.stem}")
                continue
            module_name = module_dir.name
            sch_path = module_dir / "module" / "module.kicad_sch"
            total_files += 1
            print(f"\n---- [{module_name}/{sch_path.name}] ----")
            try:
                status = process_one_sch(sch_path, KICAD_FOOTPRINT_LIB_PATH)
                if status == "ok":
                    ok_files += 1
                elif status == "skipped":
                    skipped_files += 1
                else:
                    failed_files += 1
            except Exception as e:
                failed_files += 1
                print(f"❌ Failed: {e}")

        print(
            f"\nSummary: total={total_files}, ok={ok_files}, "
            f"skipped={skipped_files}, failed={failed_files}"
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("sch_path", type=Path)
    parser.add_argument("footprint_lib_path", type=str)
    args = parser.parse_args()

    process_one_sch(args.sch_path, args.footprint_lib_path)