# Before day 1

* Staring at the layout in TT GDS viewer and KLayout
* Realizing a few basic facts
    * The GDS file contains the standard cell as a block -> no need to try to match them
    * The wiring and the standard cells seem to use differet layers
    * Actually, the inputs and outputs of the standard cells are labelled -> no need to try to label them myself!
* Formulate a basic plan
    1. Extract netlist
    2. Sanity-check netlist
    3. Convert netlist (warmup and puzzle) into verilog, and simulate puzzle against the test vector and the warmup against the verilog
    4. Segment netlist into modules based on the physical location, and write this into Amaranth.
    5. Simulate Amaranth against Verilog netlist
    6. Reverse-engineer each Amaranth module by hand, occasionally simulating against the Verilog netlist again
    7. If that fails, it seems like each module will be small enough to explore its state-space by computer. Will that help?
    8. When I get a solution, definitely simulate that against the Verilog netlist

# Day 1

1. Load everything into KLayout
    * Notice that KLayout has no layer names
2. Take the Tiny Tapeout GDS viewer's layer definitions and turn this into a KLayout 2.5D view script
    * Easy enough, but it didn't give me anything immediately useful
    * The layer names were only showing up in the 2.5D view
    * Didn't magically give me any connectivity information
    * But: it did mean that I had a source for layer names now, which is huge, and from the z-height, I could derive the connectivity too
3. Name the layers and create a layer properties file
    * I could now hide all the layers I wasn't interested in
    * (In actuality this happened in parellel with the connectivity work)
4. Figure out the "trace net" function in KLayout
    * You need to specify connectivity to make it work (edit layer stack)
    * First, I specified connections between the met1-met5 layers via the via layers
    * This resulted in the enable input going into a diode and nothing else
    * Turns out that line is connected via the diode's "li1" layer, so I added li1 as an additional layer, as well as its connection to met1 via mcon
        * I think the li1 is just a conductive layer inside the standard cells - at least, all of their connections seem to be on this layer.
        * The [pdk docs](https://skywater-pdk.readthedocs.io/en/main/rules/layers.html) say it's the local interconnect. I'm assuming it's essentially another metal layer, maybe it's a bit less conductive.
    * I could now trace single nets, neat
    * What does that tantalizing "trace all nets" button do?
    * Unsurprisingly, it traces all nets. In flat mode, this produces a mostly usable netlist, but it loses all the netlabels. I would have to relabel those nets.
    * Turns out, the netlabels live on the datatype 5 layers next to their corresponding metal layer. Let's add those into the connectivity
    * Now, the hierarchical version of "trace all nets" works better, including matching up the inputs and outputs of standard cells to specific nets. Jackpot.
    * I now have a netlist, I just need to export it in some format that's useful
5. I have exported the connectivity thing as a KLayout technology, and I tried to pair it up with the layer properties file too. I don't know how to package it up correctly, but that's our of scope for this puzzle.
6. Rough sanity check
    * There seems to be many hundreds of nets - that's about the expected number for the puzzle
    * Each net seems to have exactly one driver, and one or more load - that's good (there aren't any tri-state outputs on any of the used cells, thank you!)
    * There are 3 nets with 0 connections - it's the logo.
    * On the warmup's netlist, there are 81 unnamed nets, this corresponds to the 78 internal nets from 01_netlist.v plus the 3 from the logo. Looks good.
7. One last observation - the SKY130 PDK doesn't seem to include a D-FF with an enable pin (like it's common on FPGAs), so I think I will need to special case the combination of MUX + DFF

# Day 3

1. Some misc observations
    * The fanout on rst_n is way too high, I it goes to every resettable DFF
    * There is way fewer decoupling caps than on my Tiny Tapout 03 design, also, there is no fill
        * Definitely a different flow, maybe not even manufacturable? I can't actually tell.
    * The pinout and the warmup "puzzle" suggests lots of shift registers that are enabled by the en pin, but I don't think that's the case - not enough MUXes for that. There are probably some though. Brings into question the DFF + MUX = DFFE transformation though.
    * In the example waveform, it only outputs uppercase ASCII, but O[7] has a driver - presumably it outputs other stuff too? Are there Easter Eggs here?
2. Got netlist out of KLayout into custom format
    * Checked it in because I want the verilog to be reproducible and the extraction order and net IDs from KLayout might not be stable
3. Converted netlist to plain Verilog, and successfully simulated adder_demo against its source
    * Took the sky130 PDK sim files from my TT03 working tree
4. I have simulated the recovered puzzle netlist.
    * I couldn't be bothered to read the VCD, so I simulated some random bits
    * I thought it responds when enable falls, but it turns out it matters that it takes exactly 121 bits. That *must* be a clue. It must.

# Day 4

1. What is the deal with all the conb blocks whose lo outputs are going to a22o’s and similar?
    * That makes the other half of that and useless.
    * It also seems to go to and gates when it's the high output
    * Logic optimization will prune that, maybe? Or do I just change that to HI/LO and watch it do something even weirder? Let’s put a pin in that for now.
    * Or is this one of those things added so that we can do a simple metal layer change to fix something? Maybe to prevent a logic hazard?
2. Likewise, there is a buffer - why? I don't think I will optimize it out, I'm curious.
3. Ooops, I left the diodes in. Easy enough to fix.
4. There are 15 sky130_fd_sc_hd__clkbuf_4's in the design, with their outputs completely unconnected. I checked on the GDS. They are unused. Why? Is that just an obstacle for us? I'm not sure I believe that. Is it some odd analog semiconductor thing I don't understand? Or just some process artifact? Or is there something more profound to that?
    * Whatever, I'm pruning all of it, I just can't see any possibility of anything interesting being in there.
5. Net 1447 (in my notation) is completely undriven. And it seems to check out on the GDS too. Why??? There is no way it passed any DRC. It has to be an obstacle, at this point, but if so, why is it in the output generator?!
    * Notably, the simulation works fine with it being undriven? Or is that only because I haven't solved it?
    * This is crazy. And I'm not sure Amaranth can express 4-value Verilog nets...
    * Actually, it could also be a missing via to ... The output of one of the gates it's an input to? Probably not.
    * It does cause x-propagation, but: only when the output generator is outputting a space or a null. It never reaches the output. Hmm. I'm very worried about this.
    * I will just add a constant 0 to it, and hope for the best! That's so weird.
    * Actually, one better, I will turn it into an input. Nasty hack, but it works, because while Amaranth can't model z's, the verilog it generates will handle it just fine... I think.

# Register of Easter Eggs
* Jane Street logo on met2 (I suppose it's an easter egg, since it wasn't in the PNG, but not exactly a major achievement to find it)
