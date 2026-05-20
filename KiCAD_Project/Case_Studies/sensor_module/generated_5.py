# Prompt: I want an IMU with step counter and gesture detection. You MUST draw the clock line out with a label of SENSOR_CLK, and the data line out with a label of SENSOR_SDA. You need to draw two labels out for INT1 and INT2 as well.  Remember to add decoupling capacitors and there is no need for resistors.

# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : Sensor_Motion:ISM330DHCX###

center_x_1, center_y_1 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Sensor_Motion", symbol_name="ISM330DHCX", pos_x=center_x_1, pos_y=center_y_1, reference="U3", value="ISM330DHCX", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_1 + (-50.8), pos_y=center_y_1 + (-10.16), reference="C20", value="1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (-31.75), pos_y=center_y_1 + (25.4), reference="#PWR1", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (-31.75), pos_y=center_y_1 + (-22.86), reference="#PWR2", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (26.67), pos_y=center_y_1 + (25.4), reference="#PWR3", value="+3.3V", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label SENSOR_CLK next to U3 pin SCL 
x_U3_14, y_U3_14 = get_pin_location(symbol_ref="U3", pin_name="SCL")
add_label(label_pos=[x_U3_14+(-11.43), y_U3_14+(0)], label_text="SENSOR_CLK", label_ref="SENSOR_CLK_0", label_type="input", text_orient="left")
# Connecting Label SENSOR_CLK label_id:0 to U3 pin SCL (Pin ID 14 -- Name SCL)
connect_pins("SENSOR_CLK_0", "1", "U3", "SCL")

# Add label SENSOR_SDA next to U3 pin SDA
x_U3_15, y_U3_15 = get_pin_location(symbol_ref="U3", pin_name="SDA")
add_label(label_pos=[x_U3_15+(-11.43), y_U3_15+(0)], label_text="SENSOR_SDA", label_ref="SENSOR_SDA_0", label_type="input", text_orient="left")
# Connecting Label SENSOR_SDA label_id:0 to U3 pin SDA (Pin ID 15 -- Name SDA)
connect_pins("SENSOR_SDA_0", "1", "U3", "SDA")

# Add label INT2 next to U3 pin INT2 
x_U3_4, y_U3_4 = get_pin_location(symbol_ref="U3", pin_name="INT2")
add_label(label_pos=[x_U3_4+(-11.43), y_U3_4+(0)], label_text="IMU_INT2", label_ref="INT2_0", label_type="input", text_orient="left")
# Connecting Label INT2 label_id:0 to U3 pin INT2 (Pin ID 4 -- Name INT2)
connect_pins("INT2_0", "1", "U3", "INT2")

# Add label INT1 next to U3 pin INT1 
x_U3_3, y_U3_3 = get_pin_location(symbol_ref="U3", pin_name="INT1")
add_label(label_pos=[x_U3_3+(-20.32), y_U3_3+(0)], label_text="IMU_INT1", label_ref="INT1_0", label_type="input", text_orient="left")
# Connecting Label INT1 label_id:0 to U3 pin INT1 (Pin ID 3 -- Name INT1)
connect_pins("INT1_0", "1", "U3", "INT1")


### Connecting all wires in the Schematic ###


# Connecting #PWR3 pin +3.3V (Pin ID 1 -- Name +3.3V) to U3 pin VDD (Pin ID 16 -- Name VDD)
connect_pins("#PWR3", "+3.3V", "U3", "VDD")

# Connecting U3 pin VDDIO (Pin ID 1 -- Name VDDIO) to U3 pin VDD (Pin ID 16 -- Name VDD)
connect_pins("U3", "VDDIO", "U3", "VDD")

# Connecting #PWR2 pin 1 (Pin ID 1 -- Name None) to U3 pin 2 (Pin ID 2 -- Name None)
connect_pins("#PWR2", "1", "U3", "GND")

# Connecting #PWR1 pin +3.3V (Pin ID 1 -- Name +3.3V) to C20 pin 1 (Pin ID 1 -- Name None)
connect_pins("#PWR1", "+3.3V", "C20", "1")

# Connecting C20 pin 2 (Pin ID 2 -- Name None) to #PWR2 pin 1 (Pin ID 1 -- Name None)
connect_pins("C20", "2", "#PWR2", "1")

# Connecting C20 pin 1 (Pin ID 1 -- Name None) to #PWR1 pin +3.3V (Pin ID 1 -- Name +3.3V)
connect_pins("C20", "1", "#PWR1", "+3.3V")

connect_pins("U3", "CS", "#PWR3", "+3.3V")


write_out_all_wires()