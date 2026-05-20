# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : Connector:USB_C_Receptacle###

center_x_1, center_y_1 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Connector", symbol_name="USB_C_Plug_USB2.0", pos_x=center_x_1, pos_y=center_y_1, reference="P1", value="USB_C_Receptacle", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_1 + (14.60), pos_y=center_y_1 + (-31.75), reference="R1", value="5.1k", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (10.16), pos_y=center_y_1 + (-40.64), reference="#PWR1", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="VCC", pos_x=center_x_1 + (14.60), pos_y=center_y_1 + (31.75), reference="#PWR2", value="V_USB", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label D-_1 next to P1 pin D- 
x_P1_A7, y_P1_A7 = get_pin_location(symbol_ref="P1", pin_name="D-")
add_label(label_pos=[x_P1_A7+(-12.7), y_P1_A7+(0.0)], label_text="D-_1", label_ref="D-_1_1", label_type="input", text_orient="left")
# Connecting Label D-_1 label_id:1 to P1 pin D- (Pin ID A7 -- Name D-)
connect_pins("D-_1_1", "1", "P1", "D-")

# Add label D+_1 next to P1 pin D+ 
x_P1_A6, y_P1_A6 = get_pin_location(symbol_ref="P1", pin_name="D+")
add_label(label_pos=[x_P1_A6+(-12.7), y_P1_A6+(0.0)], label_text="D+_1", label_ref="D+_1_0", label_type="input", text_orient="left")
# Connecting Label D+_1 label_id:0 to P1 pin D+ (Pin ID A6 -- Name D+)
connect_pins("D+_1_0", "1", "P1", "D+")


### Connecting all wires in the Schematic ###


# Connecting R1 pin 2 (Pin ID 2 -- Name None) to #PWR1 pin 1 (Pin ID 1 -- Name None)
connect_pins("R1", "2", "#PWR1", "1")

# Connecting P1 pin CC (Pin ID A5 -- Name CC) to R1 pin 1 (Pin ID 1 -- Name None)
connect_pins("P1", "CC", "R1", "1")

connect_pins("P1", "GND", "#PWR1", "1")

connect_pins("P1", "VBUS", "#PWR2", "1")

write_out_all_wires()