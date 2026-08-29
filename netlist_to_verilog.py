#!/usr/bin/env python3


import json
from argparse import ArgumentParser
from pathlib import Path


def main(_in: Path, out: Path):
    with _in.open("rt") as f:
        netlist = json.load(f)
    with out.open("wt") as f:
        f.write("`default_nettype none\n\n")
        f.write(f"module {netlist['name']}_recovered_verilog (\n")
        f.write(
            ",\n".join(
                (
                    f"  output \\{net} "
                    if net.startswith("O[")
                    else f"  output {net}"
                    if net in {"S", "success"}
                    else f"  input {net}"
                )
                for net in netlist["pins"]
            )
        )
        f.write("\n);\n")
        for net in netlist["internal_wires"]:
            f.write(f"  wire {net};\n")
        f.write("\n")

        for gate in netlist["gates"]:
            f.write(f"  {gate['typename']} gate_{gate['id']} (\n")
            f.write(
                ",\n".join(
                    (
                        f"    .{pin}(\\{net} )"
                        if net.startswith("O[")
                        else f"    .{pin}({net})"
                    )
                    for pin, net in gate["connections"].items()
                )
            )
            f.write("\n  );\n\n")

        f.write("endmodule\n")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("netlist", type=Path)
    parser.add_argument("verilog", type=Path)
    args = parser.parse_args()
    main(args.netlist, args.verilog)
