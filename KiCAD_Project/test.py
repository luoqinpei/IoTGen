# The file is only used as a container for testing the generated Python Code

# Auto-generated schematic symbols
import sys
import os

# Get project path and import kicad schematic interface
PROJECT_PATH = os.environ['PROJECT_PATH']
sys.path.append(PROJECT_PATH)
from modules.kicad_sch_interface import *

### Placing center symbol 1 : Sensors_GPS:ZED-F9P###

center_x_1, center_y_1 = 150.0, 110.0

add_schematic_symbol(symbol_lib="Sensors_GPS", symbol_name="ZED-F9P", pos_x=center_x_1, pos_y=center_y_1, reference="U1", value="ZED-F9P", rotation=0, mirror="None")

### Placing other symbols in the Schematic with respect to the center symbol 1###

add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (-29), pos_y=center_y_1 + (19), reference="#PWR_+3V1", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="GND", pos_x=center_x_1 + (1), pos_y=center_y_1 + (-33), reference="#PWR1", value="GND", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Connector_Generic", symbol_name="Conn_01x04_Socket", pos_x=center_x_1 + (45), pos_y=center_y_1 + (21), reference="D1", value="ESP-32-PROJECT", rotation=180, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="Ferrite", pos_x=center_x_1 + (45), pos_y=center_y_1 + (-12), reference="R9", value="0603/0805/1206", rotation=270, mirror="None")
add_schematic_symbol(symbol_lib="power", symbol_name="+3.3V", pos_x=center_x_1 + (45), pos_y=center_y_1 + (-21), reference="#PWR2", value="+3.3V", rotation=0, mirror="None")
add_schematic_symbol(symbol_lib="Device", symbol_name="D_TVS", pos_x=center_x_1 + (60), pos_y=center_y_1 + (12), reference="D1", value="PRTR5V0U2X", rotation=90, mirror="None")
add_schematic_symbol(symbol_lib="Connector", symbol_name="SMA", pos_x=center_x_1 + (60), pos_y=center_y_1 + (20), reference="J1", value="SMA", rotation=90, mirror="None")

### Placing all global labels in the Schematic and connect them to the neighbor pin ###

# Add label GEOFENCE next to U1 pin RESETB 
x_U1_7, y_U1_7 = get_pin_location(symbol_ref="U1", pin_name="RESETB")
add_label(label_pos=[x_U1_7+(-15), y_U1_7+(0)], label_text="GEOFENCE", label_ref="GEOFENCE_0", label_type="input", text_orient="left")
# Connecting Label GEOFENCE label_id:0 to U1 pin RESETB (Pin ID 7 -- Name RESETB)
connect_pins("GEOFENCE_0", "1", "U1", "RESETB")

# Add label SCL{slash}CLK1 next to U1 pin RTK_SCL 
x_U1_37, y_U1_37 = get_pin_location(symbol_ref="U1", pin_name="RTK_SCL")
add_label(label_pos=[x_U1_37+(10), y_U1_37+(0)], label_text="SCL{slash}CLK1", label_ref="SCL{slash}CLK1_0", label_type="input", text_orient="right")
# Connecting Label SCL{slash}CLK1 label_id:0 to U1 pin RTK_SCL (Pin ID 37 -- Name RTK_SCL)
connect_pins("SCL{slash}CLK1_0", "1", "U1", "RTK_SCL")

# Add label TIMEPULSE next to U1 pin TIMEPULSE 
x_U1_35, y_U1_35 = get_pin_location(symbol_ref="U1", pin_name="TIMEPULSE")
add_label(label_pos=[x_U1_35+(-15), y_U1_35+(0)], label_text="TIMEPULSE", label_ref="TIMEPULSE_0", label_type="input", text_orient="left")
# Connecting Label TIMEPULSE label_id:0 to U1 pin TIMEPULSE (Pin ID 35 -- Name TIMEPULSE)
connect_pins("TIMEPULSE_0", "1", "U1", "TIMEPULSE")

