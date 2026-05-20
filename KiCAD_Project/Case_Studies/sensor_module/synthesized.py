#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Synthesized schematic generated from 6 blocks."""

import sys
import os

PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

# ===== Block from generated_1.py =====
### Placing center symbol 1 : Sensors:Sensor_Pressure###

center_x_1, center_y_1 = 183.890, 157.860
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





# ===== Block from generated_2.py =====
### Placing center symbol 1 : Sensor_Optical:APDS-9301###

center_x_2, center_y_2 = 233.890, 156.590
add_schematic_symbol(symbol_lib="Sensor_Optical", symbol_name="APDS-9301", pos_x=center_x_2, pos_y=center_y_2, reference="U1_1", value="APDS-9301", rotation=0, mirror="y")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_2 + (0.0), pos_y=center_y_2 + (34.29), reference="#PWR_3V3_1", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_2 + (0.0), pos_y=center_y_2 + (-21.59), reference="#PWR_GND_1", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_2 + (0.0), pos_y=center_y_2 + (16.51), reference="C1", value="100nF", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label SENSOR-SCK next to U1 pin SCL 
x_U1_4, y_U1_4 = get_pin_location(symbol_ref="U1_1", pin_name="SCL")
add_label(label_pos=[x_U1_4+(7.62), y_U1_4+(0.0)], label_text="SENSOR_SCK", label_ref="SENSOR_SCK_0_1", label_type="input", text_orient="right")
# Connecting Label SENSOR-SCK label_id:0 to U1 pin SCL (Pin ID 4 -- Name SCL)
connect_pins("SENSOR_SCK_0_1", "1", "U1_1", "SCL")

# Add label SENSOR_SDA next to U1 pin SDA 
x_U1_5, y_U1_5 = get_pin_location(symbol_ref="U1_1", pin_name="SDA")
add_label(label_pos=[x_U1_5+(7.62), y_U1_5+(0.0)], label_text="SENSOR_SDA", label_ref="SENSOR_SDA_0_1", label_type="input", text_orient="right")
# Connecting Label SENSOR_SDA label_id:0 to U1 pin SDA (Pin ID 5 -- Name SDA)
connect_pins("SENSOR_SDA_0_1", "1", "U1_1", "SDA")


### Connecting all wires in the Schematic ###


# Connecting U1 pin 1 (Pin ID 1 -- Name None) to #PWR_GND pin 1 (Pin ID 1 -- Name None)
connect_pins("U1_1", "GND", "#PWR_GND_1", "1")

# Connecting #PWR_3V3 pin +3.3V (Pin ID 1 -- Name +3.3V) to C1 pin 1 (Pin ID 1 -- Name None)
connect_pins("#PWR_3V3_1", "1", "C1", "1")

# Connecting C1 pin 2 (Pin ID 2 -- Name None) to U1 pin VDD (Pin ID 6 -- Name VDD)
connect_pins("C1", "2", "U1_1", "VDD")




# ===== Block from generated_3.py =====
### Placing center symbol 2 : Sensor_Audio:SPH0641LU4H-1###

