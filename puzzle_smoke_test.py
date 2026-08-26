from random import Random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge


@cocotb.test()
async def my_second_test(dut):
    """Try accessing the design."""

    c = Clock(dut.clk, 10, "ns")
    c.start()

    dut.rst_n.value = 0
    dut.enable.value = 0
    dut.I.value = 0

    r = Random(bytes.fromhex("77c614446ff43005"))

    for _ in range(10):
        dut.rst_n.value = 0
        await FallingEdge(dut.clk)
        await FallingEdge(dut.clk)
        await FallingEdge(dut.clk)

        dut.rst_n.value = 1

        await FallingEdge(dut.clk)
        dut.enable.value = 1
        for _ in range(121):
            dut.I.value = r.randrange(2)
            await FallingEdge(dut.clk)
        dut.enable.value = 0
        dut.I.value = 0

        for _ in range(16):
            await FallingEdge(dut.clk)

    # Validated by inspection
