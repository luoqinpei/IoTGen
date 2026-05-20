# Prompt: I want a light sensor, using APDS-9301. You MUST draw the clock line out with a label of SENSOR-SCK, and the data line out with a label of SENSOR_SDA. Note that there is NO NEED to use resistor.

# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : Sensor_Optical:APDS-9301###

center_x_1, center_y_1 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Sensor_Optical", symbol_name="APDS-9301", pos_x=center_x_1, pos_y=center_y_1, reference="U1", value="APDS-9301", rotation=0, mirror="y")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (0.0), pos_y=center_y_1 + (34.29), reference="#PWR_3V3", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (0.0), pos_y=center_y_1 + (-21.59), reference="#PWR_GND", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_1 + (0.0), pos_y=center_y_1 + (16.51), reference="C1", value="100nF", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label SENSOR-SCK next to U1 pin SCL 
x_U1_4, y_U1_4 = get_pin_location(symbol_ref="U1", pin_name="SCL")
add_label(label_pos=[x_U1_4+(7.62), y_U1_4+(0.0)], label_text="SENSOR_SCK", label_ref="SENSOR_SCK_0", label_type="input", text_orient="right")
# Connecting Label SENSOR-SCK label_id:0 to U1 pin SCL (Pin ID 4 -- Name SCL)
connect_pins("SENSOR_SCK_0", "1", "U1", "SCL")

# Add label SENSOR_SDA next to U1 pin SDA 
x_U1_5, y_U1_5 = get_pin_location(symbol_ref="U1", pin_name="SDA")
add_label(label_pos=[x_U1_5+(7.62), y_U1_5+(0.0)], label_text="SENSOR_SDA", label_ref="SENSOR_SDA_0", label_type="input", text_orient="right")
# Connecting Label SENSOR_SDA label_id:0 to U1 pin SDA (Pin ID 5 -- Name SDA)
connect_pins("SENSOR_SDA_0", "1", "U1", "SDA")


### Connecting all wires in the Schematic ###


# Connecting U1 pin 1 (Pin ID 1 -- Name None) to #PWR_GND pin 1 (Pin ID 1 -- Name None)
connect_pins("U1", "GND", "#PWR_GND", "1")

# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to C1 pin 1 (Pin ID 1 -- Name None)
connect_pins("#PWR_3V3", "1", "C1", "1")

# Connecting C1 pin 2 (Pin ID 2 -- Name None) to U1 pin VDD (Pin ID 6 -- Name VDD)
connect_pins("C1", "2", "U1", "VDD")

write_out_all_wires()