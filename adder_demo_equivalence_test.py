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

    for _ in range(100_000):
        await FallingEdge(dut.clk)
        assert dut.S_original.value == dut.S_recovered_verilog.value
        dut.en.value = r.randrange(2)
        dut.A.value = r.randrange(2)
        dut.B.value = r.randrange(2)