# Add label RXD{slash}TP_IO2 next to U1 pin TP_RTC_PD0 
x_U1_34, y_U1_34 = get_pin_location(symbol_ref="U1", pin_name="TP_RTC_PD0")
add_label(label_pos=[x_U1_34+(-15), y_U1_34+(0)], label_text="RXD{slash}TP_IO2", label_ref="RXD{slash}TP_IO2_0", label_type="input", text_orient="left")
# Connecting Label RXD{slash}TP_IO2 label_id:0 to U1 pin TP_RTC_PD0 (Pin ID 34 -- Name TP_RTC_PD0)
connect_pins("RXD{slash}TP_IO2_0", "1", "U1", "TP_RTC_PD0")

# Add label TXD{slash}TP_IO1 next to U1 pin TP_RTC_PD1 
x_U1_33, y_U1_33 = get_pin_location(symbol_ref="U1", pin_name="TP_RTC_PD1")
add_label(label_pos=[x_U1_33+(-15), y_U1_33+(0)], label_text="TXD{slash}TP_IO1", label_ref="TXD{slash}TP_IO1_0", label_type="input", text_orient="left")
# Connecting Label TXD{slash}TP_IO1 label_id:0 to U1 pin TP_RTC_PD1 (Pin ID 33 -- Name TP_RTC_PD1)
connect_pins("TXD{slash}TP_IO1_0", "1", "U1", "TP_RTC_PD1")

# Add label RTK_MOSI next to U1 pin D_SEL1 
x_U1_30, y_U1_30 = get_pin_location(symbol_ref="U1", pin_name="D_SEL1")
add_label(label_pos=[x_U1_30+(-15), y_U1_30+(0)], label_text="RTK_MOSI", label_ref="RTK_MOSI_0", label_type="input", text_orient="left")
# Connecting Label RTK_MOSI label_id:0 to U1 pin D_SEL1 (Pin ID 30 -- Name D_SEL1)
connect_pins("RTK_MOSI_0", "1", "U1", "D_SEL1")


### Connecting all wires in the Schematic ###


# Connecting #PWR_+3V1 pin +3.3V (Pin ID 1 -- Name +3.3V) to U1 pin VCC (Pin ID 6 -- Name VCC)
connect_pins("#PWR_+3V1", "+3.3V", "U1", "VCC")

# Connecting #PWR1 pin 1 (Pin ID 1 -- Name None) to U1 pin ~{RESET} (Pin ID 16 -- Name ~{RESET})
connect_pins("#PWR1", "1", "U1", "~{RESET}")

# Connecting U1 pin TXD (Pin ID 36 -- Name TXD) to D1 pin RXI (Pin ID 1 -- Name RXI)
connect_pins("U1", "TXD", "D1", "RXI")

# Connecting D1 pin TXO (Pin ID 6 -- Name TXO) to U1 pin RXD (Pin ID 5 -- Name RXD)
connect_pins("D1", "TXO", "U1", "RXD")

# Connecting D1 pin TXD/TP_IO0 (Pin ID 3 -- Name TXD/TP_IO0) to U1 pin TP_SPI_POCI (Pin ID 40 -- Name TP_SPI_POCI)
connect_pins("D1", "TXD/TP_IO0", "U1", "TP_SPI_POCI")

# Connecting D1 pin A5/GPIO4 (Pin ID 9 -- Name A5/GPIO4) to U1 pin SDA (Pin ID 31 -- Name SDA)
connect_pins("D1", "A5/GPIO4", "U1", "SDA")

# Connecting D1 pin A6/GPIO3 (Pin ID 10 -- Name A6/GPIO3) to U1 pin SCL (Pin ID 37 -- Name SCL)
connect_pins("D1", "A6/GPIO3", "U1", "SCL")

