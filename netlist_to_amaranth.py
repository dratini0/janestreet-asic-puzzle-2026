#!/usr/bin/env python3


import json
from argparse import ArgumentParser
from collections import Counter
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import TypedDict, cast

OUTPUT_PINS = {"X", "Y", "Q", "HI", "LO"}


class JsonGate(TypedDict):
    id: int
    typename: str
    x: float
    y: float
    connections: dict[str, str]


class JsonNetlist(TypedDict):
    name: str
    pins: list[str]
    internal_wires: list[str]
    gates: list[JsonGate]


@dataclass
class Gate:
    typename: str
    x: float
    y: float
    inputs: dict[str, str]
    output_netname: str


def main(_in: Path, out: Path):
    with _in.open("rt") as f:
        netlist = cast(JsonNetlist, json.load(f))

    netlist["pins"].sort()

    # Discard fanout information from gate names
    json_gates: list[JsonGate] = [
        {**gate, "typename": "_".join(gate["typename"].split("_")[:-1])}
        for gate in netlist["gates"]
    ]

    # Split the annoying 2-input gates (apparently, they are the constant 0/1 things)
    json_gates: list[JsonGate] = list(
        chain.from_iterable(
            (
                [
                    {
                        **gate,
                        "typename": "custom__const0",
                        "connections": {"X": gate["connections"]["LO"]},
                    },
                    {
                        **gate,
                        "typename": "custom__const1",
                        "connections": {"X": gate["connections"]["HI"]},
                    },
                ]
                if gate["typename"] == "sky130_fd_sc_hd__conb"
                else [gate]
            )
            for gate in json_gates
        )
    )

    # Prune output-less gates (and sanity-check)
    assert (
        max(
            len(OUTPUT_PINS.intersection(gate["connections"].keys()))
            for gate in json_gates
        )
        == 1
    ), "No multi-out gates"
    pruned_gates_counter = Counter(
        gate["typename"]
        for gate in json_gates
        if len(OUTPUT_PINS.intersection(gate["connections"].keys())) == 0
    )
    print(f"Pruning gates: {pruned_gates_counter}")
    json_gates = [
        gate
        for gate in json_gates
        if len(OUTPUT_PINS.intersection(gate["connections"].keys())) != 0
    ]

    gates: dict[str, Gate] = {
        f"{gate['typename']}_id_{gate["id"]}": Gate(
            typename=gate["typename"],
            x=gate["x"],
            y=gate["y"],
            inputs={
                k: v for k, v in gate["connections"].items() if k not in OUTPUT_PINS
            },
            output_netname=next(
                v for k, v in gate["connections"].items() if k in OUTPUT_PINS
            ),
        )
        for gate in json_gates
    }

    # Hack: Net 1447 is left floating, which Amaranth won't handle nicely. So, make it an input instead, which the verilog wrapper can leave floating (or tie to something meaningful)
    # This only applies in the puzzle, however.
    if _in.stem == "puzzle_nets":
        netlist["internal_wires"].remove("net_1447")
        netlist["pins"].append("net_1447")

    assert len({gate.output_netname for gate in gates.values()}) == len(gates), (
        "No nets driven from multiple gates"
    )

    net_drivers = {gate.output_netname: name for name, gate in gates.items()}

    assert not (set(netlist["internal_wires"]) - net_drivers.keys()), "No undriven nets"

    inputs = [pin for pin in netlist["pins"] if pin not in net_drivers]

    for pin in inputs:
        gates[pin] = Gate(
            typename="custom__input",
            x=0.0,
            y=0.0,
            inputs={},
            output_netname=pin,
        )

    outputs = {pin: net_drivers[pin] for pin in netlist["pins"] if pin not in net_drivers}

    # Removing clock buffers
    # Create clock enables (?)
    # Segment to lumps
    # Write Amaranth to file


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("netlist", type=Path)
    parser.add_argument("amaranth", type=Path)
    args = parser.parse_args()
    main(args.netlist, args.amaranth)
