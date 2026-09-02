# Makefile

# defaults
SIM ?= icarus
TOPLEVEL_LANG = verilog

VERILOG_SOURCES = sky130_sc_hd_verilog/primitives.v \
sky130_sc_hd_verilog/sky130_fd_sc_hd.v \
build/puzzle_nets.v \
build/puzzle_amaranth.v \
build/puzzle_solution.v \
puzzle_equivalence_test.v

# COCOTB_TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
COCOTB_TOPLEVEL = puzzle_equivalence_test

# COCOTB_TEST_MODULES is the basename of the Python test file(s)
COCOTB_TEST_MODULES = puzzle_equivalence_test

COMPILE_ARGS = -DFUNCTIONAL

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