# Connecting U1 pin D_SEL1 (Pin ID 28 -- Name D_SEL1) to D1 pin RXD/TOCI (Pin ID 2 -- Name RXD/TOCI)
connect_pins("U1", "D_SEL1", "D1", "RXD/TOCI")

# Connecting U1 pin D_SEL0 (Pin ID 29 -- Name D_SEL0) to D1 pin D_SEL1 (Pin ID 4 -- Name D_SEL1)
connect_pins("U1", "D_SEL0", "D1", "D_SEL1")

# Connecting U1 pin TEST (Pin ID 12 -- Name TEST) to D1 pin TXD/TP_IO1 (Pin ID 3 -- Name TXD/TP_IO1)
connect_pins("U1", "TEST", "D1", "TXD/TP_IO1")

# Connecting D1 pin A4/GPIO5 (Pin ID 8 -- Name A4/GPIO5) to U1 pin TEST (Pin ID 12 -- Name TEST)
connect_pins("D1", "A4/GPIO5", "U1", "TEST")

# Connecting U1 pin TP_RTC_PD0 (Pin ID 34 -- Name TP_RTC_PD0) to D1 pin RXD/TP_IO2 (Pin ID 2 -- Name RXD/TP_IO2)
connect_pins("U1", "TP_RTC_PD0", "D1", "RXD/TP_IO2")

# Connecting D1 pin A6/GPIO3 (Pin ID 10 -- Name A6/GPIO3) to U1 pin TP_RTC_PD1 (Pin ID 33 -- Name TP_RTC_PD1)
connect_pins("D1", "A6/GPIO3", "U1", "TP_RTC_PD1")

# Connecting U1 pin RTS/TOCL_POCI (Pin ID 39 -- Name RTS/TOCL_POCI) to D1 pin A3/GPIO2 (Pin ID 7 -- Name A3/GPIO2)
connect_pins("U1", "RTS/TOCL_POCI", "D1", "A3/GPIO2")

# Connecting U1 pin D_SEL1 (Pin ID 28 -- Name D_SEL1) to D1 pin A1/GPIO1 (Pin ID 6 -- Name A1/GPIO1)
connect_pins("U1", "D_SEL1", "D1", "A1/GPIO1")

# Connecting D1 pin GP_IO2/PERIPHERIAL_POWER (Pin ID 17 -- Name GP_IO2/PERIPHERIAL_POWER) to D1 pin D_SEL0 (Pin ID 4 -- Name D_SEL0)
connect_pins("D1", "GP_IO2/PERIPHERAL_POWER", "D1", "D_SEL0")

# Connecting D1 pin GP_IO2/PERIPHERIAL_POWER (Pin ID 17 -- Name GP_IO2/PERIPHERIAL_POWER) to D1 pin RTK_SCL (Pin ID 13 -- Name RTK_SCL)
connect_pins("D1", "GP_IO2/PERIPHERAL_POWER", "D1", "RTK_SCL")

# Connecting D1 pin A5/GPIO4 (Pin ID 9 -- Name A5/GPIO4) to D1 pin A4/GPIO5 (Pin ID 8 -- Name A4/GPIO5)
connect_pins("D1", "A5/GPIO4", "D1", "A4/GPIO5")

# Connecting D1 pin A3/GPIO2 (Pin ID 7 -- Name A3/GPIO2) to D1 pin A6/GPIO3 (Pin ID 10 -- Name A6/GPIO3)
connect_pins("D1", "A3/GPIO2", "D1", "A6/GPIO3")

# Connecting D1 pin A2/GPIO0 (Pin ID 5 -- Name A2/GPIO0) to D1 pin A4/GPIO5 (Pin ID 8 -- Name A4/GPIO5)
connect_pins("D1", "A2/GPIO0", "D1", "A4/GPIO5")

# Connecting D1 pin GP_IO2/PERIPHERAL_POWER (Pin ID 17 -- Name GP_IO2/PERIPHERAL_POWER) to D1 pin RXD/TOCI (Pin ID 2 -- Name RXD/TOCI)
connect_pins("D1", "GP_IO2/PERIPHERAL_POWER", "D1", "RXD/TOCI")

