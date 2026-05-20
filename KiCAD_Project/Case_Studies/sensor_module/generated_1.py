# Prompt to generate the schematic: I want a high-accuracy pressure sensor, using BMP280. You must draw out the clock line with a label of "SENSOR_SCK", and draw out the data line with a label of "SENSOR_SDA".

# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : Sensors:Sensor_Pressure###

center_x_1, center_y_1 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Sensor_Pressure", symbol_name="BMP280", pos_x=center_x_1, pos_y=center_y_1, reference="U1", value="BMP280", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_1 + (-8.89), pos_y=center_y_1 + (8.89), reference="C4", value="100nF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (0.0), pos_y=center_y_1 + (26.67), reference="#PWR_3V3", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (0.0), pos_y=center_y_1 + (-22.86), reference="#PWR_GND", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label SENSOR_SDA next to R4 pin 2 
x_U1_2, y_U1_2 = get_pin_location(symbol_ref="U1", pin_name="SDO")
add_label(label_pos=[x_U1_2+(-12.7), y_U1_2+(0.0)], label_text="SENSOR_SDA", label_ref="SENSOR_SDA_0", label_type="input", text_orient="left")
# Connecting Label SENSOR_SDA label_id:0 to R4 pin 2 (Pin ID 2 -- Name 2)
connect_pins("SENSOR_SDA_0", "1", "U1", "SDO")

# Add label SENSOR_SCK next to R3 pin 2 
x_U1_2, y_U1_2 = get_pin_location(symbol_ref="U1", pin_name="SCK")
add_label(label_pos=[x_U1_2+(-12.7), y_U1_2+(0.0)], label_text="SENSOR_SCK", label_ref="SENSOR_SCK_0", label_type="input", text_orient="left")
# Connecting Label SENSOR_SCK label_id:0 to R3 pin 2 (Pin ID 2 -- Name 2)
connect_pins("SENSOR_SCK_0", "1", "U1", "SCK")

### Connecting all wires in the Schematic ###



# Connecting U1 pin GND (Pin ID 6 -- Name GND) to #PWR_GND pin 1 (Pin ID 1 -- Name None)
connect_pins("U1", "GND", "#PWR_GND", "1")

# Connecting C4 pin 2 (Pin ID 2 -- Name None) to U1 pin 1 (Pin ID 1 -- Name None)
connect_pins("C4", "2", "#PWR_GND", "1")

# Connecting U1 pin VDD (Pin ID 8 -- Name VDD) to C4 pin 1 (Pin ID 1 -- Name None)
connect_pins("U1", "VDD", "C4", "1")

# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to U1 pin VDD (Pin ID 8 -- Name VDD)
connect_pins("#PWR_3V3", "+3.3V", "U1", "VDD")


write_out_all_wires()