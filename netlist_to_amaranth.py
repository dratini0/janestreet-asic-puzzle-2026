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


def prune(gates: dict[str, Gate], outputs: dict[str, str]) -> dict[str, Gate]:
    reachable = set()
    frontier = set(outputs.values())
    while frontier:
        current = frontier.pop()
        reachable.add(current)
        for input_gate in gates[current].inputs.values():
            if input_gate not in reachable:
                frontier.add(input_gate)

    unreachable = Counter(
        gate.typename for name, gate in gates.items() if name not in reachable
    )
    print(f"Pruning gates: {unreachable}")

    result = {name: gate for name, gate in gates.items() if name in reachable}
    print(f"Remaining gates: {len(result)}")

    return result


def pretty_print_combinatorial_expression(gates: dict[str, Gate], gate_name: str) -> str:
    gate = gates[gate_name]

    def recurse(pin: str) -> str:
        # The oldest macro-processing trick in the book: we need to bracket this
        # to avoid weird precedence issues
        return f"({pretty_print_combinatorial_expression(gates, gate.inputs[pin])})"

    if gate.typename in {
        "custom__input",
        "sky130_fd_sc_hd__dfrtp",
        "sky130_fd_sc_hd__dfstp",
        "sky130_fd_sc_hd__dfxtp",
        "custom__dfre",
        "custom__dfse",
        "custom__dfe",
    }:
        result = gate.output_netname
    elif gate.typename in {"custom__const0", "custom__const1"}:
        result = gate.output_netname.upper()
    elif gate.typename == "sky130_fd_sc_hd__and2":
        result = f"{recurse('A')} & {recurse('B')}"
    elif gate.typename == "sky130_fd_sc_hd__and3":
        result = f"{recurse('A')} & {recurse('B')} & {recurse('C')}"
    elif gate.typename == "sky130_fd_sc_hd__and4":
        result = f"{recurse('A')} & {recurse('B')} & {recurse('C')} & {recurse('D')}"
    elif gate.typename == "sky130_fd_sc_hd__or2":
        result = f"{recurse('A')} | {recurse('B')}"
    elif gate.typename == "sky130_fd_sc_hd__or3":
        result = f"{recurse('A')} | {recurse('B')} | {recurse('C')}"
    elif gate.typename == "sky130_fd_sc_hd__or4":
        result = f"{recurse('A')} | {recurse('B')} | {recurse('C')} | {recurse('D')}"
    elif gate.typename == "sky130_fd_sc_hd__and2b":
        result = f"~{recurse('A_N')} & {recurse('B')}"
    elif gate.typename == "sky130_fd_sc_hd__and3b":
        result = f"~{recurse('A_N')} & {recurse('B')} & {recurse('C')}"
    elif gate.typename == "sky130_fd_sc_hd__and4b":
        result = f"~{recurse('A_N')} & {recurse('B')} & {recurse('C')} & {recurse('D')}"
    elif gate.typename == "sky130_fd_sc_hd__and4bb":
        result = (
            f"~{recurse('A_N')} & ~{recurse('B_N')} & {recurse('C')} & {recurse('D')}"
        )
    elif gate.typename == "sky130_fd_sc_hd__or2b":
        result = f"{recurse('A')} | ~{recurse('B_N')}"
    elif gate.typename == "sky130_fd_sc_hd__or3b":
        result = f"{recurse('A')} | {recurse('B')} | ~{recurse('C_N')}"
    elif gate.typename == "sky130_fd_sc_hd__or4b":
        result = f"{recurse('A')} | {recurse('B')} | {recurse('C')} | ~{recurse('D_N')}"
    elif gate.typename == "sky130_fd_sc_hd__or4bb":
        result = (
            f"{recurse('A')} | ~{recurse('B')} | ~{recurse('C_N')} | ~{recurse('D_N')}"
        )
    elif gate.typename == "sky130_fd_sc_hd__nand2":
        result = f"~({recurse('A')} & {recurse('B')})"
    elif gate.typename == "sky130_fd_sc_hd__nand3":
        result = f"~({recurse('A')} & {recurse('B')} & {recurse('C')})"
    elif gate.typename == "sky130_fd_sc_hd__nand4":
        result = f"~({recurse('A')} & {recurse('B')} & {recurse('C')} & {recurse('D')})"
    elif gate.typename == "sky130_fd_sc_hd__nor2":
        result = f"~({recurse('A')} | {recurse('B')})"
    elif gate.typename == "sky130_fd_sc_hd__nor3":
        result = f"~({recurse('A')} | {recurse('B')} | {recurse('C')})"
    elif gate.typename == "sky130_fd_sc_hd__nor4":
        result = f"~({recurse('A')} | {recurse('B')} | {recurse('C')} | {recurse('D')})"
    elif gate.typename == "sky130_fd_sc_hd__nand2b":
        result = f"~(~{recurse('A_N')} & {recurse('B')})"
    elif gate.typename == "sky130_fd_sc_hd__nand3b":
        result = f"~(~{recurse('A_N')} & {recurse('B')} & {recurse('C')})"
    elif gate.typename == "sky130_fd_sc_hd__nand4b":
        result = (
            f"~(~{recurse('A_N')} & {recurse('B')} & {recurse('C')} & {recurse('D')})"
        )
    elif gate.typename == "sky130_fd_sc_hd__nand4bb":
        result = f"~(~{recurse('A_N')} & ~{recurse('B_N')} & {recurse('C')} & {recurse('D')})"
    elif gate.typename == "sky130_fd_sc_hd__nor2b":
        result = f"~({recurse('A')} | ~{recurse('B_N')})"
    elif gate.typename == "sky130_fd_sc_hd__nor3b":
        result = f"~({recurse('A')} | {recurse('B')} | ~{recurse('C_N')})"
    elif gate.typename == "sky130_fd_sc_hd__nor4b":
        result = (
            f"~({recurse('A')} | {recurse('B')} | {recurse('C')} | ~{recurse('D_N')})"
        )
    elif gate.typename == "sky130_fd_sc_hd__nor4bb":
        result = f"~({recurse('A')} | ~{recurse('B')} | ~{recurse('C_N')} | ~{recurse('D_N')})"
    elif gate.typename == "sky130_fd_sc_hd__xnor3":
        result = f"~({recurse('A')} ^ {recurse(pin='B')} ^ {recurse('C')})"
    elif gate.typename == "sky130_fd_sc_hd__inv":
        result = f"~{recurse('A')}"
    elif gate.typename == "sky130_fd_sc_hd__mux2":
        result = f"Mux({recurse('S')}, {recurse('A1')}, {recurse('A0')})"
    elif gate.typename == "sky130_fd_sc_hd__buf":
        result = f"Buf({recurse('A')})"
    # Edited version of https://github.com/TinyTapeout/tt-support-tools/blob/main/tech/sky130A/cells.json
    elif gate.typename == "sky130_fd_sc_hd__o31ai":
        result = f"~(({recurse('A1')} | {recurse('A2')} | {recurse('A3')}) & {recurse('B1')})"
    elif gate.typename == "sky130_fd_sc_hd__a221o":
        result = f"(({recurse('A1')} & {recurse('A2')}) | ({recurse('B1')} & {recurse('B2')}) | {recurse('C1')})"
    elif gate.typename == "sky130_fd_sc_hd__a2111oi":
        result = f"~(({recurse('A1')} & {recurse('A2')}) | {recurse('B1')} | {recurse('C1')} | {recurse('D1')})"
    elif gate.typename == "sky130_fd_sc_hd__a21bo":
        result = f"(({recurse('A1')} & {recurse('A2')}) | (~{recurse('B1_N')}))"
    elif gate.typename == "sky130_fd_sc_hd__o31a":
        result = (
            f"(({recurse('A1')} | {recurse('A2')} | {recurse('A3')}) & {recurse('B1')})"
        )
    elif gate.typename == "sky130_fd_sc_hd__o221a":
        result = f"(({recurse('A1')} | {recurse('A2')}) & ({recurse('B1')} | {recurse('B2')}) & {recurse('C1')})"
    elif gate.typename == "sky130_fd_sc_hd__o32ai":
        result = f"~(({recurse('A1')} | {recurse('A2')} | {recurse('A3')}) & ({recurse('B1')} | {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__a21oi":
        result = f"~(({recurse('A1')} & {recurse('A2')}) | {recurse('B1')})"
    elif gate.typename == "sky130_fd_sc_hd__a21boi":
        result = f"~(({recurse('A1')} & {recurse('A2')}) | (~{recurse('B1_N')}))"
    elif gate.typename == "sky130_fd_sc_hd__a311oi":
        result = f"~(({recurse('A1')} & {recurse('A2')} & {recurse('A3')}) | {recurse('B1')} | {recurse('C1')})"
    elif gate.typename == "sky130_fd_sc_hd__lpflow_inputiso0p":
        result = f"({recurse('A')} & ~{recurse('SLEEP_B')})"
    elif gate.typename == "sky130_fd_sc_hd__a32o":
        result = f"(({recurse('A1')} & {recurse('A2')} & {recurse('A3')}) | ({recurse('B1')} & {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__a22o":
        result = f"(({recurse('A1')} & {recurse('A2')}) | ({recurse('B1')} & {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__o2111a":
        result = f"(({recurse('A1')} | {recurse('A2')}) & {recurse('B1')} & {recurse('C1')} & {recurse('D1')})"
    elif gate.typename == "sky130_fd_sc_hd__lpflow_inputiso0n":
        result = f"({recurse('A')} & {recurse('SLEEP_B')})"
    elif gate.typename == "sky130_fd_sc_hd__o21ba":
        result = f"(({recurse('A1')} | {recurse('A2')}) & ~{recurse('B1_N')})"
    elif gate.typename == "sky130_fd_sc_hd__a21o":
        result = f"(({recurse('A1')} & {recurse('A2')}) | {recurse('B1')})"
    elif gate.typename == "sky130_fd_sc_hd__a211o":
        result = (
            f"(({recurse('A1')} & {recurse('A2')}) | {recurse('B1')} | {recurse('C1')})"
        )
    elif gate.typename == "sky130_fd_sc_hd__a221oi":
        result = f"~(({recurse('A1')} & {recurse('A2')}) | ({recurse('B1')} & {recurse('B2')}) | {recurse('C1')})"
    elif gate.typename == "sky130_fd_sc_hd__a2bb2o":
        result = f"((~{recurse('A1')} & ~{recurse('A2')}) | ({recurse('B1')} & {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__a31o":
        result = (
            f"(({recurse('A1')} & {recurse('A2')} & {recurse('A3')}) | {recurse('B1')})"
        )
    elif gate.typename == "sky130_fd_sc_hd__a2bb2oi":
        result = f"~((~{recurse('A1')} & ~{recurse('A2')}) | ({recurse('B1')} & {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__o211a":
        result = (
            f"(({recurse('A1')} | {recurse('A2')}) & {recurse('B1')} & {recurse('C1')})"
        )
    elif gate.typename == "sky130_fd_sc_hd__o311a":
        result = f"(({recurse('A1')} | {recurse('A2')} | {recurse('A3')}) & {recurse('B1')} & {recurse('C1')})"
    elif gate.typename == "sky130_fd_sc_hd__o22a":
        result = f"(({recurse('A1')} | {recurse('A2')}) & ({recurse('B1')} | {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__o22ai":
        result = f"~(({recurse('A1')} | {recurse('A2')}) & ({recurse('B1')} | {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__a2111o":
        result = f"(({recurse('A1')} & {recurse('A2')}) | {recurse('B1')} | {recurse('C1')} | {recurse('D1')})"
    elif gate.typename == "sky130_fd_sc_hd__o2bb2a":
        result = f"(~({recurse('A1_N')} & {recurse('A2_N')}) & ({recurse('B1')} | {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__o2bb2ai":
        result = f"~(~({recurse('A1')} & {recurse('A2')}) & ({recurse('B1')} | {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__o32a":
        result = f"(({recurse('A1')} | {recurse('A2')} | {recurse('A3')}) & ({recurse('B1')} | {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__lpflow_inputiso1p":
        result = f"({recurse('A')} & ~{recurse('SLEEP')})"
    elif gate.typename == "sky130_fd_sc_hd__o21bai":
        result = f"~(({recurse('A1')} | {recurse('A2')}) & ~{recurse('B1_N')})"
    elif gate.typename == "sky130_fd_sc_hd__o2111ai":
        result = f"~(({recurse('A1')} | {recurse('A2')}) & {recurse('B1')} & {recurse('C1')} & {recurse('D1')})"
    elif gate.typename == "sky130_fd_sc_hd__xor3":
        result = f"{recurse('A')} ^ {recurse('B')} ^ {recurse('C')}"
    # Wrong!
    # elif gate.typename == "sky130_fd_sc_hd__nor2b":
    #     result = (
    #         f"~({recurse('A')} | {recurse('B')} | {recurse('C')} | ~{recurse('D')})"
    #     )
    elif gate.typename == "sky130_fd_sc_hd__o41ai":
        result = f"~(({recurse('A1')} | {recurse('A2')} | {recurse('A3')} | {recurse('A4')}) & {recurse('B1')})"
    elif gate.typename == "sky130_fd_sc_hd__a211oi":
        result = f"~(({recurse('A1')} & {recurse('A2')}) | {recurse('B1')} | {recurse('C1')})"
    # Wrong!
    # elif gate.typename == "sky130_fd_sc_hd__nor3":
    #     result = (
    #         f"~({recurse('A')} | {recurse('B')} | {recurse('C')} | ~{recurse('D')})"
    #     )
    elif gate.typename == "sky130_fd_sc_hd__a31oi":
        result = f"~(({recurse('A1')} & {recurse('A2')} & {recurse('A3')}) | {recurse('B1')})"
    elif gate.typename == "sky130_fd_sc_hd__o21ai":
        result = f"~(({recurse('A1')} | {recurse('A2')}) & {recurse('B1')})"
    elif gate.typename == "sky130_fd_sc_hd__lpflow_isobufsrckapwr":
        result = f"(~{recurse('A')} | {recurse('SLEEP')})"
    elif gate.typename == "sky130_fd_sc_hd__a22oi":
        result = f"~(({recurse('A1')} & {recurse('A2')}) | ({recurse('B1')} & {recurse('B2')}))"
    # elif gate.typename == "sky130_fd_sc_hd__nor4":
    #     result = f"~({recurse('A')} | {recurse('B')} | {recurse('C')} | {recurse('D')})"
    elif gate.typename == "sky130_fd_sc_hd__a222oi":
        result = f"~(({recurse('A1')} & {recurse('A2')}) | ({recurse('B1')} & {recurse('B2')}) | ({recurse('C1')} & {recurse('C2')}))"
    elif gate.typename == "sky130_fd_sc_hd__o21a":
        result = f"(({recurse('A1')} | {recurse('A2')}) & {recurse('B1')})"
    elif gate.typename == "sky130_fd_sc_hd__o211ai":
        result = f"~(({recurse('A1')} | {recurse('A2')}) & {recurse('B1')} & {recurse('C1')})"
    elif gate.typename == "sky130_fd_sc_hd__lpflow_isobufsrc":
        result = f"(~{recurse('A')} | {recurse('SLEEP')})"
    elif gate.typename == "sky130_fd_sc_hd__lpflow_inputiso1n":
        result = f"({recurse('A')} & {recurse('SLEEP_B')})"
    elif gate.typename == "sky130_fd_sc_hd__a32oi":
        result = f"~(({recurse('A1')} & {recurse('A2')} & {recurse('A3')}) | ({recurse('B1')} & {recurse('B2')}))"
    elif gate.typename == "sky130_fd_sc_hd__o41a":
        result = f"(({recurse('A1')} | {recurse('A2')} | {recurse('A3')} | {recurse('A4')}) & {recurse('B1')})"
    elif gate.typename == "sky130_fd_sc_hd__xor2":
        result = f"{recurse('A')} ^ {recurse('B')}"
    elif gate.typename == "sky130_fd_sc_hd__a41o":
        result = f"(({recurse('A1')} & {recurse('A2')} & {recurse('A3')} & {recurse('A4')}) | {recurse('B1')})"
    elif gate.typename == "sky130_fd_sc_hd__o221ai":
        result = f"~(({recurse('A1')} | {recurse('A2')}) & ({recurse('B1')} | {recurse('B2')}) & {recurse('C1')})"
    elif gate.typename == "sky130_fd_sc_hd__xnor2":
        result = f"~({recurse('A')} ^ {recurse('B')})"
    elif gate.typename == "sky130_fd_sc_hd__o311ai":
        result = f"~(({recurse('A1')} | {recurse('A2')} | {recurse('A3')}) & {recurse('B1')} & {recurse('C1')})"
    # elif gate.typename == "sky130_fd_sc_hd__nor3b":
    #     result = f"(~({recurse('A')} | {recurse('B')})) & ~{recurse('C')})"
    elif gate.typename == "sky130_fd_sc_hd__a311o":
        result = f"(({recurse('A1')} & {recurse('A2')} & {recurse('A3')}) | {recurse('B1')} | {recurse('C1')})"
    elif gate.typename == "sky130_fd_sc_hd__a41oi":
        result = f"~(({recurse('A1')} & {recurse('A2')} & {recurse('A3')} & {recurse('A4')}) | {recurse('B1')})"

    else:
        raise RuntimeError(f"Unsupported gate type {gate.typename}!")

    # This pretty-printing is potentially exponential with the number of gates,
    # and we have ~600 of those. Prevent an OOM, and I can't parse a 10K char
    # expression anyway.
    # Temporarily increased to 1M - that looks to be one funky boolean expression!
    if len(result) > 1_000_000:
        raise RuntimeError("Boolean expression too long")
    return result


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
    print(f"Pruning ouptut-less gates: {pruned_gates_counter}")
    json_gates = [
        gate
        for gate in json_gates
        if len(OUTPUT_PINS.intersection(gate["connections"].keys())) != 0
    ]

    gates: dict[str, Gate] = {
        f"{gate['typename']}_id_{gate['id']}": Gate(
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
        net_drivers[pin] = pin

    outputs = {pin: net_drivers[pin] for pin in netlist["pins"] if pin not in inputs}

    for gate in gates.values():
        gate.inputs = {pin: net_drivers[net] for pin, net in gate.inputs.items()}

    print("Pruning unused low/hide sides of conb cells")
    gates = prune(gates, outputs)

    # Removing clock buffers
    # Specifically, asserting that we on the same clock and reset domain
    # Footnote for Amaranth generation: Amaranth only supports synchronous reset, and these gates are asynchronous.
    # The test vectors will be designed so that this doesn't matter.
    for gate in gates.values():
        if gate.typename in {
            "sky130_fd_sc_hd__dfrtp",
            "sky130_fd_sc_hd__dfstp",
            "sky130_fd_sc_hd__dfxtp",
        }:
            if gate.typename == "sky130_fd_sc_hd__dfrtp":
                assert gate.inputs["RESET_B"] == "rst_n"
                del gate.inputs["RESET_B"]
            if gate.typename == "sky130_fd_sc_hd__dfstp":
                assert gate.inputs["SET_B"] == "rst_n"
                del gate.inputs["SET_B"]
            clock_source = gate.inputs["CLK"]
            while clock_source != "clk":
                clock_source_gate = gates[clock_source]
                assert clock_source_gate.typename == "sky130_fd_sc_hd__clkbuf"
                clock_source = clock_source_gate.inputs["A"]

            del gate.inputs["CLK"]

    print("Pruning clock and reset trees")
    gates = prune(gates, outputs)

    # Create clock enables (?)
    for name, gate in gates.items():
        if gate.typename in {
            "sky130_fd_sc_hd__dfrtp",
            "sky130_fd_sc_hd__dfstp",
            "sky130_fd_sc_hd__dfxtp",
        }:
            input_gate = gates[gate.inputs["D"]]
            if input_gate.typename == "sky130_fd_sc_hd__mux2":
                assert input_gate.inputs["A1"] != name, (
                    "inverted enable inputs not supported"
                )
                if input_gate.inputs["A0"] == name:
                    print(
                        f"Adding a clock enable ({input_gate.inputs['S']}) to a {gate.typename}"
                    )
                    gate.typename = {
                        "sky130_fd_sc_hd__dfrtp": "custom__dfre",
                        "sky130_fd_sc_hd__dfstp": "custom__dfse",
                        "sky130_fd_sc_hd__dfxtp": "custom__dfe",
                    }[gate.typename]
                    gate.inputs["D"] = input_gate.inputs["A1"]
                    gate.inputs["EN"] = input_gate.inputs["S"]

    print("Pruning muxes absorbed by clock enable'd flipflops")
    gates = prune(gates, outputs)

    # Segment to lumps
    # TODO
    # Write Amaranth to file
    # WIP
    with out.open("wt") as f:
        for pin, gate_name in outputs.items():
            f.write(f"{pin}: {pretty_print_combinatorial_expression(gates, gate_name)}\n")
        for gate in gates.values():
            if gate.typename in {
                "sky130_fd_sc_hd__dfrtp",
                "sky130_fd_sc_hd__dfstp",
                "sky130_fd_sc_hd__dfxtp",
            }:
                f.write(
                    f"{gate.output_netname}: {pretty_print_combinatorial_expression(gates, gate.inputs['D'])}\n"
                )
            if gate.typename in {
                "custom__dfre",
                "custom__dfse",
                "custom__dfe",
            }:
                f.write(
                    f"{gate.output_netname}: {pretty_print_combinatorial_expression(gates, gate.inputs['D'])}\n"
                )
                f.write(
                    f"{gate.output_netname}_en: {pretty_print_combinatorial_expression(gates, gate.inputs['EN'])}\n"
                )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("netlist", type=Path)
    parser.add_argument("amaranth", type=Path)
    args = parser.parse_args()
    main(args.netlist, args.amaranth)
