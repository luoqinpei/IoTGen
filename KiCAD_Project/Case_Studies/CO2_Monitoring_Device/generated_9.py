# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : Connector:Micro_SD_Card###

center_x_1, center_y_1 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Connector", symbol_name="Micro_SD_Card", pos_x=center_x_1, pos_y=center_y_1, reference="J1", value="Micro_SD_Card", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (-24.32), pos_y=center_y_1 + (28.89), reference="#PWR_3V3", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (-24.32), pos_y=center_y_1 + (-28.89), reference="#PWR_GND", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_1 + (-28.32), pos_y=center_y_1 + (+20.16), reference="R1", value="10k", rotation=180, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_1 + (-32.32), pos_y=center_y_1 + (+20.16), reference="R2", value="10k", rotation=180, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_1 + (-35.32), pos_y=center_y_1 + (+20.16), reference="R3", value="10k", rotation=180, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_1 + (-38.94), pos_y=center_y_1 + (+20.16), reference="R4", value="10k", rotation=180, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_1 + (-44.7), pos_y=center_y_1 + (+20.16), reference="R5", value="10k", rotation=180, mirror="None")
### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label DAT1 next to J1 pin DAT1 
x_J1_8, y_J1_8 = get_pin_location(symbol_ref="J1", pin_name="DAT1")
add_label(label_pos=[x_J1_8+(-24.13), y_J1_8+(0.0)], label_text="DAT1", label_ref="DAT1_0", label_type="input", text_orient="left")
# Connecting Label DAT1 label_id:0 to J1 pin DAT1 (Pin ID 8 -- Name DAT1)
connect_pins("DAT1_0", "1", "J1", "DAT1")

# Add label DAT0 next to J1 pin DAT0 
x_J1_7, y_J1_7 = get_pin_location(symbol_ref="J1", pin_name="DAT0")
add_label(label_pos=[x_J1_7+(-24.13), y_J1_7+(0.0)], label_text="DAT0", label_ref="DAT0_0", label_type="input", text_orient="left")
# Connecting Label DAT0 label_id:0 to J1 pin DAT0 (Pin ID 7 -- Name DAT0)
connect_pins("DAT0_0", "1", "J1", "DAT0")

# Add label CLK next to J1 pin CLK 
x_J1_5, y_J1_5 = get_pin_location(symbol_ref="J1", pin_name="CLK")
add_label(label_pos=[x_J1_5+(-24.13), y_J1_5+(0.0)], label_text="CLK", label_ref="CLK_0", label_type="input", text_orient="left")
# Connecting Label CLK label_id:0 to J1 pin CLK (Pin ID 5 -- Name CLK)
connect_pins("CLK_0", "1", "J1", "CLK")

# Add label CMD next to J1 pin CMD 
x_J1_3, y_J1_3 = get_pin_location(symbol_ref="J1", pin_name="CMD")
add_label(label_pos=[x_J1_3+(-24.13), y_J1_3+(0.0)], label_text="CMD", label_ref="CMD_0", label_type="input", text_orient="left")
# Connecting Label CMD label_id:0 to J1 pin CMD (Pin ID 3 -- Name CMD)
connect_pins("CMD_0", "1", "J1", "CMD")

# Add label DAT2 next to J1 pin DAT2/CD 
x_J1_2, y_J1_2 = get_pin_location(symbol_ref="J1", pin_name="DAT2")
add_label(label_pos=[x_J1_2+(-24.13), y_J1_2+(0.0)], label_text="DAT2", label_ref="DAT2_0", label_type="input", text_orient="left")
# Connecting Label DAT2 label_id:0 to J1 pin DAT2/CD (Pin ID 2 -- Name DAT2/CD)
connect_pins("DAT2_0", "1", "J1", "DAT2")

x_J1_2, y_J1_2 = get_pin_location(symbol_ref="J1", pin_name="DAT3/CD")
add_label(label_pos=[x_J1_2+(-24.13), y_J1_2+(0.0)], label_text="DAT3", label_ref="DAT3_0", label_type="input", text_orient="left")
# Connecting Label DAT3 label_id:0 to J1 pin DAT3/CD (Pin ID 2 -- Name DAT3/CD)
connect_pins("DAT3_0", "1", "J1", "DAT3/CD")


### Connecting all wires in the Schematic ###


# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to J1 pin VDD (Pin ID 4 -- Name VDD)
connect_pins("#PWR_3V3", "+3.3V", "J1", "VDD")

# Connecting R3 pin 1 (Pin ID 1 -- Name None) to J1 pin DAT3/CD (Pin ID 2 -- Name DAT3/CD)
connect_pins("R3", "1", "J1", "DAT3/CD")
connect_pins("R3", "2", "#PWR_3V3", "1")

# Connecting J1 pin VDD (Pin ID 4 -- Name VDD) to R1 pin 1 (Pin ID 1 -- Name None)
connect_pins("J1", "DAT2", "R1", "1")
connect_pins("R1", "2", "#PWR_3V3", "1")

# Connecting R4 pin 1 (Pin ID 1 -- Name None) to J1 pin CMD (Pin ID 5 -- Name CLK)
connect_pins("R4", "1", "J1", "CMD")
connect_pins("R4", "2", "#PWR_3V3", "1")

# Connecting R2 pin 1 (Pin ID 1 -- Name None) to J1 pin DAT0 (Pin ID 3 -- Name DAT0)
connect_pins("R2", "1", "J1", "DAT0")
connect_pins("R2", "2", "#PWR_3V3", "1")

# Connecting R5 pin 1 (Pin ID 1 -- Name None) to J1 pin DAT1 (Pin ID 8 -- Name DAT1)
connect_pins("R5", "1", "J1", "DAT1")
connect_pins("R5", "2", "#PWR_3V3", "1")


connect_pins("J1", "VSS", "#PWR_GND", "1")

write_out_all_wires()