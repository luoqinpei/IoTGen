# Prompt: I want a microphone, using SPH0641LU4H-1. You MUST draw the clock line out with a label of MIC-CLK, and the data line out with a label of MIC-DATA.

# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 2 : Sensor_Audio:SPH0641LU4H-1###

center_x_2, center_y_2 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Sensor_Audio", symbol_name="SPH0641LU4H-1", pos_x=center_x_2, pos_y=center_y_2, reference="U5", value="SPH0641LU4H-1", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 2###

add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_2 + (-11.43), pos_y=center_y_2 + (11.43), reference="#PWR1", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_2 + (0.0), pos_y=center_y_2 + (-11.43), reference="#PWR_2", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label MIC-CLK next to U5 pin CLOCK 
x_U5_4, y_U5_4 = get_pin_location(symbol_ref="U5", pin_name="CLOCK")
add_label(label_pos=[x_U5_4+(11.43), y_U5_4+(0.0)], label_text="MIC-CLK", label_ref="MIC-CLK_0", label_type="input", text_orient="right")
# Connecting Label MIC-CLK label_id:0 to U5 pin CLOCK (Pin ID 4 -- Name CLOCK)
connect_pins("MIC-CLK_0", "1", "U5", "CLOCK")

# Add label MIC-DATA next to U5 pin DATA 
x_U5_3, y_U5_3 = get_pin_location(symbol_ref="U5", pin_name="DATA")
add_label(label_pos=[x_U5_3+(11.43), y_U5_3+(0.0)], label_text="MIC-DATA", label_ref="MIC-DATA_0", label_type="input", text_orient="right")
# Connecting Label MIC-DATA label_id:0 to U5 pin DATA (Pin ID 3 -- Name DATA)
connect_pins("MIC-DATA_0", "1", "U5", "DATA")


### Connecting all wires in the Schematic ###


# Connecting U5 pin 6 (Pin ID 6 -- Name None) to #PWR_2 pin 1 (Pin ID 1 -- Name None)
connect_pins("U5", "GND", "#PWR_2", "1")

# Connecting #PWR1 pin +3.3V (Pin ID 1 -- Name +3.3V) to U5 pin VDD (Pin ID 5 -- Name VDD)
connect_pins("#PWR1", "+3.3V", "U5", "VDD")


write_out_all_wires()