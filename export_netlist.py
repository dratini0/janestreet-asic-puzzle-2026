# Enter your Python code here

import json

import pya

IGNORED_NETS = {"VPWR", "VGND"}
IGNORED_GATES = {"sky130_fd_sc_hd__tapvpwrvgnd_1", "sky130_fd_sc_hd__decap_3", "sky130_fd_sc_hd__diode_2"}


def name_net(net: pya.Net) -> str:
    if net.name:
        return net.name
    else:
        return f"net_{net.cluster_id}"


current_l2ndb = pya.Application.instance().main_window().current_view().l2ndb(0)
print(f"Analyzing {current_l2ndb.description}")

netlist = current_l2ndb.netlist()

top_circuit = netlist.top_circuit()


# Filter out VPWR, VGND, and floating nets from the logo
# Encoded assumption: nothing is tied high or low by just being connected to VPWR or VGND, they always use a conb cell
# We can safely infer that there is only one power domain, however.
nets = [
    net
    for net in top_circuit.each_net()
    if net.name not in IGNORED_NETS and net.subcircuit_pin_count() != 0
]

pins = [name_net(net) for net in nets if net.name]
internal_wires = [name_net(net) for net in nets if not net.name]

gates = []

for gate in top_circuit.each_subcircuit():
    circuit = gate.circuit_ref()
    typename = circuit.name
    if not typename.startswith("sky130"):
        continue
    if typename in IGNORED_GATES:
        continue
    location = gate.trans * circuit.boundary.bbox().center()
    connections = {
        pin.name(): name_net(gate.net_for_pin(pin.id()))
        for pin in circuit.each_pin()
        if pin.name() and pin.name() not in IGNORED_NETS
    }
    gates.append(
        {
            "typename": typename,
            "x": location.x,
            "y": location.y,
            "connections": connections,
        }
    )

with open(f"{top_circuit.name}_nets.json", "wt") as f:
    json.dump(
        {
            "name": top_circuit.name,
            "pins": pins,
            "internal_wires": internal_wires,
            "gates": gates,
        },
        f,
        indent=2,
    )

