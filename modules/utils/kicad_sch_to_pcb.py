'''
This module provides utilities to convert KiCad schematic files (.kicad_sch) to PCB files (.kicad_pcb) using the kicad-cli tool. It includes functions to find the kicad-cli executable, run it with appropriate arguments, and handle the conversion process. The main function demonstrates how to use these utilities to convert a schematic file to a PCB file.
'''
import subprocess, platform, shutil
from pathlib import Path
import os, sys
project_path = os.environ.get("PROJECT_PATH")
sys.path.append(project_path)

# -------- helpers --------
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

def _run(args):
    """Run kicad‑cli and raise if it fails."""
    subprocess.run([_find_kicad_cli(), *args], check=True)

def convert_sch_to_pcb(sch: str, pcb: str):
    """
    kicad-cli pcb update my_project.kicad_pcb --schematic my_project.kicad_sch
    """
    cmd = ["pcb", "update", str(pcb), "--schematic", str(sch)]  # :contentReference[oaicite:4]{index=4}
    _run(cmd)
    return Path(pcb)