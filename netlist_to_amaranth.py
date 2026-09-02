#!/usr/bin/env python3


import io
import json
import re
from argparse import ArgumentParser, BooleanOptionalAction
from collections import Counter
from dataclasses import dataclass
from itertools import chain, groupby
from pathlib import Path
from typing import Self, TypedDict, cast

from matplotlib.ticker import MultipleLocator

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


@dataclass(frozen=True)
class OutputPolicy:
    fanout_limit: int  # 0 = unlimited


DEFAULT_OUTPUT_POLICY = OutputPolicy(fanout_limit=2)


@dataclass
class Gate:
    typename: str
    x: float
    y: float
    inputs: dict[str, str]
    output_netname: str


@dataclass
class Lump:
    name: str
    x0: float
    x1: float
    y0: float
    y1: float
    output_policy: OutputPolicy | None = None


# fmt: off
LUMPS = {
    "adder_demo": [
        Lump("ShiftRegisterA", 0.0, 50.0, 50.0, 100.0),
        Lump("ShiftRegisterB", 0.0, 50.0, 0.0, 50.0),
        Lump("Compare496", 50.0, 100.0, 42.0, 100.0),
        Lump("Add", 50.0, 100.0, 0.0, 42.0),
    ],
    "puzzle": [
        # Named after Sinnoh region towns, since I don't acctually know what
        # each one does yet

        # Column 1
        Lump("Floaroma", 0., 50., 180., 250.,),
        Lump("Jubilife", 0., 50., 125., 180.,),
        Lump("Twinleaf", 0., 50., 70., 125.,),
        # Column 2
        Lump("Snowpoint", 50., 100., 125., 180.,),
        Lump("Eterna", 50., 100., 70., 125.,),
        Lump("Oreburgh", 50., 100., 30., 70.,),
        Lump("Sandgem", 50., 100., 0., 30.,),
        # Column 3
        # I'm not sure these three are separate lumps, but let's try
        Lump("Celestic", 100., 140., 265., 300.),
        Lump("Hearthome", 100., 140., 195., 265.),
        Lump("Solaceon", 100., 140., 160., 195.),

        Lump("Pastoria", 100., 140., 30., 160.),
        # Column 4
        Lump("Veilstone", 140., 200., 265., 300.),
        Lump("Output_MtCoronet", 140., 200., 235., 265.),
        Lump("Output_EternaForest", 140., 200., 160., 235.),
        Lump("Output_LakeAcuity", 140., 200., 125., 160.),
        Lump("Output_LakeVerity", 140., 200., 105., 125.),
        Lump("Output_LakeValor", 140., 200., 70., 105.),
        Lump("Sunyshore", 140., 200., 0., 70.),
    ],
}
# fmt: on


def sanitize_identifier(name: str) -> str:
    return re.sub("[^a-zA-Z0-9]", "_", name)


