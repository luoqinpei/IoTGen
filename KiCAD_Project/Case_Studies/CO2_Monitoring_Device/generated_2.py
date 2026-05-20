# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : RF_Module:ESP32-WROOM-32E###

center_x_1, center_y_1 = 150.000, 110.000
add_schematic_symbol(symbol_lib="RF_Module", symbol_name="ESP32-WROOM-32E", pos_x=center_x_1, pos_y=center_y_1, reference="U1", value="ESP32-WROOM-32E", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_1 + (-20.32), pos_y=center_y_1 + (-8.89), reference="C22", value="0.22uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (-8.89), pos_y=center_y_1 + (36.99), reference="#PWR_3V3", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (-8.89), pos_y=center_y_1 + (-41.59), reference="#PWR_GND_U1", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_1 + (-24.32), pos_y=center_y_1 + (+27.89), reference="C4", value="0.1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_1 + (-24.32), pos_y=center_y_1 + (+33.89), reference="R1", value="10k", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label CH340-TX next to U1 pin TXD0/IO1 
x_U1_21, y_U1_21 = get_pin_location(symbol_ref="U1", pin_name="TXD0/IO1")
add_label(label_pos=[x_U1_21+(-6.35), y_U1_21+(0.0)], label_text="CH340-RX", label_ref="CH340-RX_0", label_type="input", text_orient="left")
# Connecting Label CH340-TX label_id:0 to U1 pin TXD0/IO1 (Pin ID 21 -- Name TXD0/IO1)
connect_pins("CH340-RX_0", "1", "U1", "TXD0/IO1")

# Add label CH340-RX next to U1 pin RXD0/IO3 
x_U1_20, y_U1_20 = get_pin_location(symbol_ref="U1", pin_name="RXD0/IO3")
add_label(label_pos=[x_U1_20+(-6.35), y_U1_20+(0.0)], label_text="CH340-TX", label_ref="CH340-TX_0", label_type="input", text_orient="left")
# Connecting Label CH340-RX label_id:0 to U1 pin RXD0/IO3 (Pin ID 20 -- Name RXD0/IO3)
connect_pins("CH340-TX_0", "1", "U1", "RXD0/IO3")

# Add label I2C_SDA{slash}SDI next to U1 pin IO21/SDA 
x_U1_38, y_U1_38 = get_pin_location(symbol_ref="U1", pin_name="IO21")
add_label(label_pos=[x_U1_38+(-6.35), y_U1_38+(0.0)], label_text="I2C_SDA{slash}SDI", label_ref="I2C_SDA{slash}SDI_0", label_type="input", text_orient="left")
# Connecting Label I2C_SDA{slash}SDI label_id:0 to U1 pin IO21 (Pin ID 38 -- Name IO21)
connect_pins("I2C_SDA{slash}SDI_0", "1", "U1", "IO21")

# Add label I2C_SCL{slash}SCK next to U1 pin IO22/SCL 
x_U1_37, y_U1_37 = get_pin_location(symbol_ref="U1", pin_name="IO22")
add_label(label_pos=[x_U1_37+(-6.35), y_U1_37+(0.0)], label_text="I2C_SCL{slash}SCK", label_ref="I2C_SCL{slash}SCK_0", label_type="input", text_orient="left")
# Connecting Label I2C_SCL{slash}SCK label_id:0 to U1 pin IO22/SCL (Pin ID 37 -- Name IO22/SCL)
connect_pins("I2C_SCL{slash}SCK_0", "1", "U1", "IO22")

# Add label D1-PRO next to U1 pin IO13 
x_U1_27, y_U1_27 = get_pin_location(symbol_ref="U1", pin_name="IO13")
add_label(label_pos=[x_U1_27+(-6.35), y_U1_27+(0.0)], label_text="DAT3", label_ref="DAT3_0", label_type="input", text_orient="left")
# Connecting Label D1-PRO label_id:0 to U1 pin IO13 (Pin ID 27 -- Name IO13)
connect_pins("DAT3_0", "1", "U1", "IO13")

# Add label D2-PRO next to U1 pin IO15 
x_U1_25, y_U1_25 = get_pin_location(symbol_ref="U1", pin_name="IO15")
add_label(label_pos=[x_U1_25+(-6.35), y_U1_25+(0.0)], label_text="CMD", label_ref="CMD_0", label_type="input", text_orient="left")
# Connecting Label D2-PRO label_id:0 to U1 pin IO15 (Pin ID 25 -- Name IO15)
connect_pins("CMD_0", "1", "U1", "IO15")

# Add label D3-PRO next to U1 pin IO2 
x_U1_26, y_U1_26 = get_pin_location(symbol_ref="U1", pin_name="IO2")
add_label(label_pos=[x_U1_26+(-6.35), y_U1_26+(0.0)], label_text="DAT0", label_ref="DAT0_0", label_type="input", text_orient="left")
# Connecting Label D3-PRO label_id:0 to U1 pin IO2 (Pin ID 26 -- Name IO2)
connect_pins("DAT0_0", "1", "U1", "IO2")

# Add label D11-PRO next to U1 pin IO16 
x_U1_14, y_U1_14 = get_pin_location(symbol_ref="U1", pin_name="IO16")
add_label(label_pos=[x_U1_14+(-6.35), y_U1_14+(0.0)], label_text="RXD", label_ref="RXD_0", label_type="input", text_orient="left")
# Connecting Label D11-PRO label_id:0 to U1 pin IO16 (Pin ID 14 -- Name IO16)
connect_pins("RXD_0", "1", "U1", "IO16")

# Add label D6-PRO next to U1 pin IO14 
x_U1_13, y_U1_13 = get_pin_location(symbol_ref="U1", pin_name="IO14")
add_label(label_pos=[x_U1_13+(-6.35), y_U1_13+(0.0)], label_text="CLK", label_ref="CLK_0", label_type="input", text_orient="left")
# Connecting Label D6-PRO label_id:0 to U1 pin IO14 (Pin ID 13 -- Name IO14)
connect_pins("CLK_0", "1", "U1", "IO14")

# Add label D4-PRO next to U1 pin IO12 
x_U1_12, y_U1_12 = get_pin_location(symbol_ref="U1", pin_name="IO12")
add_label(label_pos=[x_U1_12+(-6.35), y_U1_12+(0.0)], label_text="DAT2", label_ref="DAT2_0", label_type="input", text_orient="left")
# Connecting Label D4-PRO label_id:0 to U1 pin IO12 (Pin ID 12 -- Name IO12)
connect_pins("DAT2_0", "1", "U1", "IO12")

# Add label D5-PRO next to U1 pin IO4 
x_U1_5, y_U1_5 = get_pin_location(symbol_ref="U1", pin_name="IO4")
add_label(label_pos=[x_U1_5+(-6.35), y_U1_5+(0.0)], label_text="DAT1", label_ref="DAT1_0", label_type="input", text_orient="left")
# Connecting Label D5-PRO label_id:0 to U1 pin IO4 (Pin ID 5 -- Name IO4)
connect_pins("DAT1_0", "1", "U1", "IO4")

# Add label D12-PRO next to U1 pin IO0 
x_U1_34, y_U1_34 = get_pin_location(symbol_ref="U1", pin_name="IO0")
add_label(label_pos=[x_U1_34+(-6.35), y_U1_34+(0.0)], label_text="BOOT", label_ref="BOOT_0", label_type="input", text_orient="left")
# Connecting Label D12-PRO label_id:0 to U1 pin IO0 (Pin ID 34 -- Name IO0)
connect_pins("BOOT_0", "1", "U1", "IO0")

# Add label ADO{slash}TDI next to U1 pin IO25 
x_U1_33, y_U1_33 = get_pin_location(symbol_ref="U1", pin_name="IO25")
add_label(label_pos=[x_U1_33+(-6.35), y_U1_33+(0.0)], label_text="LED", label_ref="LED_0", label_type="input", text_orient="left")
# Connecting Label ADO{slash}TDI label_id:0 to U1 pin IO25 (Pin ID 33 -- Name IO25)
connect_pins("LED_0", "1", "U1", "IO25")

# Add label D11-PRO{slash}AUX next to U1 pin IO5 
x_U1_28, y_U1_28 = get_pin_location(symbol_ref="U1", pin_name="IO5")
add_label(label_pos=[x_U1_28+(-6.35), y_U1_28+(0.0)], label_text="ESP5", label_ref="ESP5_0", label_type="input", text_orient="left")
# Connecting Label D11-PRO{slash}AUX label_id:0 to U1 pin IO5 (Pin ID 28 -- Name IO5)
connect_pins("ESP5_0", "1", "U1", "IO5")

# Add label D13-PRO{slash}AUX next to U1 pin IO33 
x_U1_3, y_U1_3 = get_pin_location(symbol_ref="U1", pin_name="IO33")
add_label(label_pos=[x_U1_3+(-6.35), y_U1_3+(0.0)], label_text="ESP33", label_ref="ESP33_0", label_type="input", text_orient="left")
# Connecting Label D13-PRO{slash}AUX label_id:0 to U1 pin IO33 (Pin ID 3 -- Name IO33)
connect_pins("ESP33_0", "1", "U1", "IO33")

# Add label D10-PRO{slash}AUX next to U1 pin IO32 
x_U1_2, y_U1_2 = get_pin_location(symbol_ref="U1", pin_name="IO32")
add_label(label_pos=[x_U1_2+(-6.35), y_U1_2+(0.0)], label_text="ESP32", label_ref="ESP32_0", label_type="input", text_orient="left")
# Connecting Label D10-PRO{slash}AUX label_id:0 to U1 pin IO32 (Pin ID 2 -- Name IO32)
connect_pins("ESP32_0", "1", "U1", "IO32")

x_U1_3, y_U1_3 = get_pin_location(symbol_ref="U1", pin_name="EN")
add_label(label_pos=[x_U1_3+(-16.35), y_U1_3+(0.0)], label_text="RESET", label_ref="RESET_0", label_type="input", text_orient="left")
connect_pins("RESET_0", "1", "U1", "EN")


### Connecting all wires in the Schematic ###


# Connecting C22 pin 2 (Pin ID 2 -- Name None) to U1 pin VDDA (Pin ID 43 -- Name VDDA)
connect_pins("C22", "1", "U1", "VDD")

# Connecting U1 pin 46 (Pin ID 46 -- Name None) to #PWR_GND_U1 pin 1 (Pin ID 1 -- Name None)
connect_pins("U1", "GND", "#PWR_GND_U1", "1")

# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to U1 pin VCC (Pin ID 44 -- Name VCC)
connect_pins("#PWR_3V3", "+3.3V", "U1", "VDD")

# Connecting C4 pin 1 (Pin ID 1 -- Name None) to U1 pin VDD (Pin ID 41 -- Name VDD)
connect_pins("C22", "2", "U1", "GND")

connect_pins("C4", "2", "#PWR_GND_U1", "1")

connect_pins("C4", "1", "U1", "EN")

connect_pins("R1", "2", "U1", "EN")

connect_pins("R1", "1", "#PWR_3V3", "+3.3V")


write_out_all_wires()