# Connecting D1 pin USBF- (Pin ID 3 -- Name USBF-) to D1 pin RXD/TP_IO1 (Pin ID 3 -- Name RXD/TP_IO1)
connect_pins("D1", "USBF-", "D1", "RXD/TP_IO1")

# Connecting D1 pin USBF+ (Pin ID 4 -- Name USBF+) to D1 pin TXD/TP_IO0 (Pin ID 1 -- Name TXD/TP_IO0)
connect_pins("D1", "USBF+", "D1", "TXD/TP_IO0")

# Connecting D1 pin GP_IO2/PERIPHERAL_POWER (Pin ID 17 -- Name GP_IO2/PERIPHERAL_POWER) to D1 pin RTK_MOSI (Pin ID 11 -- Name RTK_MOSI)
connect_pins("D1", "GP_IO2/PERIPHERAL_POWER", "D1", "RTK_MOSI")

# Connecting D1 pin GP_IO2/PERIPHERAL_POWER (Pin ID 17 -- Name GP_IO2/PERIPHERAL_POWER) to D1 pin A1/GPIO1 (Pin ID 6 -- Name A1/GPIO1)
connect_pins("D1", "GP_IO2/PERIPHERAL_POWER", "D1", "A1/GPIO1")

# Connecting D1 pin A2/GPIO0 (Pin ID 5 -- Name A2/GPIO0) to D1 pin RTK_MOSI (Pin ID 11 -- Name RTK_MOSI)
connect_pins("D1", "A2/GPIO0", "D1", "RTK_MOSI")

# Connecting D1 pin TXD/TP_IO0 (Pin ID 1 -- Name TXD/TP_IO0) to D1 pin D_SEL1 (Pin ID 4 -- Name D_SEL1)
connect_pins("D1", "TXD/TP_IO0", "D1", "D_SEL1")

# Connecting D1 pin GP_IO2/PERIPHERAL_POWER (Pin ID 17 -- Name GP_IO2/PERIPHERAL_POWER) to D1 pin A6/GPIO3 (Pin ID 10 -- Name A6/GPIO3)
connect_pins("D1", "GP_IO2/PERIPHERAL_POWER", "D1", "A6/GPIO3")

# Connecting U1 pin RXD (Pin ID 5 -- Name RXD) to D1 pin RXD/TOCI (Pin ID 2 -- Name RXD/TOCI)
connect_pins("U1", "RXD", "D1", "RXD/TOCI")

# Connecting D1 pin A3/GPIO2 (Pin ID 7 -- Name A3/GPIO2) to U1 pin RTS/TOCL_POCI (Pin ID 39 -- Name RTS/TOCL_POCI)
connect_pins("D1", "A3/GPIO2", "U1", "RTS/TOCL_POCI")

# Connecting U1 pin TXD (Pin ID 36 -- Name TXD) to D1 pin TXD/TP_IO0 (Pin ID 1 -- Name TXD/TP_IO0)
connect_pins("U1", "TXD", "D1", "TXD/TP_IO0")

# Connecting D1 pin TXO (Pin ID 6 -- Name TXO) to U1 pin RXD (Pin ID 5 -- Name RXD)
connect_pins("D1", "TXO", "U1", "RXD")

# Connecting #PWR_+3V1 pin +3.3V (Pin ID 1 -- Name +3.3V) to U1 pin VCC (Pin ID 6 -- Name VCC)
connect_pins("#PWR_+3V1", "+3.3V", "U1", "VCC")

# Connecting U1 pin RTS/TOCL_POCI (Pin ID 39 -- Name RTS/TOCL_POCI) to D1 pin A4/GPIO5 (Pin ID 8 -- Name A4/GPIO5)
connect_pins("U1", "RTS/TOCL_POCI", "D1", "A4/GPIO5")