@dataclass
class Module:
    name: str
    gates: dict[str, Gate]
    outputs: dict[str, str]
    output_policy: OutputPolicy = DEFAULT_OUTPUT_POLICY

    def prune(self):
        reachable = set()
        frontier = set(self.outputs.values())
        while frontier:
            current = frontier.pop()
            reachable.add(current)
            for input_gate in self.gates[current].inputs.values():
                if input_gate not in reachable:
                    frontier.add(input_gate)

        unreachable = Counter(
            gate.typename for name, gate in self.gates.items() if name not in reachable
        )
        print(f"Pruning gates: {unreachable}")

        result = {name: gate for name, gate in self.gates.items() if name in reachable}
        print(f"Remaining gates: {len(result)}")

        self.gates = result

    def pretty_print_combinatorial_expression(
        self, gate_name: str, intermediates: dict[str, str], *, use_intermediates=True
    ) -> str:
        gate = self.gates[gate_name]

        def recurse(pin: str) -> str:
            # The oldest macro-processing trick in the book: we need to bracket this
            # to avoid weird precedence issues
            return f"({self.pretty_print_combinatorial_expression(gate.inputs[pin], intermediates, use_intermediates=True)})"

        if gate.typename == "custom__input":
            result = f"self.{gate.output_netname}"
        elif gate.typename in {
            "sky130_fd_sc_hd__dfrtp",
            "sky130_fd_sc_hd__dfstp",
            "sky130_fd_sc_hd__dfxtp",
            "custom__dfre",
            "custom__dfse",
            "custom__dfe",
        }:
            result = f"self._{gate.output_netname}"
        elif gate.typename == "custom__const0":
            result = "0"
        elif gate.typename == "custom__const1":
            result = "1"
        elif use_intermediates and gate_name in intermediates:
            result = f"self._{intermediates[gate_name]}"
        elif gate.typename == "sky130_fd_sc_hd__and2":
            result = f"{recurse('A')} & {recurse('B')}"
        elif gate.typename == "sky130_fd_sc_hd__and3":
            result = f"{recurse('A')} & {recurse('B')} & {recurse('C')}"
        elif gate.typename == "sky130_fd_sc_hd__and4":
            result = (
                f"{recurse('A')} & {recurse('B')} & {recurse('C')} & {recurse('D')}"
            )
        elif gate.typename == "sky130_fd_sc_hd__or2":
            result = f"{recurse('A')} | {recurse('B')}"
        elif gate.typename == "sky130_fd_sc_hd__or3":
            result = f"{recurse('A')} | {recurse('B')} | {recurse('C')}"
        elif gate.typename == "sky130_fd_sc_hd__or4":
            result = (
                f"{recurse('A')} | {recurse('B')} | {recurse('C')} | {recurse('D')}"
            )
        elif gate.typename == "sky130_fd_sc_hd__and2b":
            result = f"~{recurse('A_N')} & {recurse('B')}"
        elif gate.typename == "sky130_fd_sc_hd__and3b":
            result = f"~{recurse('A_N')} & {recurse('B')} & {recurse('C')}"
        elif gate.typename == "sky130_fd_sc_hd__and4b":
            result = (
                f"~{recurse('A_N')} & {recurse('B')} & {recurse('C')} & {recurse('D')}"
            )
        elif gate.typename == "sky130_fd_sc_hd__and4bb":
            result = f"~{recurse('A_N')} & ~{recurse('B_N')} & {recurse('C')} & {recurse('D')}"
        elif gate.typename == "sky130_fd_sc_hd__or2b":
            result = f"{recurse('A')} | ~{recurse('B_N')}"
        elif gate.typename == "sky130_fd_sc_hd__or3b":
            result = f"{recurse('A')} | {recurse('B')} | ~{recurse('C_N')}"
        elif gate.typename == "sky130_fd_sc_hd__or4b":
            result = (
                f"{recurse('A')} | {recurse('B')} | {recurse('C')} | ~{recurse('D_N')}"
            )
        elif gate.typename == "sky130_fd_sc_hd__or4bb":
            result = f"{recurse('A')} | {recurse('B')} | ~{recurse('C_N')} | ~{recurse('D_N')}"
        elif gate.typename == "sky130_fd_sc_hd__nand2":
            result = f"~({recurse('A')} & {recurse('B')})"
        elif gate.typename == "sky130_fd_sc_hd__nand3":
            result = f"~({recurse('A')} & {recurse('B')} & {recurse('C')})"
        elif gate.typename == "sky130_fd_sc_hd__nand4":
            result = (
                f"~({recurse('A')} & {recurse('B')} & {recurse('C')} & {recurse('D')})"
            )
        elif gate.typename == "sky130_fd_sc_hd__nor2":
            result = f"~({recurse('A')} | {recurse('B')})"
        elif gate.typename == "sky130_fd_sc_hd__nor3":
            result = f"~({recurse('A')} | {recurse('B')} | {recurse('C')})"
        elif gate.typename == "sky130_fd_sc_hd__nor4":
            result = (
                f"~({recurse('A')} | {recurse('B')} | {recurse('C')} | {recurse('D')})"
            )
        elif gate.typename == "sky130_fd_sc_hd__nand2b":
            result = f"~(~{recurse('A_N')} & {recurse('B')})"
        elif gate.typename == "sky130_fd_sc_hd__nand3b":
            result = f"~(~{recurse('A_N')} & {recurse('B')} & {recurse('C')})"
        elif gate.typename == "sky130_fd_sc_hd__nand4b":
            result = f"~(~{recurse('A_N')} & {recurse('B')} & {recurse('C')} & {recurse('D')})"
        elif gate.typename == "sky130_fd_sc_hd__nand4bb":
            result = f"~(~{recurse('A_N')} & ~{recurse('B_N')} & {recurse('C')} & {recurse('D')})"
        elif gate.typename == "sky130_fd_sc_hd__nor2b":
            result = f"~({recurse('A')} | ~{recurse('B_N')})"
        elif gate.typename == "sky130_fd_sc_hd__nor3b":
            result = f"~({recurse('A')} | {recurse('B')} | ~{recurse('C_N')})"
        elif gate.typename == "sky130_fd_sc_hd__nor4b":
            result = f"~({recurse('A')} | {recurse('B')} | {recurse('C')} | ~{recurse('D_N')})"
        elif gate.typename == "sky130_fd_sc_hd__nor4bb":
            result = f"~({recurse('A')} | {recurse('B')} | ~{recurse('C_N')} | ~{recurse('D_N')})"
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
            result = f"(({recurse('A1')} | {recurse('A2')} | {recurse('A3')}) & {recurse('B1')})"
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
            result = f"(({recurse('A1')} & {recurse('A2')}) | {recurse('B1')} | {recurse('C1')})"
        elif gate.typename == "sky130_fd_sc_hd__a221oi":
            result = f"~(({recurse('A1')} & {recurse('A2')}) | ({recurse('B1')} & {recurse('B2')}) | {recurse('C1')})"
        elif gate.typename == "sky130_fd_sc_hd__a2bb2o":
            result = f"((~{recurse('A1')} & ~{recurse('A2')}) | ({recurse('B1')} & {recurse('B2')}))"
        elif gate.typename == "sky130_fd_sc_hd__a31o":
            result = f"(({recurse('A1')} & {recurse('A2')} & {recurse('A3')}) | {recurse('B1')})"
        elif gate.typename == "sky130_fd_sc_hd__a2bb2oi":
            result = f"~((~{recurse('A1')} & ~{recurse('A2')}) | ({recurse('B1')} & {recurse('B2')}))"
        elif gate.typename == "sky130_fd_sc_hd__o211a":
            result = f"(({recurse('A1')} | {recurse('A2')}) & {recurse('B1')} & {recurse('C1')})"
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

    def write_amaranth_module(self, f: io.Writer[str]):
        intermediates = {}

        for name, gate in self.gates.items():
            if gate.typename == "sky130_fd_sc_hd__buf":
                intermediates[name] = gate.output_netname

        if self.output_policy.fanout_limit > 0:
            fanouts = Counter(
                chain.from_iterable(
                    gate.inputs.values() for gate in self.gates.values()
                )
            )
            fanouts.update(self.outputs.values())

            for name, fanout in fanouts.items():
                if fanout > self.output_policy.fanout_limit:
                    gate = self.gates[name]
                    if gate.typename not in {
                        "custom__input",
                        "custom__const0",
                        "custom__const1",
                        "sky130_fd_sc_hd__dfrtp",
                        "sky130_fd_sc_hd__dfstp",
                        "sky130_fd_sc_hd__dfxtp",
                        "custom__dfre",
                        "custom__dfse",
                        "custom__dfe",
                    }:
                        intermediates[name] = gate.output_netname

        # TODO: toposort intermediates? Or just do it by hand?

        f.write(f"class {self.name}(wiring.Component):\n")
        for gate in self.gates.values():
            if gate.typename == "custom__input":
                f.write(f"    {gate.output_netname}: In(1)\n")
        for pin in self.outputs:
            f.write(f"    {pin}: Out(1)\n")

        f.write("\n    def __init__(self):\n")
        for intermediate_net in intermediates.values():
            f.write(f"        self._{intermediate_net} = Signal(1)\n")
        for gate in self.gates.values():
            if gate.typename in {"sky130_fd_sc_hd__dfrtp", "custom__dfre"}:
                f.write(f"        self._{gate.output_netname} = Signal(1, init=0)\n")
            if gate.typename in {"sky130_fd_sc_hd__dfstp", "custom__dfse"}:
                f.write(f"        self._{gate.output_netname} = Signal(1, init=1)\n")
            if gate.typename in {"sky130_fd_sc_hd__dfxtp", "custom__dfe"}:
                f.write(
                    f"        self._{gate.output_netname} = Signal(1, reset_less=True)\n"
                )
        f.write("\n        super().__init__()\n\n")

        f.write("    def elaborate(self, platform):\n        m = Module()\n\n")
        if intermediates:
            f.write("        m.d.comb += [\n")
            for gate_name, intermediate_net in intermediates.items():
                f.write(
                    f"            self._{intermediate_net}.eq({self.pretty_print_combinatorial_expression(gate_name, intermediates, use_intermediates=False)}),\n"
                )
            f.write("        ]\n\n")

        f.write("        m.d.sync += [\n")
        for gate in self.gates.values():
            if gate.typename in {
                "sky130_fd_sc_hd__dfrtp",
                "sky130_fd_sc_hd__dfstp",
                "sky130_fd_sc_hd__dfxtp",
            }:
                f.write(
                    f"            self._{gate.output_netname}.eq({self.pretty_print_combinatorial_expression(gate.inputs['D'], intermediates)}),\n"
                )
        f.write("        ]\n\n")

        flops_with_enable = [
            gate
            for gate in self.gates.values()
            if gate.typename in {"custom__dfre", "custom__dfse", "custom__dfe"}
        ]
        flops_with_enable.sort(key=lambda gate: gate.inputs["EN"])
        for enable, group in groupby(
            flops_with_enable, key=lambda gate: gate.inputs["EN"]
        ):
            f.write(
                f"        with m.If({self.pretty_print_combinatorial_expression(enable, intermediates)}):\n"
            )
            f.write("            m.d.sync += [\n")
            for gate in group:
                f.write(
                    f"                self._{gate.output_netname}.eq({self.pretty_print_combinatorial_expression(gate.inputs['D'], intermediates)}),\n"
                )
            f.write("            ]\n\n")

        f.write("        m.d.comb += [\n")
        for pin, driver in self.outputs.items():
            f.write(
                f"            self.{pin}.eq({self.pretty_print_combinatorial_expression(driver, intermediates)}),\n"
            )
        f.write("        ]\n\n")

        f.write("        return m\n\n")

    @classmethod
    def load(cls, _in: Path) -> Self:
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

        assert not (set(netlist["internal_wires"]) - net_drivers.keys()), (
            "No undriven nets"
        )

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

        outputs = {
            pin: net_drivers[pin] for pin in netlist["pins"] if pin not in inputs
        }

        for gate in gates.values():
            gate.inputs = {pin: net_drivers[net] for pin, net in gate.inputs.items()}

        top = cls(netlist["name"], gates, outputs)

        print("Pruning unused low/hide sides of conb cells")
        top.prune()
        return top

    def sanitize_net_names(self):
        """Sanitize net names"""
        self.outputs = {
            sanitize_identifier(net): driver for net, driver in self.outputs.items()
        }
        for gate in self.gates.values():
            gate.output_netname = sanitize_identifier(gate.output_netname)

    def remove_clock_and_reset(self):
        """
        Remove clock buffers

        Specifically, asserting that we on the same clock and reset domain
        Footnote for Amaranth generation: Amaranth only supports synchronous
        reset, and these gates are asynchronous. The test vectors will be
        designed so that this doesn't matter.
        """
        for gate in self.gates.values():
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
                    clock_source_gate = self.gates[clock_source]
                    assert clock_source_gate.typename == "sky130_fd_sc_hd__clkbuf"
                    clock_source = clock_source_gate.inputs["A"]

                del gate.inputs["CLK"]

        print("Pruning clock and reset trees")
        self.prune()

    def create_clock_enables(self):
        for name, gate in self.gates.items():
            if gate.typename in {
                "sky130_fd_sc_hd__dfrtp",
                "sky130_fd_sc_hd__dfstp",
                "sky130_fd_sc_hd__dfxtp",
            }:
                input_gate = self.gates[gate.inputs["D"]]
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
        self.prune()

    def visualize_lumps(self, lumps: list[Lump] | None):
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        combinatorial_gates = [
            gate
            for gate in self.gates.values()
            if gate.typename
            not in {
                "custom__input",
                "sky130_fd_sc_hd__dfrtp",
                "sky130_fd_sc_hd__dfstp",
                "sky130_fd_sc_hd__dfxtp",
                "custom__dfre",
                "custom__dfse",
                "custom__dfe",
            }
        ]
        sequential_gates = [
            gate
            for gate in self.gates.values()
            if gate.typename
            in {
                "sky130_fd_sc_hd__dfrtp",
                "sky130_fd_sc_hd__dfstp",
                "sky130_fd_sc_hd__dfxtp",
                "custom__dfre",
                "custom__dfse",
                "custom__dfe",
            }
        ]

        _fig, ax = plt.subplots()
        ax.set_title(f"{self.name} lumps")
        ax.plot(
            [gate.x for gate in combinatorial_gates],
            [gate.y for gate in combinatorial_gates],
            "r.",
            label="comb",
        )
        ax.plot(
            [gate.x for gate in sequential_gates],
            [gate.y for gate in sequential_gates],
            "b.",
            label="ff",
        )
        ax.xaxis.set_major_locator(MultipleLocator(20))
        ax.yaxis.set_major_locator(MultipleLocator(20))

        if lumps:
            for lump in lumps:
                ax.add_patch(
                    Rectangle(
                        (lump.x0, lump.y0),
                        lump.x1 - lump.x0,
                        lump.y1 - lump.y0,
                        edgecolor="black",
                        fill=False,
                    ),
                )
                ax.text(
                    (lump.x0 + lump.x1) / 2,
                    (lump.y0 + lump.y1) / 2,
                    lump.name,
                    ha="center",
                )

        ax.legend()

        plt.show()

    def separate_lumps(self, lumps_definitions: list[Lump]) -> list[Self]:
        lumps = {
            lump.name: self.__class__(
                name=lump.name,
                gates={},
                outputs={},
                output_policy=lump.output_policy or self.output_policy,
            )
            for lump in lumps_definitions
        }
        gate_to_lump = {}
        for name, gate in self.gates.items():
            if gate.typename == "custom__input":
                continue
            for lump in LUMPS[self.name]:
                if lump.x0 <= gate.x < lump.x1 and lump.y0 <= gate.y < lump.y1:
                    lumps[lump.name].gates[name] = gate
                    gate_to_lump[name] = lump.name
                    break
            else:
                raise RuntimeError(f"Gate {name} falls outside all defined lumps")

        for lump in lumps.values():
            added_inputs = {}
            inputs = {}
            for gate in lump.gates.values():
                for pin, source in gate.inputs.items():
                    if source in added_inputs:
                        gate.inputs[pin] = added_inputs[source]
                    elif source not in lump.gates:
                        net = self.gates[source].output_netname

                        inputs[net] = Gate(
                            typename="custom__input",
                            x=0.0,
                            y=0.0,
                            inputs={},
                            output_netname=net,
                        )

                        if source in gate_to_lump:
                            lumps[gate_to_lump[source]].outputs[net] = source

                        gate.inputs[pin] = net
                        added_inputs[source] = net

            lump.gates.update(inputs)

        for net, driver in self.outputs.items():
            source_lump = lumps[gate_to_lump[driver]]
            source_lump.outputs[net] = driver

        return list(lumps.values())


