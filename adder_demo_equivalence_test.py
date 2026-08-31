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
    dut.en.value = 0
    dut.A.value = 0
    dut.B.value = 0

    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1

    r = Random(bytes.fromhex("df50d2b6c44e5120"))

    for _ in range(10_000):
        await FallingEdge(dut.clk)
        assert dut.S_original.value == dut.S_recovered_verilog.value
        assert dut.S_original.value == dut.S_amaranth.value
        dut.en.value = r.random() < 2/3
        dut.A.value = r.random() < 2/3
        dut.B.value = r.random() < 2/3