# Connecting #PWR_+3V1 pin +3.3V (Pin ID 1 -- Name +3.3V) to D1 pin +3V3 (Pin ID 5 -- Name +3V3)
connect_pins("#PWR_+3V1", "+3.3V", "D1", "+3V3")

# Connecting U1 pin TP_RTC_PD0 (Pin ID 34 -- Name TP_RTC_PD0) to D1 pin RXD/TP_IO2 (Pin ID 2 -- Name RXD/TP_IO2)
connect_pins("U1", "TP_RTC_PD0", "D1", "RXD/TP_IO2")

# Connecting D1 pin +9V (Pin ID 7 -- Name +9V) to D1 pin D1 (Pin ID 12 -- Name D1)
connect_pins("D1", "+9V", "D1", "D1")

# Connecting D1 pin D0 (Pin ID 15 -- Name D0) to R9 pin 1 (Pin ID 1 -- Name None)
connect_pins("D1", "D0", "R9", "1")

# Connecting #PWR_+3V1 pin +3.3V (Pin ID 1 -- Name +3.3V) to D1 pin +3V3 (Pin ID 5 -- Name +3V3)
connect_pins("#PWR_+3V1", "+3.3V", "D1", "+3V3")

# Connecting U1 pin A0/GPIO2 (Pin ID 31 -- Name A0/GPIO2) to D1 pin A3/GPIO2 (Pin ID 7 -- Name A3/GPIO2)
connect_pins("U1", "A0/GPIO2", "D1", "A3/GPIO2")

# Connecting D1 pin D0 (Pin ID 15 -- Name D0) to D1 pin D0 (Pin ID 15 -- Name D0)
connect_pins("D1", "D0", "D1", "D0")

# Connecting D1 pin D0 (Pin ID 15 -- Name D0) to D1 pin GP_IO2/PERIPHERAL_POWER (Pin ID 17 -- Name GP_IO2/PERIPHERAL_POWER)
connect_pins("D1", "D0", "D1", "GP_IO2/PERIPHERAL_POWER")

# Connecting U1 pin D_SEL0 (Pin ID 29 -- Name D_SEL0) to D1 pin RTK_MOSI (Pin ID 11 -- Name RTK_MOSI)
connect_pins("U1", "D_SEL0", "D1", "RTK_MOSI")

# Connecting U1 pin D_SEL0 (Pin ID 29 -- Name D_SEL0) to D1 pin A2/GPIO0 (Pin ID 5 -- Name A2/GPIO0)
connect_pins("U1", "D_SEL0", "D1", "A2/GPIO0")

# Connecting D1 pin A6/GPIO3 (Pin ID 10 -- Name A6/GPIO3) to U1 pin SDA (Pin ID 31 -- Name SDA)
connect_pins("D1", "A6/GPIO3", "U1", "SDA")

# Connecting U1 pin RTS/TOCL_POCI (Pin ID 39 -- Name RTS/TOCL_POCI) to D1 pin D_SEL1 (Pin ID 4 -- Name D_SEL1)
connect_pins("U1", "RTS/TOCL_POCI", "D1", "D_SEL1")

# Connecting D1 pin TXD/TP_IO1 (Pin ID 3 -- Name TXD/TP_IO1) to U1 pin RTK_SCL (Pin ID 37 -- Name RTK_SCL)
connect_pins("D1", "TXD/TP_IO1", "U1", "RTK_SCL")

# Connecting U1 pin RXD (Pin ID 5 -- Name RXD) to D1 pin RXD/TOCI (Pin ID 2 -- Name RXD/TOCI)
connect_pins("U1", "RXD", "D1", "RXD/TOCI")

# Connecting D1 pin TXD/TP_IO0 (Pin ID 1 -- Name TXD/TP_IO0) to U1 pin D_SEL1 (Pin ID 28 -- Name D_SEL1)
connect_pins("D1", "TXD/TP_IO0", "U1", "D_SEL1")

write_out_all_wires()