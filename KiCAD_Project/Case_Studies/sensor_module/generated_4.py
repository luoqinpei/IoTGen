# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 5 : Sensor:BME680###

center_x_5, center_y_5 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Sensor", symbol_name="BME680", pos_x=center_x_5, pos_y=center_y_5, reference="U1", value="BME680", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 5###

add_schematic_symbol(symbol_lib="power", symbol_name="+3V3", pos_x=center_x_5 + (0.0), pos_y=center_y_5 + (31.75), reference="#PWR5", value="+3V3", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_5 + (0.0), pos_y=center_y_5 + (-20.32), reference="#PWR7", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label SENSOR_SDA next to U1 pin SDI 
x_U1_1_3, y_U1_1_3 = get_pin_location(symbol_ref="U1", pin_name="SDI")
add_label(label_pos=[x_U1_1_3+(2.54), y_U1_1_3+(0.0)], label_text="SENSOR_SDA", label_ref="SENSOR_SDA_1", label_type="input", text_orient="right")
# Connecting Label SENSOR_SDA label_id:1 to U1 pin SDI (Pin ID 3 -- Name SDI)
connect_pins("SENSOR_SDA_1", "1", "U1", "SDI")

# Add label SENSOR_SCK next to U1 pin SCK 
x_U1_1_4, y_U1_1_4 = get_pin_location(symbol_ref="U1", pin_name="SCK")
add_label(label_pos=[x_U1_1_4+(2.54), y_U1_1_4+(0.0)], label_text="SENSOR_SCK", label_ref="SENSOR_SCK_0", label_type="input", text_orient="right")
# Connecting Label SENSOR_SCK label_id:0 to U1 pin SCK (Pin ID 4 -- Name SCK)
connect_pins("SENSOR_SCK_0", "1", "U1", "SCK")


### Connecting all wires in the Schematic ###


# Connecting U1 pin 1 (Pin ID 1 -- Name None) to #PWR7 pin 1 (Pin ID 1 -- Name None)
connect_pins("U1", "1", "#PWR7", "1")

# Connecting U1 pin VDDIO (Pin ID 6 -- Name VDDIO) to #PWR5 pin +3V3 (Pin ID 1 -- Name +3V3)
connect_pins("U1", "VDDIO", "#PWR5", "+3V3")

# Connecting U1 pin 7 (Pin ID 7 -- Name None) to U1 pin 1 (Pin ID 1 -- Name None)
connect_pins("U1", "7", "U1", "1")

# Connecting U1_1 pin CSB (Pin ID 7 -- Name CSB) to U1 pin SDI (Pin ID 3 -- Name SDI)
connect_pins("U1", "CSB", "#PWR5", "+3V3")



write_out_all_wires()