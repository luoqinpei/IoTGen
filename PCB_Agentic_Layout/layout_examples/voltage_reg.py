import os
import sys

project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)

from pathlib import Path
from PCB_Agentic_Layout.layout_api import layout_api

layout = layout_api()
layout.place_fp("U1", (100, 100), 0)
layout.place_fp("C1", (110, 105), 90)
layout.place_fp("C2", (110, 95), 90)
layout.auto_routing()
layout.save()