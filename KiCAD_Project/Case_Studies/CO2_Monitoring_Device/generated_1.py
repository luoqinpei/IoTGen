# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 3 : Interface_USB:CH340G###

center_x_3, center_y_3 = 150.000, 110.000
add_schematic_symbol(symbol_lib="Interface_USB", symbol_name="CH340G", pos_x=center_x_3, pos_y=center_y_3, reference="U6", value="CH340G", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 3###

add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_3 + (-24.13), pos_y=center_y_3 + (10.16), reference="#PWR6", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_3 + (-24.13), pos_y=center_y_3 + (-19.05), reference="#PWR7", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label CH340-TX next to U6 pin TXD 
x_U6_1, y_U6_1 = get_pin_location(symbol_ref="U6", pin_name="TXD")
add_label(label_pos=[x_U6_1+(-3.81), y_U6_1+(0.0)], label_text="CH340-TX", label_ref="CH340-TX_1", label_type="input", text_orient="left")
# Connecting Label CH340-TX label_id:1 to U6 pin TXD (Pin ID 1 -- Name TXD)
connect_pins("CH340-TX_1", "1", "U6", "TXD")

# Add label CH340-RX next to U6 pin RXD 
x_U6_2, y_U6_2 = get_pin_location(symbol_ref="U6", pin_name="RXD")
add_label(label_pos=[x_U6_2+(-3.81), y_U6_2+(0.0)], label_text="CH340-RX", label_ref="CH340-RX_1", label_type="input", text_orient="left")
# Connecting Label CH340-RX label_id:1 to U6 pin RXD (Pin ID 2 -- Name RXD)
connect_pins("CH340-RX_1", "1", "U6", "RXD")

# Add label CH340-DTR next to U6 pin 12 
x_U6_12, y_U6_12 = get_pin_location(symbol_ref="U6", pin_name="12")
add_label(label_pos=[x_U6_12+(-3.81), y_U6_12+(0.0)], label_text="CH340-DTR", label_ref="CH340-DTR_0", label_type="input", text_orient="left")
# Connecting Label CH340-DTR label_id:0 to U6 pin 12 (Pin ID 12 -- Name 12)
connect_pins("CH340-DTR_0", "1", "U6", "12")

# Add label CH340-RTS next to U6 pin ~{RTS} 
x_U6_15, y_U6_15 = get_pin_location(symbol_ref="U6", pin_name="~{RTS}")
add_label(label_pos=[x_U6_15+(-3.81), y_U6_15+(0.0)], label_text="CH340-RTS", label_ref="CH340-RTS_0", label_type="input", text_orient="left")
# Connecting Label CH340-RTS label_id:0 to U6 pin ~{RTS} (Pin ID 15 -- Name ~{RTS})
connect_pins("CH340-RTS_0", "1", "U6", "~{RTS}")

# Add label D+ next to U6 pin UD+ 
x_U6_3, y_U6_3 = get_pin_location(symbol_ref="U6", pin_name="UD+")
add_label(label_pos=[x_U6_3+(-3.81), y_U6_3+(0.0)], label_text="D+", label_ref="D+_0", label_type="input", text_orient="left")
# Connecting Label D+ label_id:0 to U6 pin UD+ (Pin ID 3 -- Name UD+)
connect_pins("D+_0", "1", "U6", "UD+")

# Add label D- next to U6 pin UD- 
x_U6_4, y_U6_4 = get_pin_location(symbol_ref="U6", pin_name="UD-")
add_label(label_pos=[x_U6_4+(-3.81), y_U6_4+(0.0)], label_text="D-", label_ref="D-_0", label_type="input", text_orient="left")
# Connecting Label D- label_id:0 to U6 pin UD- (Pin ID 4 -- Name UD-)
connect_pins("D-_0", "1", "U6", "UD-")


### Connecting all wires in the Schematic ###


# Connecting #PWR7 pin 1 (Pin ID 1 -- Name None) to U6 pin 9 (Pin ID 9 -- Name None)
connect_pins("#PWR7", "1", "U6", "GND")

# Connecting #PWR6 pin +5V (Pin ID 1 -- Name +5V) to U6 pin VCC (Pin ID 11 -- Name VCC)
connect_pins("#PWR6", "+5V", "U6", "VCC")


write_out_all_wires()