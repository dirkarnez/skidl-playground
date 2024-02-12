from skidl import *

set_default_tool(KICAD)

gnd = Net('GND')  # Ground reference.
vin = Net('VI')   # Input voltage to the divider.
vout = Net('VO')  # Output voltage from the divider.
r1, r2 = 2 * Part('Device', 'R', TEMPLATE)  # Create two resistors.
r1.value, r1.footprint = '1K',  'Resistor_SMD:R_0805_2012Metric'  # Set resistor values
r2.value, r2.footprint = '500', 'Resistor_SMD:R_0805_2012Metric'  # and footprints.
r1[1] += vin      # Connect the input to the first resistor.
r2[2] += gnd      # Connect the second resistor to ground.
vout += r1[2], r2[1]  # Output comes from the connection of the two resistors.

generate_netlist()