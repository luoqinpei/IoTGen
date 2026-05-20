#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Synthesized schematic generated from 9 blocks."""

import sys
import os

PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

# ===== Block from generated_1.py =====
### Placing center symbol 3 : Interface_USB:CH340G###

center_x_1, center_y_1 = 199.130, 154.050
add_schematic_symbol(symbol_lib="Interface_USB", symbol_name="CH340G", pos_x=center_x_1, pos_y=center_y_1, reference="U6", value="CH340G", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 3###

add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (-24.13), pos_y=center_y_1 + (10.16), reference="#PWR6", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (-24.13), pos_y=center_y_1 + (-19.05), reference="#PWR7", value="GND", rotation=0, mirror="None")

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





# ===== Block from generated_2.py =====
### Placing center symbol 1 : RF_Module:ESP32-WROOM-32E###

center_x_2, center_y_2 = 249.320, 176.590
add_schematic_symbol(symbol_lib="RF_Module", symbol_name="ESP32-WROOM-32E", pos_x=center_x_2, pos_y=center_y_2, reference="U1", value="ESP32-WROOM-32E", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_2 + (-20.32), pos_y=center_y_2 + (-8.89), reference="C22", value="0.22uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_2 + (-8.89), pos_y=center_y_2 + (36.99), reference="#PWR_3V3", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_2 + (-8.89), pos_y=center_y_2 + (-41.59), reference="#PWR_GND_U1", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_2 + (-24.32), pos_y=center_y_2 + (+27.89), reference="C4", value="0.1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_2 + (-24.32), pos_y=center_y_2 + (+33.89), reference="R1", value="10k", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label CH340-TX next to U1 pin TXD0/IO1 
x_U1_21, y_U1_21 = get_pin_location(symbol_ref="U1", pin_name="TXD0/IO1")
add_label(label_pos=[x_U1_21+(-6.35), y_U1_21+(0.0)], label_text="CH340-TX", label_ref="CH340-TX_0", label_type="input", text_orient="left")
# Connecting Label CH340-TX label_id:0 to U1 pin TXD0/IO1 (Pin ID 21 -- Name TXD0/IO1)
connect_pins("CH340-TX_0", "1", "U1", "TXD0/IO1")

# Add label CH340-RX next to U1 pin RXD0/IO3 
x_U1_20, y_U1_20 = get_pin_location(symbol_ref="U1", pin_name="RXD0/IO3")
add_label(label_pos=[x_U1_20+(-6.35), y_U1_20+(0.0)], label_text="CH340-RX", label_ref="CH340-RX_0", label_type="input", text_orient="left")
# Connecting Label CH340-RX label_id:0 to U1 pin RXD0/IO3 (Pin ID 20 -- Name RXD0/IO3)
connect_pins("CH340-RX_0", "1", "U1", "RXD0/IO3")

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





# ===== Block from generated_3.py =====
### Placing center symbol 1 : Connector:USB_C_Receptacle###

center_x_3, center_y_3 = 280.270, 175.640
add_schematic_symbol(symbol_lib="Connector", symbol_name="USB_C_Plug_USB2.0", pos_x=center_x_3, pos_y=center_y_3, reference="P1", value="USB_C_Receptacle", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_3 + (14.60), pos_y=center_y_3 + (-31.75), reference="R1_1", value="5.1k", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_3 + (10.16), pos_y=center_y_3 + (-40.64), reference="#PWR1", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="VCC", pos_x=center_x_3 + (14.60), pos_y=center_y_3 + (31.75), reference="#PWR2", value="V_USB", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label D-_1 next to P1 pin D- 
x_P1_A7, y_P1_A7 = get_pin_location(symbol_ref="P1", pin_name="D-")
add_label(label_pos=[x_P1_A7+(-12.7), y_P1_A7+(0.0)], label_text="D-_1", label_ref="D-_1_1", label_type="input", text_orient="left")
# Connecting Label D-_1 label_id:1 to P1 pin D- (Pin ID A7 -- Name D-)
connect_pins("D-_1_1", "1", "P1", "D-")

# Add label D+_1 next to P1 pin D+ 
x_P1_A6, y_P1_A6 = get_pin_location(symbol_ref="P1", pin_name="D+")
add_label(label_pos=[x_P1_A6+(-12.7), y_P1_A6+(0.0)], label_text="D+_1", label_ref="D+_1_0", label_type="input", text_orient="left")
# Connecting Label D+_1 label_id:0 to P1 pin D+ (Pin ID A6 -- Name D+)
connect_pins("D+_1_0", "1", "P1", "D+")


### Connecting all wires in the Schematic ###


# Connecting R1 pin 2 (Pin ID 2 -- Name None) to #PWR1 pin 1 (Pin ID 1 -- Name None)
connect_pins("R1_1", "2", "#PWR1", "1")

# Connecting P1 pin CC (Pin ID A5 -- Name CC) to R1 pin 1 (Pin ID 1 -- Name None)
connect_pins("P1", "CC", "R1_1", "1")

connect_pins("P1", "GND", "#PWR1", "1")

connect_pins("P1", "VBUS", "#PWR2", "1")




# ===== Block from generated_4.py =====
### Placing center symbol 1 : Regulator_Linear:AP2112K-3.3###

center_x_4, center_y_4 = 381.700, 145.360
add_schematic_symbol(symbol_lib="Regulator_Linear", symbol_name="AP2112K-3.3", pos_x=center_x_4, pos_y=center_y_4, reference="U1_1", value="AP2112K-3.3", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="power", symbol_name="VCC", pos_x=center_x_4 + (-36.83), pos_y=center_y_4 + (7.62), reference="#PWR5V", value="V_USB", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_4 + (10.16), pos_y=center_y_4 + (1.27), reference="#PWR33V", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_4 + (0.00), pos_y=center_y_4 + (-10.36), reference="#PWRGND", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="D_TVS", pos_x=center_x_4 + (-17.78), pos_y=center_y_4 + (-2.54), reference="D_VIN", value="~", rotation=270, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_4 + (-10.35), pos_y=center_y_4 + (-3.81), reference="C2", value="1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_4 + (12.54), pos_y=center_y_4 + (-3.81), reference="C3", value="1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_4 + (20.08), pos_y=center_y_4 + (-3.81), reference="C4_1", value="10pF", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###


### Connecting all wires in the Schematic ###


# Connecting C3 pin 1 (Pin ID 1 -- Name None) to C4 pin 1 (Pin ID 1 -- Name None)
connect_pins("C3", "1", "C4_1", "1")

# Connecting C3 pin 2 (Pin ID 2 -- Name None) to C4 pin 2 (Pin ID 2 -- Name None)
connect_pins("C3", "2", "C4_1", "2")

# Connecting #PWR5V pin +5V (Pin ID 1 -- Name +5V) to D_VIN pin A1 (Pin ID 1 -- Name A1)
connect_pins("#PWR5V", "+5V", "D_VIN", "A2")

connect_pins("D_VIN", "A1", "U1_1", "VIN")

connect_pins("#PWRGND", "GND", "U1_1", "GND")

# Connecting U1 pin VOUT (Pin ID 5 -- Name VOUT) to #PWR33V pin +3.3V (Pin ID 1 -- Name +3.3V)
connect_pins("U1_1", "VOUT", "#PWR33V", "+3.3V")

# Connecting U1 pin VIN (Pin ID 1 -- Name VIN) to U1 pin EN (Pin ID 3 -- Name EN)
connect_pins("U1_1", "VIN", "U1_1", "EN")

# Connecting C2 pin 2 (Pin ID 2 -- Name None) to U1 pin VIN (Pin ID 1 -- Name VIN)
connect_pins("C2", "1", "U1_1", "VIN")

# Connecting C2 pin 1 (Pin ID 1 -- Name None) to U1 pin EN (Pin ID 3 -- Name EN)
connect_pins("C2", "2", "#PWRGND", "GND")

# Connecting C4 pin 2 (Pin ID 2 -- Name None) to U1 pin VOUT (Pin ID 5 -- Name VOUT)
connect_pins("C4_1", "1", "U1_1", "VOUT")

connect_pins("C4_1", "2", "#PWRGND", "GND")




# ===== Block from generated_5.py =====
### Placing center symbol 1 : Driver_LED:WS2811###

center_x_5, center_y_5 = 188.970, 292.790
add_schematic_symbol(symbol_lib="LED", symbol_name="WS2812B", pos_x=center_x_5, pos_y=center_y_5, reference="U1_2", value="WS2811", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="C_Small", pos_x=center_x_5 + (+17.62), pos_y=center_y_5 + (-22.86), reference="C5", value="2.2uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_5 + (-13.97), pos_y=center_y_5 + (6.35), reference="#PWR_3V3_U1", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_5 + (0.0), pos_y=center_y_5 + (-29.21), reference="#PWR_GND_U1_1", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label D1-PRO_0 next to U1 pin DIN 
x_U1_6, y_U1_6 = get_pin_location(symbol_ref="U1_2", pin_name="DIN")
add_label(label_pos=[x_U1_6+(-16.51), y_U1_6+(0.0)], label_text="LED", label_ref="LED_0_1", label_type="input", text_orient="left")
# Connecting Label D1-PRO_0 label_id:0 to U1 pin DIN (Pin ID 6 -- Name DIN)
connect_pins("LED_0_1", "1", "U1_2", "DIN")


### Connecting all wires in the Schematic ###


# Connecting C5 pin 2 (Pin ID 2 -- Name None) to #PWR_GND_U1 pin 1 (Pin ID 1 -- Name None)
connect_pins("C5", "2", "#PWR_GND_U1_1", "1")

# Connecting #PWR_3V3_U1 pin +3.3V (Pin ID 1 -- Name +3.3V) to U1 pin VDD (Pin ID 8 -- Name VDD)
connect_pins("#PWR_3V3_U1", "+3.3V", "U1_2", "VDD")

# Connecting U1 pin VSS (Pin ID 4 -- Name VSS) to #PWR_GND_U1 pin 1 (Pin ID 1 -- Name None)
connect_pins("U1_2", "VSS", "#PWR_GND_U1_1", "1")

# Connecting C5 pin 1 (Pin ID 1 -- Name None) to U1 pin VDD (Pin ID 8 -- Name VDD)
connect_pins("C5", "1", "U1_2", "VDD")





# ===== Block from generated_6.py =====
### Placing center symbol 2 : Switch:SW_SPST###

center_x_6, center_y_6 = 256.590, 273.740
add_schematic_symbol(symbol_lib="Switch", symbol_name="SW_SPST", pos_x=center_x_6, pos_y=center_y_6, reference="SW2", value="OFF", rotation=90, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 2###

add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_6 + (0.0), pos_y=center_y_6 + (-10.16), reference="#GND1", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Switch", symbol_name="SW_SPST", pos_x=center_x_6 + (22.86), pos_y=center_y_6 + (2.54), reference="SW1", value="OFF", rotation=90, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_6 + (22.86), pos_y=center_y_6 + (-7.62), reference="#GND2", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label BOOT next to SW1 pin B 
x_SW1_2, y_SW1_2 = get_pin_location(symbol_ref="SW1", pin_name="B")
add_label(label_pos=[x_SW1_2+(10.16), y_SW1_2+(0.0)], label_text="BOOT", label_ref="BOOT_0_1", label_type="input", text_orient="right")
# Connecting Label BOOT label_id:0 to SW1 pin B (Pin ID 2 -- Name B)
connect_pins("BOOT_0_1", "1", "SW1", "B")

# Add label RESET next to SW2 pin B 
x_SW2_2, y_SW2_2 = get_pin_location(symbol_ref="SW2", pin_name="B")
add_label(label_pos=[x_SW2_2+(27.94), y_SW2_2+(0.0)], label_text="RESET", label_ref="RESET_0_1", label_type="input", text_orient="right")
# Connecting Label RESET label_id:0 to SW2 pin B (Pin ID 2 -- Name B)
connect_pins("RESET_0_1", "1", "SW2", "B")


### Connecting all wires in the Schematic ###


# Connecting SW2 pin A (Pin ID 1 -- Name A) to #GND1 pin 1 (Pin ID 1 -- Name None)
connect_pins("SW2", "A", "#GND1", "1")

# Connecting SW1 pin A (Pin ID 1 -- Name A) to #GND2 pin 1 (Pin ID 1 -- Name None)
connect_pins("SW1", "A", "#GND2", "1")





# ===== Block from generated_7.py =====
### Placing center symbol 1 : Sensors:Sensor_Gas###

center_x_7, center_y_7 = 351.040, 290.250
add_schematic_symbol(symbol_lib="Sensor_Gas", symbol_name="SCD40-D-R2", pos_x=center_x_7, pos_y=center_y_7, reference="U1_3", value="SCD40-D-R2", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_7 + (+15.21), pos_y=center_y_7 + (12.62), reference="R11", value="4.7k", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_7 + (+21.21), pos_y=center_y_7 + (12.62), reference="R22", value="4.7k", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_7 + (-21.59), pos_y=center_y_7 + (-7.62), reference="C1", value="0.1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_7 + (-21.59), pos_y=center_y_7 + (19.05), reference="#PWR_3V3_1", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_7 + (-21.59), pos_y=center_y_7 + (-26.67), reference="#PWR_GND", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label I2C_SDA{slash}SDI next to R22 pin 1 
x_R22_1, y_R22_1 = get_pin_location(symbol_ref="U1_3", pin_name="SDA")
add_label(label_pos=[x_R22_1+(12.89), y_R22_1+(0.0)], label_text="I2C_SDA{slash}SDI", label_ref="I2C_SDA{slash}SDI_0_1", label_type="input", text_orient="right")
# Connecting Label I2C_SDA{slash}SDI label_id:0 to R22 pin 1 (Pin ID 1 -- Name 1)
connect_pins("I2C_SDA{slash}SDI_0_1", "1", "U1_3", "SDA")

# Add label I2C_SCL{slash}SDO next to R11 pin 1 
x_R11_1, y_R11_1 = get_pin_location(symbol_ref="U1_3", pin_name="SCL")
add_label(label_pos=[x_R11_1+(12.89), y_R11_1+(0.0)], label_text="I2C_SCL{slash}SDO", label_ref="I2C_SCL{slash}SDO_0", label_type="input", text_orient="right")
# Connecting Label I2C_SCL{slash}SDO label_id:0 to R11 pin 1 (Pin ID 1 -- Name 1)
connect_pins("I2C_SCL{slash}SDO_0", "1", "U1_3", "SCL")

### Connecting all wires in the Schematic ###


# Connecting C1 pin 2 (Pin ID 2 -- Name None) to #PWR_GND pin 1 (Pin ID 1 -- Name None)
connect_pins("C1", "2", "#PWR_GND", "1")

connect_pins("#PWR_GND", "1", "U1_3", "GND")

# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to U1 pin VDD (Pin ID 2 -- Name VDD)
connect_pins("#PWR_3V3_1", "+3.3V", "U1_3", "VDD")

# Connecting R11 pin 2 (Pin ID 2 -- Name None) to U1 pin SCL (Pin ID 4 -- Name SCL)
connect_pins("R11", "2", "I2C_SCL{slash}SDO_0", "1")

# Connecting R22 pin 2 (Pin ID 2 -- Name None) to U1 pin SDA (Pin ID 3 -- Name SDA)
connect_pins("R22", "2", "U1_3", "SDA")

# Connecting C1 pin 1 (Pin ID 1 -- Name None) to #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V)
connect_pins("C1", "1", "#PWR_3V3_1", "+3.3V")

# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to R11 pin 1 (Pin ID 1 -- Name None)
connect_pins("#PWR_3V3_1", "+3.3V", "R11", "1")

# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to R22 pin 1 (Pin ID 1 -- Name None)
connect_pins("#PWR_3V3_1", "+3.3V", "R22", "1")





# ===== Block from generated_8.py =====
### Placing center symbol 2 : Device:Q_NPN_BCE###

center_x_8, center_y_8 = 177.540, 373.270
add_schematic_symbol(symbol_lib="Device", symbol_name="Q_NPN_BCE", pos_x=center_x_8, pos_y=center_y_8, reference="Q2", value="NPN", rotation=90, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 2###

add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_8 + (-2.54), pos_y=center_y_8 + (-13.97), reference="R2", value="10k", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_8 + (27.86), pos_y=center_y_8 + (-0.0), reference="R1_2", value="10k", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="Q_NPN_BCE", pos_x=center_x_8 + (29.21), pos_y=center_y_8 + (-13.97), reference="Q1", value="NPN", rotation=180, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label CH340-RTS next to R2 pin 1 
x_R2_1, y_R2_1 = get_pin_location(symbol_ref="R2", pin_name="1")
add_label(label_pos=[x_R2_1+(-7.62), y_R2_1+(0.0)], label_text="CH340-RTS", label_ref="CH340-RTS_0_1", label_type="input", text_orient="left")
# Connecting Label CH340-RTS label_id:0 to R2 pin 1 (Pin ID 1 -- Name 1)
connect_pins("CH340-RTS_0_1", "1", "R2", "1")

# Add label CH340-DTR next to R1 pin 1 
x_R1_1, y_R1_1 = get_pin_location(symbol_ref="R1_2", pin_name="1")
add_label(label_pos=[x_R1_1+(-7.62), y_R1_1+(0.0)], label_text="CH340-DTR", label_ref="CH340-DTR_0_1", label_type="input", text_orient="left")
# Connecting Label CH340-DTR label_id:0 to R1 pin 1 (Pin ID 1 -- Name 1)
connect_pins("CH340-DTR_0_1", "1", "R1_2", "1")

# Add label RESET next to Q1 pin C 
x_Q1_1, y_Q1_1 = get_pin_location(symbol_ref="Q1", pin_name="C")
add_label(label_pos=[x_Q1_1+(-6.35), y_Q1_1+(0.0)], label_text="RESET", label_ref="RESET_0_2", label_type="input", text_orient="left")
# Connecting Label RESET label_id:0 to Q1 pin C (Pin ID 1 -- Name C)
connect_pins("RESET_0_2", "1", "Q1", "C")

# Add label BOOT next to Q2 pin C 
x_Q2_1, y_Q2_1 = get_pin_location(symbol_ref="Q2", pin_name="C")
add_label(label_pos=[x_Q2_1+(-6.35), y_Q2_1+(0.0)], label_text="BOOT", label_ref="BOOT_0_2", label_type="input", text_orient="left")
# Connecting Label BOOT label_id:0 to Q2 pin C (Pin ID 1 -- Name C)
connect_pins("BOOT_0_2", "1", "Q2", "C")


### Connecting all wires in the Schematic ###


# Connecting R2 pin 2 (Pin ID 2 -- Name None) to Q2 pin B (Pin ID 2 -- Name B)
connect_pins("R2", "2", "Q2", "B")

# Connecting Q2 pin B (Pin ID 2 -- Name B) to R1 pin 2 (Pin ID 2 -- Name None)
connect_pins("Q1", "B", "R1_2", "2")

connect_pins("Q1", "E", "CH340-RTS_0_1", "1")

connect_pins("Q2", "E", "CH340-DTR_0_1", "1")





# ===== Block from generated_9.py =====
### Placing center symbol 1 : Connector:Micro_SD_Card###

center_x_9, center_y_9 = 301.450, 388.190
add_schematic_symbol(symbol_lib="Connector", symbol_name="Micro_SD_Card", pos_x=center_x_9, pos_y=center_y_9, reference="J1", value="Micro_SD_Card", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_9 + (-24.32), pos_y=center_y_9 + (28.89), reference="#PWR_3V3_2", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_9 + (-24.32), pos_y=center_y_9 + (-28.89), reference="#PWR_GND_1", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_9 + (-28.32), pos_y=center_y_9 + (+20.16), reference="R1_3", value="10k", rotation=180, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_9 + (-32.32), pos_y=center_y_9 + (+20.16), reference="R2_1", value="10k", rotation=180, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_9 + (-35.32), pos_y=center_y_9 + (+20.16), reference="R3", value="10k", rotation=180, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_9 + (-38.94), pos_y=center_y_9 + (+20.16), reference="R4", value="10k", rotation=180, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="R", pos_x=center_x_9 + (-44.7), pos_y=center_y_9 + (+20.16), reference="R5", value="10k", rotation=180, mirror="None")
### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label DAT1 next to J1 pin DAT1 
x_J1_8, y_J1_8 = get_pin_location(symbol_ref="J1", pin_name="DAT1")
add_label(label_pos=[x_J1_8+(-24.13), y_J1_8+(0.0)], label_text="DAT1", label_ref="DAT1_0_1", label_type="input", text_orient="left")
# Connecting Label DAT1 label_id:0 to J1 pin DAT1 (Pin ID 8 -- Name DAT1)
connect_pins("DAT1_0_1", "1", "J1", "DAT1")

# Add label DAT0 next to J1 pin DAT0 
x_J1_7, y_J1_7 = get_pin_location(symbol_ref="J1", pin_name="DAT0")
add_label(label_pos=[x_J1_7+(-24.13), y_J1_7+(0.0)], label_text="DAT0", label_ref="DAT0_0_1", label_type="input", text_orient="left")
# Connecting Label DAT0 label_id:0 to J1 pin DAT0 (Pin ID 7 -- Name DAT0)
connect_pins("DAT0_0_1", "1", "J1", "DAT0")

# Add label CLK next to J1 pin CLK 
x_J1_5, y_J1_5 = get_pin_location(symbol_ref="J1", pin_name="CLK")
add_label(label_pos=[x_J1_5+(-24.13), y_J1_5+(0.0)], label_text="CLK", label_ref="CLK_0_1", label_type="input", text_orient="left")
# Connecting Label CLK label_id:0 to J1 pin CLK (Pin ID 5 -- Name CLK)
connect_pins("CLK_0_1", "1", "J1", "CLK")

# Add label CMD next to J1 pin CMD 
x_J1_3, y_J1_3 = get_pin_location(symbol_ref="J1", pin_name="CMD")
add_label(label_pos=[x_J1_3+(-24.13), y_J1_3+(0.0)], label_text="CMD", label_ref="CMD_0_1", label_type="input", text_orient="left")
# Connecting Label CMD label_id:0 to J1 pin CMD (Pin ID 3 -- Name CMD)
connect_pins("CMD_0_1", "1", "J1", "CMD")

# Add label DAT2 next to J1 pin DAT2/CD 
x_J1_2, y_J1_2 = get_pin_location(symbol_ref="J1", pin_name="DAT2")
add_label(label_pos=[x_J1_2+(-24.13), y_J1_2+(0.0)], label_text="DAT2", label_ref="DAT2_0_1", label_type="input", text_orient="left")
# Connecting Label DAT2 label_id:0 to J1 pin DAT2/CD (Pin ID 2 -- Name DAT2/CD)
connect_pins("DAT2_0_1", "1", "J1", "DAT2")

x_J1_2, y_J1_2 = get_pin_location(symbol_ref="J1", pin_name="DAT3/CD")
add_label(label_pos=[x_J1_2+(-24.13), y_J1_2+(0.0)], label_text="DAT3", label_ref="DAT3_0_1", label_type="input", text_orient="left")
# Connecting Label DAT3 label_id:0 to J1 pin DAT3/CD (Pin ID 2 -- Name DAT3/CD)
connect_pins("DAT3_0_1", "1", "J1", "DAT3/CD")


### Connecting all wires in the Schematic ###


# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to J1 pin VDD (Pin ID 4 -- Name VDD)
connect_pins("#PWR_3V3_2", "+3.3V", "J1", "VDD")

# Connecting R3 pin 1 (Pin ID 1 -- Name None) to J1 pin DAT3/CD (Pin ID 2 -- Name DAT3/CD)
connect_pins("R3", "1", "J1", "DAT3/CD")
connect_pins("R3", "2", "#PWR_3V3_2", "1")

# Connecting J1 pin VDD (Pin ID 4 -- Name VDD) to R1 pin 1 (Pin ID 1 -- Name None)
connect_pins("J1", "DAT2", "R1_3", "1")
connect_pins("R1_3", "2", "#PWR_3V3_2", "1")

# Connecting R4 pin 1 (Pin ID 1 -- Name None) to J1 pin CMD (Pin ID 5 -- Name CLK)
connect_pins("R4", "1", "J1", "CMD")
connect_pins("R4", "2", "#PWR_3V3_2", "1")

# Connecting R2 pin 1 (Pin ID 1 -- Name None) to J1 pin DAT0 (Pin ID 3 -- Name DAT0)
connect_pins("R2_1", "1", "J1", "DAT0")
connect_pins("R2_1", "2", "#PWR_3V3_2", "1")

# Connecting R5 pin 1 (Pin ID 1 -- Name None) to J1 pin DAT1 (Pin ID 8 -- Name DAT1)
connect_pins("R5", "1", "J1", "DAT1")
connect_pins("R5", "2", "#PWR_3V3_2", "1")


connect_pins("J1", "VSS", "#PWR_GND_1", "1")




write_out_all_wires()
