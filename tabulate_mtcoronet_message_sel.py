#!/usr/bin/env python3


from itertools import permutations
from amaranth.sim import Simulator
import matplotlib.pyplot as plt
import numpy as np
from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out


class Output_MtCoronet(wiring.Component):
    done_delayed: In(1)
    egg_almost_success: In(1)
    egg_full: In(1)
    egg_empty: In(1)
    success: In(1)
    I: In(8)
    output_enable: Out(1)
    message_select_1: Out(1)
    message_select_2: Out(1)
    message_select_3: Out(1)
    char_index: Out(4)
    O: Out(8)

    def __init__(self):
        self._char_index = Signal(4, reset_less=True)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.done_delayed):
            with m.If(self._char_index != 15):
                m.d.sync += self._char_index.eq(self._char_index + 1)
        with m.Else():
            m.d.sync += self._char_index.eq(0)

        m.d.comb += [
            self.char_index.eq(self._char_index),
            self.output_enable.eq((self.done_delayed) & (self._char_index != 15)),
            self.message_select_1.eq(
                ~(
                    (self.egg_empty)
                    | (((self.success) | (self.egg_almost_success)) & ~(self.egg_full))
                )
            ),
            self.message_select_2.eq(
                ~(
                    (self.egg_empty)
                    | (self.success)
                    | (self.egg_full)
                    | ~(self.egg_almost_success)
                )
            ),
            self.message_select_3.eq(
                ~(
                    ((~(self.success)) & (self.egg_almost_success))
                    | (self.egg_full)
                    | (self.egg_empty)
                )
            ),
        ]

        with m.If(self.output_enable):
            m.d.comb += self.O.eq(self.I)
        with m.Else():
            m.d.comb += self.O.eq(0)

        return m

dut = Output_MtCoronet()

inputs = [
    "success",
    "egg_almost_success",
    "egg_full",
    "egg_empty",
]

async def testbench(ctx):
    for i in range(16):
        input_values = {name: (i >> bit) & 1 for bit, name in enumerate(inputs)}
        for name, value in input_values.items():
            ctx.set(getattr(dut, name), value)

        reuslt = [ctx.get(getattr(dut, f"message_select_{bit}")) for bit in range(1, 4)]

        print(f"{input_values=} {reuslt=}")


sim = Simulator(dut)
sim.add_testbench(testbench)
sim.run()
