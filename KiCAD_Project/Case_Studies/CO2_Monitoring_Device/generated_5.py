# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : Driver_LED:WS2811###

center_x_1, center_y_1 = 150.000, 110.000
add_schematic_symbol(symbol_lib="LED", symbol_name="WS2812B", pos_x=center_x_1, pos_y=center_y_1, reference="U1", value="WS2811", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="C_Small", pos_x=center_x_1 + (+17.62), pos_y=center_y_1 + (-22.86), reference="C5", value="2.2uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (-13.97), pos_y=center_y_1 + (6.35), reference="#PWR_3V3_U1", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (0.0), pos_y=center_y_1 + (-29.21), reference="#PWR_GND_U1", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label D1-PRO_0 next to U1 pin DIN 
x_U1_6, y_U1_6 = get_pin_location(symbol_ref="U1", pin_name="DIN")
add_label(label_pos=[x_U1_6+(-16.51), y_U1_6+(0.0)], label_text="LED", label_ref="LED_0", label_type="input", text_orient="left")
# Connecting Label D1-PRO_0 label_id:0 to U1 pin DIN (Pin ID 6 -- Name DIN)
connect_pins("LED_0", "1", "U1", "DIN")


### Connecting all wires in the Schematic ###


# Connecting C5 pin 2 (Pin ID 2 -- Name None) to #PWR_GND_U1 pin 1 (Pin ID 1 -- Name None)
connect_pins("C5", "2", "#PWR_GND_U1", "1")

# Connecting #PWR_3V3_U1 pin +3.3V (Pin ID 1 -- Name +3.3V) to U1 pin VDD (Pin ID 8 -- Name VDD)
connect_pins("#PWR_3V3_U1", "+3.3V", "U1", "VDD")

# Connecting U1 pin VSS (Pin ID 4 -- Name VSS) to #PWR_GND_U1 pin 1 (Pin ID 1 -- Name None)
connect_pins("U1", "VSS", "#PWR_GND_U1", "1")

# Connecting C5 pin 1 (Pin ID 1 -- Name None) to U1 pin VDD (Pin ID 8 -- Name VDD)
connect_pins("C5", "1", "U1", "VDD")


write_out_all_wires()