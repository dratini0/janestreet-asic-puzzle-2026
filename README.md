# ASIC Reverse-Engineering Puzzle solution

This repo represents my solution to [Jane Street's ASIC reverse engineering puzzle](https://blog.janestreet.com/can-you-reverse-engineer-an-asic/).
It is a fork of the [original repository](https://github.com/janestreet/asic-puzzle-2026), I just had to remove its fork-ness to keep it private until the submission deadline.
This is a limitation of GitHub.

## Copyright
* Puzzle files (`warmup/*`, `puzzle.gds`, `example_inputs.vcd`, `layout.png`) are copyright Jane Street
* The files inside `sky130_sc_hd_verilog` are copyright The SkyWater PDK Authors, license include in the file (for every single standard cell, no less)
* `cells.json` is copyright Tiny Tapeout, [source](https://github.com/TinyTapeout/tt-support-tools/blob/main/tech/sky130A/cells.json) (be careful, it has bugs in the formulas!)
* All other files in this repository are my own work, Apache 2.0, I guess, if you want to use it for some reason?

## AI disclaimer

I have not used any AI tools to author this code, which I regret in retrospect.
The [fork of PyEDA](https://github.com/Speedata-io/pyeda) I have been using seems to be mostly maintained with Claude, however.
