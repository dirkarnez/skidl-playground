from skidl import *
import matplotlib.pyplot as plt

from skidl.pyspice import *

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

# =============================


vcc = Part("Device", "Battery", value=5 @ u_V)
r1 = Part("Device", "R", value=1 @ u_kOhm)
r2 = Part("Device", "R", value=2 @ u_kOhm)

vcc.convert_for_spice(V, {1: "p", 2: "n"})
r1.convert_for_spice(R, {1: "p", 2: "n"})
r2.convert_for_spice(R, {1: "p", 2: "n"})

vin, vout, gnd = Net("Vin"), Net("Vout"), Net("GND")
vin.netio = "i"
vout.netio = "o"
gnd.netio = "o"

gnd & vcc["n p"] & vin & r1 & vout & r2 & gnd

# generate_svg() need graphviz

set_default_tool(SPICE)
circ = generate_netlist()
print(circ)
sim = circ.simulator()
analysis = sim.dc(V1=slice(0, 5, 0.5))

dc_vin = analysis.Vin
dc_vout = analysis.Vout

print("{:^7s}{:^7s}".format("Vin (V)", " Vout (V)"))
print("=" * 15)
for v, i in zip(dc_vin.as_ndarray(), dc_vout.as_ndarray()):
    print("{:6.2f} {:6.2f}".format(v, i))


# =============================

lib_search_paths[SPICE].append("SpiceLib")


###############################################################################
# NCP1117 voltage regulator.
###############################################################################

reset()
gnd = Net("0")
lib_search_paths[SPICE].append("SpiceLib")
vin = V(dc_value=8 @ u_V)  # Input power supply
splib = SchLib("NCP1117") # 
vreg = Part(splib, "ncp1117_33-x")  # Voltage regulator.
r = R(value=470 @ u_Ohm)
print(vreg)
vreg["IN", "OUT"] += vin["p"], r[1]
gnd += vin["n"], r[2], vreg["GND"]
print(gnd)
print(vreg["IN"].net)
print(vreg["OUT"].net)
print(node(vreg["IN"]))
print(node(vin["p"]))

# Simulate the voltage regulator subcircuit.
circ = generate_netlist(
    libs="SpiceLib"
)  # Pass-in the library where the voltage regulator subcircuit is stored.
sim = circ.simulator()
dc_vals = sim.dc(**{vin.ref: slice(0, 10, 0.1)})

# Get the input and output voltages.
inp = dc_vals[node(vin["p"])]
outp = dc_vals[node(vreg["OUT"])]

# Plot the input and output waveforms. The output will be the inverse of the input since it passed
# through three inverters.
figure = plt.figure(1)
plt.title("Output Voltage vs. Input Voltage")
plt.xlabel("Input Voltage (V)")
plt.ylabel("Output Voltage (V)")
plt.plot(inp, outp)
plt.show()