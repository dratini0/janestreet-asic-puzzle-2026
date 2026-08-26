SIM ?= icarus
TOPLEVEL_LANG ?= verilog


build/%_nets.v: %_nets.json netlist_to_verilog.py
	./netlist_to_verilog.py $< $@

adder_demo_equivalence_test: build/adder_demo_nets.v
	make -f adder_demo_equivalence_test.mk clean sim

puzzle_smoke_test: build/puzzle_nets.v
	make -f puzzle_smoke_test.mk clean sim

.PHONY: adder_demo_equivalence_test puzzle_smoke_test