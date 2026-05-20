# Prompt: I want an Magnetometer module. You MUST draw the clock line out with a label of SENSOR_CLK, and the data line out with a label of SENSOR_SDA. You need to draw the label of INT out as well (name the label after the chip name).  Remember to add decoupling capacitors and there is no need for resistors.

# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : Sensor_Magnetic:LIS3MDL###

center_x_1, center_y_1 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Sensor_Magnetic", symbol_name="LIS3MDL", pos_x=center_x_1, pos_y=center_y_1, reference="U1", value="LIS3MDL", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="C_Small", pos_x=center_x_1 + (-17.78), pos_y=center_y_1 + (-15.24), reference="C1", value="0.1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (2.54), pos_y=center_y_1 + (31.75), reference="#PWR1", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (2.54), pos_y=center_y_1 + (-21.59), reference="#PWR2", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C_Small", pos_x=center_x_1 + (2.54), pos_y=center_y_1 + (-15.24), reference="C2", value="0.1uF", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label SENSOR_CLK next to U1 pin SCL/SPC 
x_U1_1, y_U1_1 = get_pin_location(symbol_ref="U1", pin_name="SCL/SPC")
add_label(label_pos=[x_U1_1+(-6.35), y_U1_1+(0.0)], label_text="SENSOR_CLK", label_ref="SENSOR_CLK_0", label_type="input", text_orient="left")
# Connecting Label SENSOR_CLK label_id:0 to U1 pin SCL/SPC (Pin ID 1 -- Name SCL/SPC)
connect_pins("SENSOR_CLK_0", "1", "U1", "SCL/SPC")

# Add label SENSOR_SDA next to U1 pin SDA/SDI/SDO 
x_U1_11, y_U1_11 = get_pin_location(symbol_ref="U1", pin_name="SDA/SDI/SDO")
add_label(label_pos=[x_U1_11+(-6.35), y_U1_11+(0.0)], label_text="SENSOR_SDA", label_ref="SENSOR_SDA_0", label_type="input", text_orient="left")
# Connecting Label SENSOR_SDA label_id:0 to U1 pin SDA/SDI/SDO (Pin ID 11 -- Name SDA/SDI/SDO)
connect_pins("SENSOR_SDA_0", "1", "U1", "SDA/SDI/SDO")

x_U1_7, y_U1_7 = get_pin_location(symbol_ref="U1", pin_name="INT")
add_label(label_pos=[x_U1_7+(2.54), y_U1_7+(0.0)], label_text="Mag_INT", label_ref="Mag_INT_0", label_type="output", text_orient="right")
# Connecting Label Mag_INT label_id:0 to U1 pin INT (Pin ID 7 -- Name INT)
connect_pins("Mag_INT_0", "1", "U1", "INT")


### Connecting all wires in the Schematic ###


# Connecting #PWR1 pin +3.3V (Pin ID 1 -- Name +3.3V) to U1 pin Vdd (Pin ID 5 -- Name Vdd)
connect_pins("#PWR1", "+3.3V", "U1", "Vdd")

# Connecting #PWR2 pin GND (Pin ID 1 -- Name GND) to U1 pin GND (Pin ID 10 -- Name GND)
connect_pins("C2", "2", "#PWR2", "1")

# Connecting C2 pin 1 (Pin ID 1 -- Name None) to U1 pin Vdd_IO (Pin ID 6 -- Name Vdd_IO)
connect_pins("C2", "1", "U1", "Vdd_IO")

# Connecting U1 pin Vdd_IO (Pin ID 6 -- Name Vdd_IO) to U1 pin Vdd (Pin ID 5 -- Name Vdd)
connect_pins("U1", "Vdd", "U1", "Vdd_IO")

# Connecting #PWR2 pin GND (Pin ID 1 -- Name GND) to C1 pin 2 (Pin ID 2 -- Name None)
connect_pins("C1", "2", "#PWR2", "1")

# Connecting C1 pin 1 (Pin ID 1 -- Name None) to U1 pin Vdd (Pin ID 5 -- Name Vdd)
connect_pins("C1", "1", "U1", "Vdd")

# Connecting #PWR2 pin 1 (Pin ID 1 -- Name None) to U1 pin 10 (Pin ID 10 -- Name GND)
connect_pins("#PWR2", "1", "U1", "GND")



write_out_all_wires()