def generate_amaranth(in_: Path, out: Path, enable_lumping=True):
    top = Module.load(in_)
    top.sanitize_net_names()
    top.remove_clock_and_reset()
    top.create_clock_enables()

    if enable_lumping:
        if top.name not in LUMPS:
            raise NotImplementedError(f"No lumps defined for design {top.name}")
        lumps = top.separate_lumps(LUMPS[top.name])
    else:
        lumps = None

    # Write Amaranth to file

    with out.open("wt") as f:
        f.write(
            "from sys import argv\n"
            "\n"
            "from amaranth import *\n"
            "from amaranth.lib import wiring\n"
            "from amaranth.lib.wiring import In, Out\n"
            "\n"
        )

        f.write("\ndef Buf(expr):\n    return expr\n\n")

        if lumps:
            for module in lumps:
                module.write_amaranth_module(f)

            net_to_lump = dict(
                chain.from_iterable(
                    ((net, lump.name) for net in lump.outputs) for lump in lumps
                )
            )

            f.write(f"class {top.name}(wiring.Component):\n")
            for gate in top.gates.values():
                if gate.typename == "custom__input":
                    f.write(f"    {gate.output_netname}: In(1)\n")
            for pin in top.outputs:
                f.write(f"    {pin}: Out(1)\n")

            f.write("\n    # Testing outputs\n")
            for net in net_to_lump:
                if net not in top.outputs:
                    f.write(f"    {net}: Out(1)\n")

            f.write("\n    def elaborate(self, platform):\n        m = Module()\n\n")
            for lump in lumps:
                f.write(f"        m.submodules.{lump.name.lower()} = {lump.name}()\n")

            f.write("\n        m.d.comb += [\n")
            for lump in lumps:
                for gate in lump.gates.values():
                    if gate.typename == "custom__input":
                        net = gate.output_netname
                        if net in net_to_lump:
                            source = net_to_lump[net]
                            f.write(
                                f"            m.submodules.{lump.name.lower()}.{net}.eq(m.submodules.{source.lower()}.{net}),\n"
                            )
                        else:
                            f.write(
                                f"            m.submodules.{lump.name.lower()}.{net}.eq(self.{net}),\n"
                            )
            f.write("        ]\n\n")

            f.write("        m.d.comb += [\n")
            for pin in top.outputs:
                source = net_to_lump[pin]
                f.write(
                    f"            self.{pin}.eq(m.submodules.{source.lower()}.{pin}),\n"
                )
            f.write("        ]\n\n")

            f.write("        # Testing outputs\n")
            f.write("        m.d.comb += [\n")
            for net, source in net_to_lump.items():
                if net not in top.outputs:
                    f.write(
                        f"            self.{net}.eq(m.submodules.{source.lower()}.{net}),\n"
                    )
            f.write("        ]\n\n")
            f.write("        return m\n\n")
        else:
            top.write_amaranth_module(f)

        ports = [
            gate.output_netname
            for gate in top.gates.values()
            if gate.typename == "custom__input"
        ] + list(net_to_lump.keys())

        f.write(
            'if __name__ == "__main__":\n'
            "    from amaranth.back import verilog\n"
            f"    top = {top.name}()\n"
            '    with open(argv[1], "wt") as f:\n'
            f'        f.write(verilog.convert(top, name="{top.name}_amaranth", ports=[\n'
        )
        for port in ports:
            f.write(f"            top.{port},\n")
        f.write("        ]))\n")


def debug_lumps(in_: Path):
    top = Module.load(in_)
    top.sanitize_net_names()
    top.remove_clock_and_reset()
    top.create_clock_enables()
    top.visualize_lumps(LUMPS.get(top.name))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("netlist", type=Path)
    subparsers = parser.add_subparsers(required=True)

    generate_amaranth_subparser = subparsers.add_parser("generate_amaranth")
    generate_amaranth_subparser.set_defaults(action="generate_amaranth")
    generate_amaranth_subparser.add_argument("amaranth", type=Path)
    generate_amaranth_subparser.add_argument(
        "--lumping", action=BooleanOptionalAction, default=True
    )

    visualize_lumps_subparser = subparsers.add_parser("visualize_lumps")
    visualize_lumps_subparser.set_defaults(action="visualize_lumps")

    args = parser.parse_args()

    if args.action == "generate_amaranth":
        generate_amaranth(args.netlist, args.amaranth, enable_lumping=args.lumping)
    elif args.action == "visualize_lumps":
        debug_lumps(args.netlist)
