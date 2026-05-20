# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *
set_schematic_filename(r"")
### Placing center symbol 1 : Device:R###

center_x_1, center_y_1 = 150.0, 110.0

add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_1, pos_y=center_y_1, reference="R1", value="2.2K", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="power", symbol_name="+3V3", pos_x=center_x_1 + (0), pos_y=center_y_1 + (13), reference="#PWR3V1", value="+3V3", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="LED", pos_x=center_x_1 + (0), pos_y=center_y_1 + (-7), reference="D1", value="LED", rotation=90, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (0), pos_y=center_y_1 + (-15), reference="#PWR2", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###


### Connecting all wires in the Schematic ###


# Connecting R1 pin 2 (Pin ID 2 -- Name None) to D1 pin A1 (Pin ID 2 -- Name A)
connect_pins("R1", "2", "D1", "A")

# Connecting D1 pin A2 (Pin ID 1 -- Name K) to #PWR2 pin 1 (Pin ID 1 -- Name None)
connect_pins("D1", "K", "#PWR2", "1")

# Connecting #PWR3V1 pin +3V3 (Pin ID 1 -- Name +3V3) to R1 pin 1 (Pin ID 1 -- Name None)
connect_pins("#PWR3V1", "+3V3", "R1", "1")

write_out_all_wires()