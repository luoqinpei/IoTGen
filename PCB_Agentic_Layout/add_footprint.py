'''
This script check the symbols in the schematic to see if they have footprints,
if not, it searches for the corresponding footprints in the KiCAD libraries and
adds them to the schematic.
'''


import os
import re
from pathlib import Path
import sys

project_path = os.environ.get("PROJECT_PATH")
if project_path is None:
    raise EnvironmentError("PROJECT_PATH environment variable is not set.")
sys.path.append(project_path)
from modules.kicad_sch_interface import get_fp


definite_location = 0 # Set to 1, use definite locations for all symbols
definite_wires = 0 # Set to 1, use definite locations for all symbols and wires

if definite_wires == 1:
    definite_location = 1

sch_pattern = re.compile(r"^sch_(\d+)_(\d+)\.kicad_sch$", re.IGNORECASE)
block_pattern = re.compile(r"^block[_\-]?\d+\.kicad_sch$", re.IGNORECASE)

DEBUG = False

if __name__ == "__main__":

    proj_path = Path(os.environ["PROJECT_PATH"])
    base_dir = proj_path / "dataset"

    if not base_dir.exists():
        raise FileNotFoundError(f"[Error] Base dir not found: {base_dir}")
    
    if DEBUG:
        # sch_path = BASE_DIR / "15335_9DoF_Schematic" / "block_0.kicad_sch"
        sch_path = Path("")
        print(f"\n---- [Debug] ----")
        fps = get_fp(str(sch_path))
        print(f"Footprints: {len(fps)}")
    else:
        total_files = 0
        ok_files = 0
        skipped_files = 0
        failed_files = 0

        for module_dir in sorted(p for p in base_dir.iterdir() if p.is_dir()):
            module_name = module_dir.name

            sch_path = module_dir / "module" / "module.kicad_sch"
            total_files += 1

            try:
                fps = get_fp(str(sch_path))
                print(f"✅ [{module_name}/{sch_path.name}] Footprints: {len(fps)}")
                ok_files += 1

            except Exception as e:
                failed_files += 1
                print(f"❌ [{module_name}/{sch_path.name}] Failed: {e}")

        print(
            f"\nSummary: total={total_files}, ok={ok_files}, skipped={skipped_files}, failed={failed_files}"
        )