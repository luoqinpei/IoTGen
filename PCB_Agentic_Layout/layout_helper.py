'''
Helper functions for PCB layout operations.
This module provides utility functions to interact with KiCAD PCB files using the pcbnew Python API. It includes functions to read PCB files, extract information about tracks, vias, footprints, zones, and netclasses, and perform operations such as auto-routing and clearing wiring. The functions are designed to be used in conjunction with the layout_api for more complex PCB manipulation tasks.
It also solves the problems of heterogeneous environments and dependencies by running the pcbnew API code in a subprocess, allowing for better isolation and error handling when working with KiCAD PCB files.
'''

import subprocess
import ast
from pathlib import Path
import re

import os, sys
project_path = os.environ.get("PROJECT_PATH")
sys.path.append(project_path)
layout_api_path = Path(project_path) / "pcb_layout"
from config import pcbnew_path

_IGNORES = [
    re.compile(r".*stdpbase\.cpp\(\d+\): assert .*create wxApp before calling this.*", re.I),
    re.compile(r'.*assert\s+"?traits"?\s+failed.*create wxApp before calling this.*', re.I),
    re.compile(r".*create wxApp before calling this.*", re.I),
]

def _filter_noise_lines(text: str) -> list[str]:
    lines = [ln.strip() for ln in text.splitlines()]
    kept = []
    for ln in lines:
        if not ln:
            continue
        if any(p.search(ln) for p in _IGNORES):
            continue
        kept.append(ln)
    return kept

def get_layout_lib_info(pcb_filename: str,
                        pcbnew_path: str = pcbnew_path,
                        timeout: int = 180):
    """
        from PCB_Agentic_Layout.layout_api import layout_api, set_pcb_path
        layout = layout_api(pcb_filename)
        lib_info = layout.layout.get_all_lib_info()
        print(lib_info)
    """

    pcb_path = Path(pcb_filename).resolve()

    if not pcb_path.exists():
        return {"ok": False, "stderr": f"PCB file not found: {pcb_path}"}
    if not pcb_path.is_file():
        return {"ok": False, "stderr": f"Path is not a file: {pcb_path}"}
    try:
        with open(pcb_path, "rb"):
            pass
    except OSError as e:
        return {"ok": False, "stderr": f"Cannot read PCB file: {pcb_path}", "oserror": str(e)}
    code = f"""
import os
import sys
project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)
sys.path.append(r'''{layout_api_path}''')
from PCB_Agentic_Layout.layout_api import layout_api
layout = layout_api(r'''{pcb_filename}''')
lib_info = layout.get_all_lib_info()
print(lib_info)
""".lstrip()

    proc = subprocess.run(
        [pcbnew_path, "-c", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )

    raw_out = proc.stdout.decode("utf-8", errors="ignore")
    raw_err = proc.stderr.decode("utf-8", errors="ignore")

    # 
    out_lines = _filter_noise_lines(raw_out)
    err_lines = _filter_noise_lines(raw_err)

    #  stdout ， stderr；
    payload_line = (out_lines or err_lines)[-1] if (out_lines or err_lines) else ""

    parsed = None
    if payload_line:
        try:
            parsed = ast.literal_eval(payload_line)
        except Exception:
            parsed = None  # （ __repr__），

    print("Layout lib info payload:", payload_line)
    return {
        "ok": bool(payload_line),
        "content": payload_line,
        "data": parsed,
    }

def auto_wiring_score(pcb_filename: str,
                        pcbnew_path: str = pcbnew_path,
                        timeout: int = 120):
    """
        from PCB_Agentic_Layout.layout_api import layout_api, set_pcb_path
        layout = layout_api(pcb_filename)
        lib_info = layout.layout.get_all_lib_info()
        print(lib_info)
    """

    pcb_path = Path(pcb_filename).resolve()

    if not pcb_path.exists():
        return {"ok": False, "stderr": f"PCB file not found: {pcb_path}"}
    if not pcb_path.is_file():
        return {"ok": False, "stderr": f"Path is not a file: {pcb_path}"}
    try:
        with open(pcb_path, "rb"):
            pass
    except OSError as e:
        return {"ok": False, "stderr": f"Cannot read PCB file: {pcb_path}", "oserror": str(e)}
    code = f"""
import os
import sys
project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)
sys.path.append(r'''{layout_api_path}''')
from PCB_Agentic_Layout.layout_api import layout_api
layout = layout_api(r'''{pcb_filename}''')
layout.auto_routing()
""".lstrip()
    
    try:
        proc = subprocess.run(
            [pcbnew_path, "-c", code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        # Timeout, return score 0
        return 0
    

    raw_out = proc.stdout.decode("utf-8", errors="ignore")
    print(raw_out)
    
    m = re.search(r"score of ([0-9.]+)", raw_out)
    score = float(m.group(1).rstrip(".")) if m else None
    return {"ok": True, "score": score}

def clear_wiring(pcb_filename: str, pcb_new_path: str = pcbnew_path, timeout: int = 180):

    pcb_path = Path(pcb_filename).resolve()

    if not pcb_path.exists():
        return {"ok": False, "stderr": f"PCB file not found: {pcb_path}"}
    if not pcb_path.is_file():
        return {"ok": False, "stderr": f"Path is not a file: {pcb_path}"}
    try:
        with open(pcb_path, "rb"):
            pass
    except OSError as e:
        return {"ok": False, "stderr": f"Cannot read PCB file: {pcb_path}", "oserror": str(e)}
    code = f"""
import os
import sys
project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)
sys.path.append(r'''{layout_api_path}''')
from PCB_Agentic_Layout.layout_api import layout_api
layout = layout_api(r'''{pcb_filename}''')
layout.clear_wiring()
layout.save()
""".lstrip()

    proc = subprocess.run(
        [pcbnew_path, "-c", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )

    return 