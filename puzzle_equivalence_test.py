import cocotb.types
from random import Random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge


async def check_equivalence(dut):
    inter_module_nets = [
        "net_1927",
        "net_3613",
        "net_323",
        "net_857",
        "net_203",
        "net_719",
        "net_2480",
        "net_736",
        "net_349",
        "net_2313",
        "net_3136",
        "net_3617",
        "net_1928",
        "net_204",
        "net_2461",
        "net_3830",
        "net_1363",
        "net_405",
        "net_2471",
        "net_2393",
        "net_1034",
        "net_1905",
        "net_2117",
        "net_1516",
        "net_2298",
        "net_1420",
        "net_3771",
        "net_1693",
        "net_791",
        "net_3435",
        "net_1816",
        "net_1815",
        "net_1472",
        "net_2120",
        "net_2460",
        "net_1559",
        "net_1628",
        "net_343",
        "net_934",
        "net_399",
        "net_545",
        "net_1694",
        "net_985",
        "net_378",
        "net_2479",
        "net_1738",
        "net_2088",
        "net_2475",
        "net_3552",
        "net_3420",
        "net_2315",
        "net_2505",
        "net_1351",
        "net_3920",
        "net_2004",
        "net_2416",
        "net_3283",
        "net_20",
        "net_1084",
        "net_1505",
        "net_1977",
        "net_3518",
        "net_377",
        "net_3384",
        "net_1719",
        "net_3419",
        "net_3818",
        "net_1822",
        "net_2006",
        "net_1936",
        "net_1723",
        "net_380",
        "net_1425",
        "net_3516",
        "net_294",
        "net_2259",
        "net_1365",
        "net_1907",
        "net_3543",
        "net_3037",
        "net_319",
        "net_401",
        "net_2189",
        "net_435",
        "net_1508",
        "net_2232",
        "net_1185",
        "net_1557",
        "net_2154",
        "net_1629",
        "net_341",
        "net_2240",
        "net_2386",
        "net_2459",
        "net_1526",
        "net_226",
        "net_832",
        "net_2474",
        "net_2463",
    ]

    while True:
        await FallingEdge(dut.clk)
        # At the beginning of a reset, there is a mismatch because of the
        # sync/async reset issue, so ignore differences while held in reset
        if dut.rst_n.value:
            assert dut.success_recovered_verilog.value == dut.success_amaranth.value
            assert dut.success_recovered_verilog.value == dut.success_solution.value
            assert dut.O_recovered_verilog.value == dut.O_amaranth.value
            assert dut.O_recovered_verilog.value == dut.O_solution.value
            for net in inter_module_nets:
                reference_val: cocotb.types.Logic = getattr(
                    dut.recovered_verilog, net
                ).value
                # In Amaranth, registers always start initialized - forgive this
                if reference_val == 0 or reference_val == 1:
                    assert reference_val == getattr(dut.amaranth, net).value
                    assert reference_val == getattr(dut.solution, net).value


@cocotb.test()
async def random_inputs(dut):
    c = Clock(dut.clk, 10, "ns")
    c.start()

    dut.rst_n.value = 0
    dut.enable.value = 0
    dut.I.value = 0

    cocotb.start_soon(check_equivalence(dut))

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


async def test_with_data(dut, data: list[list[int]]):
    c = Clock(dut.clk, 10, "ns")
    c.start()

    dut.rst_n.value = 0
    dut.enable.value = 0
    dut.I.value = 0

    cocotb.start_soon(check_equivalence(dut))

    dut.rst_n.value = 0
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1

    await FallingEdge(dut.clk)
    dut.enable.value = 1
    assert len(data) == 11
    for line in data:
        assert len(line) == 11
        for bit in line:
            dut.I.value = bit
            await FallingEdge(dut.clk)
    dut.enable.value = 0
    dut.I.value = 0

    for _ in range(16):
        await FallingEdge(dut.clk)


@cocotb.test()
async def eterna_pass(dut):
    await test_with_data(
        dut,
        [
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    )


@cocotb.test()
async def eterna_too_many(dut):
    await test_with_data(
        dut,
        [
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],  # too many
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    )


@cocotb.test()
async def eterna_too_few(dut):
    await test_with_data(
        dut,
        [
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # too few
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    )
