# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : Sensors:Sensor_Gas###

center_x_1, center_y_1 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Sensor_Gas", symbol_name="SCD40-D-R2", pos_x=center_x_1, pos_y=center_y_1, reference="U1", value="SCD40-D-R2", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_1 + (+15.21), pos_y=center_y_1 + (12.62), reference="R11", value="4.7k", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_1 + (+21.21), pos_y=center_y_1 + (12.62), reference="R22", value="4.7k", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_1 + (-21.59), pos_y=center_y_1 + (-7.62), reference="C1", value="0.1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (-21.59), pos_y=center_y_1 + (19.05), reference="#PWR_3V3", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (-21.59), pos_y=center_y_1 + (-26.67), reference="#PWR_GND", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label I2C_SDA{slash}SDI next to R22 pin 1 
x_R22_1, y_R22_1 = get_pin_location(symbol_ref="U1", pin_name="SDA")
add_label(label_pos=[x_R22_1+(12.89), y_R22_1+(0.0)], label_text="I2C_SDA{slash}SDI", label_ref="I2C_SDA{slash}SDI_0", label_type="input", text_orient="right")
# Connecting Label I2C_SDA{slash}SDI label_id:0 to R22 pin 1 (Pin ID 1 -- Name 1)
connect_pins("I2C_SDA{slash}SDI_0", "1", "U1", "SDA")

# Add label I2C_SCL{slash}SDO next to R11 pin 1 
x_R11_1, y_R11_1 = get_pin_location(symbol_ref="U1", pin_name="SCL")
add_label(label_pos=[x_R11_1+(12.89), y_R11_1+(0.0)], label_text="I2C_SCL{slash}SDO", label_ref="I2C_SCL{slash}SDO_0", label_type="input", text_orient="right")
# Connecting Label I2C_SCL{slash}SDO label_id:0 to R11 pin 1 (Pin ID 1 -- Name 1)
connect_pins("I2C_SCL{slash}SDO_0", "1", "U1", "SCL")

### Connecting all wires in the Schematic ###


# Connecting C1 pin 2 (Pin ID 2 -- Name None) to #PWR_GND pin 1 (Pin ID 1 -- Name None)
connect_pins("C1", "2", "#PWR_GND", "1")

connect_pins("#PWR_GND", "1", "U1", "GND")

# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to U1 pin VDD (Pin ID 2 -- Name VDD)
connect_pins("#PWR_3V3", "+3.3V", "U1", "VDD")

# Connecting R11 pin 2 (Pin ID 2 -- Name None) to U1 pin SCL (Pin ID 4 -- Name SCL)
connect_pins("R11", "2", "I2C_SCL{slash}SDO_0", "1")

# Connecting R22 pin 2 (Pin ID 2 -- Name None) to U1 pin SDA (Pin ID 3 -- Name SDA)
connect_pins("R22", "2", "U1", "SDA")

# Connecting C1 pin 1 (Pin ID 1 -- Name None) to #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V)
connect_pins("C1", "1", "#PWR_3V3", "+3.3V")

# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to R11 pin 1 (Pin ID 1 -- Name None)
connect_pins("#PWR_3V3", "+3.3V", "R11", "1")

# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to R22 pin 1 (Pin ID 1 -- Name None)
connect_pins("#PWR_3V3", "+3.3V", "R22", "1")


write_out_all_wires()