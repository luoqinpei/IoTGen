# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : Regulator_Linear:AP2112K-3.3###

center_x_1, center_y_1 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Regulator_Linear", symbol_name="AP2112K-3.3", pos_x=center_x_1, pos_y=center_y_1, reference="U1", value="AP2112K-3.3", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="power", symbol_name="VCC", pos_x=center_x_1 + (-36.83), pos_y=center_y_1 + (7.62), reference="#PWR5V", value="V_USB", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (10.16), pos_y=center_y_1 + (1.27), reference="#PWR33V", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (0.00), pos_y=center_y_1 + (-10.36), reference="#PWRGND", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="D_TVS", pos_x=center_x_1 + (-17.78), pos_y=center_y_1 + (-2.54), reference="D_VIN", value="~", rotation=270, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_1 + (-10.35), pos_y=center_y_1 + (-3.81), reference="C2", value="1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_1 + (12.54), pos_y=center_y_1 + (-3.81), reference="C3", value="1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_1 + (20.08), pos_y=center_y_1 + (-3.81), reference="C4", value="10pF", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###


### Connecting all wires in the Schematic ###


# Connecting C3 pin 1 (Pin ID 1 -- Name None) to C4 pin 1 (Pin ID 1 -- Name None)
connect_pins("C3", "1", "C4", "1")

# Connecting C3 pin 2 (Pin ID 2 -- Name None) to C4 pin 2 (Pin ID 2 -- Name None)
connect_pins("C3", "2", "C4", "2")

# Connecting #PWR5V pin +5V (Pin ID 1 -- Name +5V) to D_VIN pin A1 (Pin ID 1 -- Name A1)
connect_pins("#PWR5V", "+5V", "D_VIN", "A2")

connect_pins("D_VIN", "A1", "U1", "VIN")

connect_pins("#PWRGND", "GND", "U1", "GND")

# Connecting U1 pin VOUT (Pin ID 5 -- Name VOUT) to #PWR33V pin +3.3V (Pin ID 1 -- Name +3.3V)
connect_pins("U1", "VOUT", "#PWR33V", "+3.3V")

# Connecting U1 pin VIN (Pin ID 1 -- Name VIN) to U1 pin EN (Pin ID 3 -- Name EN)
connect_pins("U1", "VIN", "U1", "EN")

# Connecting C2 pin 2 (Pin ID 2 -- Name None) to U1 pin VIN (Pin ID 1 -- Name VIN)
connect_pins("C2", "1", "U1", "VIN")

# Connecting C2 pin 1 (Pin ID 1 -- Name None) to U1 pin EN (Pin ID 3 -- Name EN)
connect_pins("C2", "2", "#PWRGND", "GND")

# Connecting C4 pin 2 (Pin ID 2 -- Name None) to U1 pin VOUT (Pin ID 5 -- Name VOUT)
connect_pins("C4", "1", "U1", "VOUT")

connect_pins("C4", "2", "#PWRGND", "GND")

write_out_all_wires()