center_x_3, center_y_3 = 295.320, 146.430
add_schematic_symbol(symbol_lib="Sensor_Audio", symbol_name="SPH0641LU4H-1", pos_x=center_x_3, pos_y=center_y_3, reference="U5", value="SPH0641LU4H-1", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 2###

add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_3 + (-11.43), pos_y=center_y_3 + (11.43), reference="#PWR1", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_3 + (0.0), pos_y=center_y_3 + (-11.43), reference="#PWR_2", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label MIC-CLK next to U5 pin CLOCK 
x_U5_4, y_U5_4 = get_pin_location(symbol_ref="U5", pin_name="CLOCK")
add_label(label_pos=[x_U5_4+(11.43), y_U5_4+(0.0)], label_text="MIC-CLK", label_ref="MIC-CLK_0", label_type="input", text_orient="right")
# Connecting Label MIC-CLK label_id:0 to U5 pin CLOCK (Pin ID 4 -- Name CLOCK)
connect_pins("MIC-CLK_0", "1", "U5", "CLOCK")

# Add label MIC-DATA next to U5 pin DATA 
x_U5_3, y_U5_3 = get_pin_location(symbol_ref="U5", pin_name="DATA")
add_label(label_pos=[x_U5_3+(11.43), y_U5_3+(0.0)], label_text="MIC-DATA", label_ref="MIC-DATA_0", label_type="input", text_orient="right")
# Connecting Label MIC-DATA label_id:0 to U5 pin DATA (Pin ID 3 -- Name DATA)
connect_pins("MIC-DATA_0", "1", "U5", "DATA")


### Connecting all wires in the Schematic ###


# Connecting U5 pin 6 (Pin ID 6 -- Name None) to #PWR_2 pin 1 (Pin ID 1 -- Name None)
connect_pins("U5", "GND", "#PWR_2", "1")

# Connecting #PWR1 pin +3.3V (Pin ID 1 -- Name +3.3V) to U5 pin VDD (Pin ID 5 -- Name VDD)
connect_pins("#PWR1", "+3.3V", "U5", "VDD")





# ===== Block from generated_4.py =====
### Placing center symbol 5 : Sensor:BME680###

center_x_4, center_y_4 = 345.320, 155.320
add_schematic_symbol(symbol_lib="Sensor", symbol_name="BME680", pos_x=center_x_4, pos_y=center_y_4, reference="U1_2", value="BME680", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 5###

add_schematic_symbol(symbol_lib="power", symbol_name="+3V3", pos_x=center_x_4 + (0.0), pos_y=center_y_4 + (31.75), reference="#PWR5", value="+3V3", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_4 + (0.0), pos_y=center_y_4 + (-20.32), reference="#PWR7", value="GND", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label SENSOR_SDA next to U1 pin SDI 
x_U1_1_3, y_U1_1_3 = get_pin_location(symbol_ref="U1_2", pin_name="SDI")
add_label(label_pos=[x_U1_1_3+(2.54), y_U1_1_3+(0.0)], label_text="SENSOR_SDA", label_ref="SENSOR_SDA_1", label_type="input", text_orient="right")
# Connecting Label SENSOR_SDA label_id:1 to U1 pin SDI (Pin ID 3 -- Name SDI)
connect_pins("SENSOR_SDA_1", "1", "U1_2", "SDI")

# Add label SENSOR_SCK next to U1 pin SCK 
x_U1_1_4, y_U1_1_4 = get_pin_location(symbol_ref="U1_2", pin_name="SCK")
add_label(label_pos=[x_U1_1_4+(2.54), y_U1_1_4+(0.0)], label_text="SENSOR_SCK", label_ref="SENSOR_SCK_0_2", label_type="input", text_orient="right")
# Connecting Label SENSOR_SCK label_id:0 to U1 pin SCK (Pin ID 4 -- Name SCK)
connect_pins("SENSOR_SCK_0_2", "1", "U1_2", "SCK")


### Connecting all wires in the Schematic ###


# Connecting U1 pin 1 (Pin ID 1 -- Name None) to #PWR7 pin 1 (Pin ID 1 -- Name None)
connect_pins("U1_2", "1", "#PWR7", "1")

# Connecting U1 pin VDDIO (Pin ID 6 -- Name VDDIO) to #PWR5 pin +3V3 (Pin ID 1 -- Name +3V3)
connect_pins("U1_2", "VDDIO", "#PWR5", "+3V3")

# Connecting U1 pin 7 (Pin ID 7 -- Name None) to U1 pin 1 (Pin ID 1 -- Name None)
connect_pins("U1_2", "7", "U1_2", "1")

# Connecting U1_1 pin CSB (Pin ID 7 -- Name CSB) to U1 pin SDI (Pin ID 3 -- Name SDI)
connect_pins("U1_2", "CSB", "#PWR5", "+3V3")






# ===== Block from generated_5.py =====
### Placing center symbol 1 : Sensor_Motion:ISM330DHCX###

center_x_5, center_y_5 = 225.800, 263.740
add_schematic_symbol(symbol_lib="Sensor_Motion", symbol_name="ISM330DHCX", pos_x=center_x_5, pos_y=center_y_5, reference="U3", value="ISM330DHCX", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="C", pos_x=center_x_5 + (-50.8), pos_y=center_y_5 + (-10.16), reference="C20", value="1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_5 + (-31.75), pos_y=center_y_5 + (25.4), reference="#PWR1_1", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_5 + (-31.75), pos_y=center_y_5 + (-22.86), reference="#PWR2", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_5 + (26.67), pos_y=center_y_5 + (25.4), reference="#PWR3", value="+3.3V", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label SENSOR_CLK next to U3 pin SCL 
x_U3_14, y_U3_14 = get_pin_location(symbol_ref="U3", pin_name="SCL")
add_label(label_pos=[x_U3_14+(-11.43), y_U3_14+(0)], label_text="SENSOR_CLK", label_ref="SENSOR_CLK_0", label_type="input", text_orient="left")
# Connecting Label SENSOR_CLK label_id:0 to U3 pin SCL (Pin ID 14 -- Name SCL)
connect_pins("SENSOR_CLK_0", "1", "U3", "SCL")

# Add label SENSOR_SDA next to U3 pin SDA
x_U3_15, y_U3_15 = get_pin_location(symbol_ref="U3", pin_name="SDA")
add_label(label_pos=[x_U3_15+(-11.43), y_U3_15+(0)], label_text="SENSOR_SDA", label_ref="SENSOR_SDA_0_2", label_type="input", text_orient="left")
# Connecting Label SENSOR_SDA label_id:0 to U3 pin SDA (Pin ID 15 -- Name SDA)
connect_pins("SENSOR_SDA_0_2", "1", "U3", "SDA")

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
connect_pins("#PWR1_1", "+3.3V", "C20", "1")

# Connecting C20 pin 2 (Pin ID 2 -- Name None) to #PWR2 pin 1 (Pin ID 1 -- Name None)
connect_pins("C20", "2", "#PWR2", "1")

# Connecting C20 pin 1 (Pin ID 1 -- Name None) to #PWR1 pin +3.3V (Pin ID 1 -- Name +3.3V)
connect_pins("C20", "1", "#PWR1_1", "+3.3V")

connect_pins("U3", "CS", "#PWR3", "+3.3V")





# ===== Block from generated_6.py =====
### Placing center symbol 1 : Sensor_Magnetic:LIS3MDL###

center_x_6, center_y_6 = 320.250, 262.470
add_schematic_symbol(symbol_lib="Sensor_Magnetic", symbol_name="LIS3MDL", pos_x=center_x_6, pos_y=center_y_6, reference="U1_3", value="LIS3MDL", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="Device", symbol_name="C_Small", pos_x=center_x_6 + (-17.78), pos_y=center_y_6 + (-15.24), reference="C1_1", value="0.1uF", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_6 + (2.54), pos_y=center_y_6 + (31.75), reference="#PWR1_2", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_6 + (2.54), pos_y=center_y_6 + (-21.59), reference="#PWR2_1", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="C_Small", pos_x=center_x_6 + (2.54), pos_y=center_y_6 + (-15.24), reference="C2", value="0.1uF", rotation=0, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label SENSOR_CLK next to U1 pin SCL/SPC 
x_U1_1, y_U1_1 = get_pin_location(symbol_ref="U1_3", pin_name="SCL/SPC")
add_label(label_pos=[x_U1_1+(-6.35), y_U1_1+(0.0)], label_text="SENSOR_CLK", label_ref="SENSOR_CLK_0_1", label_type="input", text_orient="left")
# Connecting Label SENSOR_CLK label_id:0 to U1 pin SCL/SPC (Pin ID 1 -- Name SCL/SPC)
connect_pins("SENSOR_CLK_0_1", "1", "U1_3", "SCL/SPC")

# Add label SENSOR_SDA next to U1 pin SDA/SDI/SDO 
x_U1_11, y_U1_11 = get_pin_location(symbol_ref="U1_3", pin_name="SDA/SDI/SDO")
add_label(label_pos=[x_U1_11+(-6.35), y_U1_11+(0.0)], label_text="SENSOR_SDA", label_ref="SENSOR_SDA_0_3", label_type="input", text_orient="left")
# Connecting Label SENSOR_SDA label_id:0 to U1 pin SDA/SDI/SDO (Pin ID 11 -- Name SDA/SDI/SDO)
connect_pins("SENSOR_SDA_0_3", "1", "U1_3", "SDA/SDI/SDO")

x_U1_7, y_U1_7 = get_pin_location(symbol_ref="U1_3", pin_name="INT")
add_label(label_pos=[x_U1_7+(2.54), y_U1_7+(0.0)], label_text="Mag_INT", label_ref="Mag_INT_0", label_type="output", text_orient="right")
# Connecting Label Mag_INT label_id:0 to U1 pin INT (Pin ID 7 -- Name INT)
connect_pins("Mag_INT_0", "1", "U1_3", "INT")


### Connecting all wires in the Schematic ###


# Connecting #PWR1 pin +3.3V (Pin ID 1 -- Name +3.3V) to U1 pin Vdd (Pin ID 5 -- Name Vdd)
connect_pins("#PWR1_2", "+3.3V", "U1_3", "Vdd")

# Connecting #PWR2 pin GND (Pin ID 1 -- Name GND) to U1 pin GND (Pin ID 10 -- Name GND)
connect_pins("C2", "2", "#PWR2_1", "1")

# Connecting C2 pin 1 (Pin ID 1 -- Name None) to U1 pin Vdd_IO (Pin ID 6 -- Name Vdd_IO)
connect_pins("C2", "1", "U1_3", "Vdd_IO")

# Connecting U1 pin Vdd_IO (Pin ID 6 -- Name Vdd_IO) to U1 pin Vdd (Pin ID 5 -- Name Vdd)
connect_pins("U1_3", "Vdd", "U1_3", "Vdd_IO")

# Connecting #PWR2 pin GND (Pin ID 1 -- Name GND) to C1 pin 2 (Pin ID 2 -- Name None)
connect_pins("C1_1", "2", "#PWR2_1", "1")

# Connecting C1 pin 1 (Pin ID 1 -- Name None) to U1 pin Vdd (Pin ID 5 -- Name Vdd)
connect_pins("C1_1", "1", "U1_3", "Vdd")

# Connecting #PWR2 pin 1 (Pin ID 1 -- Name None) to U1 pin 10 (Pin ID 10 -- Name GND)
connect_pins("#PWR2_1", "1", "U1_3", "GND")






write_out_all_wires()
