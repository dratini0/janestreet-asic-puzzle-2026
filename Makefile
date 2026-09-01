SIM ?= icarus
TOPLEVEL_LANG ?= verilog


build/%_nets.v: %_nets.json netlist_to_verilog.py
	./netlist_to_verilog.py $< $@

build/%_amaranth.py: %_nets.json netlist_to_amaranth.py
	./netlist_to_amaranth.py $< $@

build/%_amaranth.v: build/%_amaranth.py
	python $< $@

adder_demo_equivalence_test: build/adder_demo_nets.v build/adder_demo_amaranth.v
	make -f adder_demo_equivalence_test.mk clean sim

puzzle_equivalence_test: build/puzzle_nets.v build/puzzle_amaranth.v
	make -f puzzle_equivalence_test.mk clean sim

.PHONY: adder_demo_equivalence_test puzzle_equivalence_test