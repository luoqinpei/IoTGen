# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 2 : Switch:SW_SPST###

center_x_2, center_y_2 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Switch", symbol_name="SW_SPST", pos_x=center_x_2, pos_y=center_y_2, reference="SW2", value="OFF", rotation=90, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 2###

add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_2 + (0.0), pos_y=center_y_2 + (-10.16), reference="#GND1", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Switch", symbol_name="SW_SPST", pos_x=center_x_2 + (22.86), pos_y=center_y_2 + (2.54), reference="SW1", value="OFF", rotation=90, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_2 + (22.86), pos_y=center_y_2 + (-7.62), reference="#GND2", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label BOOT next to SW1 pin B 
x_SW1_2, y_SW1_2 = get_pin_location(symbol_ref="SW1", pin_name="B")
add_label(label_pos=[x_SW1_2+(10.16), y_SW1_2+(0.0)], label_text="BOOT", label_ref="BOOT_0", label_type="input", text_orient="right")
# Connecting Label BOOT label_id:0 to SW1 pin B (Pin ID 2 -- Name B)
connect_pins("BOOT_0", "1", "SW1", "B")

# Add label RESET next to SW2 pin B 
x_SW2_2, y_SW2_2 = get_pin_location(symbol_ref="SW2", pin_name="B")
add_label(label_pos=[x_SW2_2+(27.94), y_SW2_2+(0.0)], label_text="RESET", label_ref="RESET_0", label_type="input", text_orient="right")
# Connecting Label RESET label_id:0 to SW2 pin B (Pin ID 2 -- Name B)
connect_pins("RESET_0", "1", "SW2", "B")


### Connecting all wires in the Schematic ###


# Connecting SW2 pin A (Pin ID 1 -- Name A) to #GND1 pin 1 (Pin ID 1 -- Name None)
connect_pins("SW2", "A", "#GND1", "1")

# Connecting SW1 pin A (Pin ID 1 -- Name A) to #GND2 pin 1 (Pin ID 1 -- Name None)
connect_pins("SW1", "A", "#GND2", "1")


write_out_all_wires()