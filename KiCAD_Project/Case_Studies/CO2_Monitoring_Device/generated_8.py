# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 2 : Device:Q_NPN_BCE###

center_x_2, center_y_2 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Device", symbol_name="Q_NPN_BCE", pos_x=center_x_2, pos_y=center_y_2, reference="Q2", value="NPN", rotation=90, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 2###

add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_2 + (-2.54), pos_y=center_y_2 + (-13.97), reference="R2", value="10k", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_2 + (27.86), pos_y=center_y_2 + (-0.0), reference="R1", value="10k", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="Q_NPN_BCE", pos_x=center_x_2 + (29.21), pos_y=center_y_2 + (-13.97), reference="Q1", value="NPN", rotation=180, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label CH340-RTS next to R2 pin 1 
x_R2_1, y_R2_1 = get_pin_location(symbol_ref="R2", pin_name="1")
add_label(label_pos=[x_R2_1+(-7.62), y_R2_1+(0.0)], label_text="CH340-RTS", label_ref="CH340-RTS_0", label_type="input", text_orient="left")
# Connecting Label CH340-RTS label_id:0 to R2 pin 1 (Pin ID 1 -- Name 1)
connect_pins("CH340-RTS_0", "1", "R2", "1")

# Add label CH340-DTR next to R1 pin 1 
x_R1_1, y_R1_1 = get_pin_location(symbol_ref="R1", pin_name="1")
add_label(label_pos=[x_R1_1+(-7.62), y_R1_1+(0.0)], label_text="CH340-DTR", label_ref="CH340-DTR_0", label_type="input", text_orient="left")
# Connecting Label CH340-DTR label_id:0 to R1 pin 1 (Pin ID 1 -- Name 1)
connect_pins("CH340-DTR_0", "1", "R1", "1")

# Add label RESET next to Q1 pin C 
x_Q1_1, y_Q1_1 = get_pin_location(symbol_ref="Q1", pin_name="C")
add_label(label_pos=[x_Q1_1+(-6.35), y_Q1_1+(0.0)], label_text="RESET", label_ref="RESET_0", label_type="input", text_orient="left")
# Connecting Label RESET label_id:0 to Q1 pin C (Pin ID 1 -- Name C)
connect_pins("RESET_0", "1", "Q1", "C")

# Add label BOOT next to Q2 pin C 
x_Q2_1, y_Q2_1 = get_pin_location(symbol_ref="Q2", pin_name="C")
add_label(label_pos=[x_Q2_1+(-6.35), y_Q2_1+(0.0)], label_text="BOOT", label_ref="BOOT_0", label_type="input", text_orient="left")
# Connecting Label BOOT label_id:0 to Q2 pin C (Pin ID 1 -- Name C)
connect_pins("BOOT_0", "1", "Q2", "C")


### Connecting all wires in the Schematic ###


# Connecting R2 pin 2 (Pin ID 2 -- Name None) to Q2 pin B (Pin ID 2 -- Name B)
connect_pins("R2", "2", "Q2", "B")

# Connecting Q2 pin B (Pin ID 2 -- Name B) to R1 pin 2 (Pin ID 2 -- Name None)
connect_pins("Q1", "B", "R1", "2")

connect_pins("Q1", "E", "CH340-RTS_0", "1")

connect_pins("Q2", "E", "CH340-DTR_0", "1")


write_out_all_wires()