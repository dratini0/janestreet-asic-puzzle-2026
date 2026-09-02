#!/usr/bin/env python3


from itertools import permutations
from amaranth.sim import Simulator
import matplotlib.pyplot as plt
import numpy as np
from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out


# fmt: off
class Sunyshore(wiring.Component):
    minor_count: In(4)
    major_count: In(4)
    net_736: Out(1)
    net_1034: Out(1)
    net_857: Out(1)
    net_985: Out(1)

    def __init__(self):
        self._net_23 = Signal(1)
        self._net_103 = Signal(1)
        self._net_179 = Signal(1)
        self._net_43 = Signal(1)
        self._net_109 = Signal(1)
        self._net_25 = Signal(1)
        self._net_561 = Signal(1)
        self._net_40 = Signal(1)
        self._net_102 = Signal(1)
        self._net_39 = Signal(1)
        self._net_494 = Signal(1)
        self._net_270 = Signal(1)
        self._net_510 = Signal(1)
        self._net_574 = Signal(1)
        self._net_523 = Signal(1)
        self._net_56 = Signal(1)
        self._net_536 = Signal(1)
        self._net_15 = Signal(1)
        self._net_704 = Signal(1)
        self._net_775 = Signal(1)
        self._net_823 = Signal(1)
        self._net_565 = Signal(1)
        self._net_659 = Signal(1)
        self._net_773 = Signal(1)
        self._net_772 = Signal(1)
        self._net_45 = Signal(1)
        self._net_606 = Signal(1)
        self._net_21 = Signal(1)
        self._net_151 = Signal(1)
        self._net_58 = Signal(1)
        self._net_17 = Signal(1)
        self._net_99 = Signal(1)
        self._net_42 = Signal(1)
        self._net_16 = Signal(1)
        self._net_61 = Signal(1)
        self._net_14 = Signal(1)
        self._net_137 = Signal(1)
        self._net_53 = Signal(1)
        self._net_59 = Signal(1)
        self._net_51 = Signal(1)
        self._net_38 = Signal(1)
        self._net_240 = Signal(1)
        self._net_145 = Signal(1)
        self._net_122 = Signal(1)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._net_23.eq((self._net_270) ^ (~((self._net_659) ^ (self._net_565)))),
            self._net_103.eq(~((self._net_58) & (self._net_38))),
            self._net_179.eq(~((self._net_53) | (self._net_14))),
            self._net_43.eq(~((self._net_25) & (self._net_15))),
            self._net_109.eq(~((self._net_58) & (self._net_42))),
            self._net_25.eq(~((self._net_270) ^ (~((self._net_659) ^ (self._net_565))))),
            self._net_561.eq(((((((self._net_270) & (~((self._net_659) & (self._net_565)))) | (~((self._net_659) | (self._net_565))))) & (~((~(((~(~(self._net_606) & ((self.major_count[3]) ^ (self._net_510)))) & (~((self.minor_count[3]) & (~((self._net_606) ^ ((self.major_count[3]) ^ (self._net_510))))))) | ((~((self.major_count[1]) | (self._net_523))) | (self._net_574) | ((~((self.major_count[0]) & (self.major_count[2]))) & (self._net_523) & (~((self.major_count[1]) ^ (self.major_count[3]))))))) | ((~(~(self._net_606) & ((self.major_count[3]) ^ (self._net_510)))) & (~((self.minor_count[3]) & (~((self._net_606) ^ ((self.major_count[3]) ^ (self._net_510)))))) & ((~((self.major_count[1]) | (self._net_523))) | (self._net_574) | ((~((self.major_count[0]) & (self.major_count[2]))) & (self._net_523) & (~((self.major_count[1]) ^ (self.major_count[3]))))))))) | (~(((~(~(self._net_606) & ((self.major_count[3]) ^ (self._net_510)))) & (~((self.minor_count[3]) & (~((self._net_606) ^ ((self.major_count[3]) ^ (self._net_510))))))) | ((~((self.major_count[1]) | (self._net_523))) | (self._net_574) | ((~((self.major_count[0]) & (self.major_count[2]))) & (self._net_523) & (~((self.major_count[1]) ^ (self.major_count[3]))))))))),
            self._net_40.eq(~((self._net_25) | (self._net_179))),
            self._net_102.eq(~((self._net_561) ^ (~(~(self.major_count[0]) & ~(self.major_count[1]) & (self.major_count[2]) & (self.major_count[3])) & (~(((self.major_count[1]) | (self._net_523)) & ((~(((self.major_count[1]) & (self.major_count[3])) | (self.major_count[2]))) | ((((self.major_count[1]) & (self.major_count[2]) & (self.major_count[3])) | (self._net_574))))))))),
            self._net_39.eq(((((self._net_270) & (~((self._net_659) & (self._net_565)))) | (~((self._net_659) | (self._net_565))))) ^ (~((~(((~(~(self._net_606) & ((self.major_count[3]) ^ (self._net_510)))) & (~((self.minor_count[3]) & (~((self._net_606) ^ ((self.major_count[3]) ^ (self._net_510))))))) | ((~((self.major_count[1]) | (self._net_523))) | (self._net_574) | ((~((self.major_count[0]) & (self.major_count[2]))) & (self._net_523) & (~((self.major_count[1]) ^ (self.major_count[3]))))))) | ((~(~(self._net_606) & ((self.major_count[3]) ^ (self._net_510)))) & (~((self.minor_count[3]) & (~((self._net_606) ^ ((self.major_count[3]) ^ (self._net_510)))))) & ((~((self.major_count[1]) | (self._net_523))) | (self._net_574) | ((~((self.major_count[0]) & (self.major_count[2]))) & (self._net_523) & (~((self.major_count[1]) ^ (self.major_count[3]))))))))),
            self._net_494.eq((self._net_25) & (self._net_53) & (self._net_59)),
            self._net_270.eq((((self.minor_count[1]) & (self._net_51) & ((self.minor_count[2]) ^ (~(((self.major_count[1]) & (self._net_510)) | (~((self.major_count[1]) | (self.major_count[2]))))))) | ((self._net_58) & (self._net_151)))),
            self._net_510.eq((self.major_count[0]) ^ (self.major_count[2])),
            self._net_574.eq(~((~((self.major_count[0]) & (self.major_count[2]))) | (~((self.major_count[1]) ^ (self.major_count[3]))))),
            self._net_523.eq(~((self.major_count[3]) & (self._net_510))),
            self._net_56.eq(~((self._net_240) | (~((self._net_145) & (~((self.minor_count[0]) & (self.major_count[0]))))))),
            self._net_536.eq((self._net_561) ^ (~(~(self.major_count[0]) & ~(self.major_count[1]) & (self.major_count[2]) & (self.major_count[3])) & (~(((self.major_count[1]) | (self._net_523)) & ((~(((self.major_count[1]) & (self.major_count[3])) | (self.major_count[2]))) | ((((self.major_count[1]) & (self.major_count[2]) & (self.major_count[3])) | (self._net_574)))))))),
            self._net_15.eq(~((self._net_53) & (self._net_14))),
            self._net_704.eq((self._net_772) ^ (self._net_773)),
            self._net_775.eq(~((~((self._net_772) | (self._net_773))) | ((((self.major_count[0]) | (self.major_count[1])) & (self.major_count[2]) & (self.major_count[3]))))),
            self._net_823.eq(~((self._net_772) ^ (self._net_773))),
            self._net_565.eq((~((self.minor_count[2]) & (~(((self.major_count[1]) & (self._net_510)) | (~((self.major_count[1]) | (self.major_count[2])))))) & ((~((self.major_count[0]) & (self.major_count[1]))) | (self.major_count[2])))),
            self._net_659.eq(~((self.minor_count[3]) ^ (~((self._net_606) ^ ((self.major_count[3]) ^ (self._net_510)))))),
            self._net_773.eq((((self._net_606) & (self._net_574)) | (~(((self.major_count[3]) & (self._net_606)) | (self._net_574))))),
            self._net_772.eq(~(((self._net_561) & (~(((self.major_count[1]) | (self._net_523)) & ((~(((self.major_count[1]) & (self.major_count[3])) | (self.major_count[2]))) | ((((self.major_count[1]) & (self.major_count[2]) & (self.major_count[3])) | (self._net_574))))))) | (~(self.major_count[0]) & ~(self.major_count[1]) & (self.major_count[2]) & (self.major_count[3])))),
            self._net_45.eq((self._net_99) | (self._net_38)),
            self._net_606.eq(~((self.major_count[1]) & (self.major_count[2]))),
            self._net_21.eq(~((self._net_122) & (self._net_53))),
            self._net_151.eq(~((self._net_145) | (~((self.minor_count[0]) & (self.major_count[0]))))),
            self._net_58.eq(~((~((self.minor_count[1]) & (self._net_51))) ^ ((self.minor_count[2]) ^ (~(((self.major_count[1]) & (self._net_510)) | (~((self.major_count[1]) | (self.major_count[2])))))))),
            self._net_17.eq((self._net_25) | (self._net_45)),
            self._net_99.eq((self._net_58) ^ (self._net_151)),
            self._net_42.eq(~((self._net_145) | (self._net_122))),
            self._net_16.eq((self._net_99) | (self._net_14)),
            self._net_61.eq((self._net_42) | (self._net_53) | (self._net_14)),
            self._net_14.eq(~((~(((self.minor_count[0]) & (self.major_count[0])) | (self._net_240))) | (self._net_38))),
            self._net_137.eq(~((self._net_53) | (self._net_56))),
            self._net_53.eq(~((self._net_58) ^ (self._net_151))),
            self._net_59.eq((self._net_122) & (self._net_38)),
            self._net_51.eq((self.major_count[0]) ^ (self.major_count[1])),
            self._net_38.eq(~(self._net_151) & (~((self._net_145) & (~((self.minor_count[0]) & (self.major_count[0])))))),
            self._net_240.eq(~((self.minor_count[0]) | (self.major_count[0]))),
            self._net_145.eq(~((self.minor_count[1]) ^ (self._net_51))),
            self._net_122.eq(((self.minor_count[0]) & (self.major_count[0])) | (self._net_240)),
        ]

        m.d.sync += [
        ]

        m.d.comb += [
            self.net_736.eq(((((((~((self._net_109) | (self._net_25))) | (self._net_39) | (self._net_494)) & (self._net_102) & (~((self._net_39) & (Mux((self._net_23), ((self._net_42) | (self._net_14) | (self._net_137)), (self._net_61))))))) | ((((self._net_536) & ((((self._net_53) & ((self._net_25) | (self._net_14))) | (~(~(((self._net_23) & (self._net_179)) | (self._net_39)))))) & (~((self._net_39) & (~(((self._net_42) | (self._net_23) | (self._net_99)) & (self._net_109)))))) | (self._net_704)))) & (self._net_775) & ((self._net_823) | ((((~((self._net_39) & (self._net_43))) | (self._net_40)) & (self._net_102) & ((self._net_39) | (~((self._net_23) | (self._net_103))) | (~((self._net_23) | (self._net_45)))))) | (~(((~((self._net_39) & (self._net_43))) & ((self._net_39) | (self._net_40) | ((((self._net_42) | (self._net_99)) & (self._net_25) & (self._net_109))))) | (self._net_102)))))),
            self.net_1034.eq((((self._net_704) | (Mux((self._net_536), (Mux((self._net_39), ((((self._net_23) & (self._net_103) & (self._net_21)) | (self._net_59))), ((((self._net_42) | (self._net_43)) & ((self._net_25) | (self._net_14)))))), ((((self._net_39) | (self._net_494) | (~((self._net_25) | (self._net_61)))) & ((~((self._net_179) | (self._net_43))) | (~(((self._net_25) | (self._net_137) | (~(self._net_16))) & (self._net_39))))))))) & ((((self._net_536) & ((((self._net_39) & (self._net_43) & (self._net_17)) | (((((self._net_23) | (~(~(self._net_59) & (self._net_45)))) & ((self._net_17) | (~(((self.minor_count[0]) & (self.major_count[0])) | (self._net_240)))))) & (~(((self._net_23) & (self._net_179)) | (self._net_39))))))) | ((((self._net_137) | (~(((self._net_23) | (~(self._net_16))) & (self._net_39)))) & (((((self._net_23) | ((self._net_103) & (self._net_21))) & (self._net_17))) | (self._net_39)) & (self._net_102))) | (self._net_823))) & (self._net_775))),
            self.net_857.eq((((self._net_704) | ((((self._net_536) & ((((self._net_39) & (~((self._net_109) | (self._net_23)))) | (~((((self._net_25) & (~((self._net_58) & (self._net_56)))) | ((((self._net_42) | (self._net_16)) & (self._net_23))) | (self._net_39))))))) | ((self._net_102) & ((((self._net_58) & (self._net_39) & (self._net_38)) | (self._net_40) | ((self._net_25) & (~(self._net_56)) & (self._net_21)))) & (~(((self._net_40) | ((self._net_25) & (~(self._net_56)) & (self._net_21))) & (self._net_39))))))) & (~(((self._net_536) | (Mux((self._net_39), ((((self._net_15) & (self._net_40)) | ((self._net_16) & (self._net_25)))), ((~((self._net_23) | (self._net_45))) | ((((self._net_23) | (self._net_56)) & (self._net_45))))))) & ((((self._net_39) & (self._net_45)) | (Mux((~(~(self._net_59) & (self._net_45))), (self._net_25), (self._net_40))) | (self._net_102))) & (self._net_704))) & (self._net_775))),
            self.net_985.eq((((self._net_704) | (~(((self._net_536) | ((((self._net_39) | (self._net_494) | (~(((self._net_25) & (self._net_59)) | (self._net_61)))) & ((~(((self._net_25) | (self._net_137) | (~(self._net_16))) & (self._net_39))) | (~((self._net_23) | (self._net_179))))))) & ((self._net_39) | (self._net_102) | ((self._net_42) | (self._net_14) | (self._net_137)) | ((((self._net_42) | (self._net_16)) & (self._net_23))))))) & ((((self._net_39) & (~(((self._net_25) | (self._net_15)) & (((self._net_42) | (self._net_23) | (self._net_16)) | (self._net_536))))) | (((self._net_536) | (~((self._net_23) | (self._net_103)))) & (~(((self._net_536) & ((((self._net_25) | (~((self._net_58) & (self._net_56)))) & ~(~((self._net_109) | (self._net_23)))))) | (self._net_39)))) | (self._net_823))) & (self._net_775))),
        ]

        return m
# fmt: on

data = np.zeros((4, 16, 16), dtype=np.uint8)

dut = Sunyshore()


async def testbench(ctx):
    for major in range(16):
        ctx.set(dut.major_count, major)
        for minor in range(16):
            ctx.set(dut.minor_count, minor)
            data[0, major, minor] = ctx.get(dut.net_736)
            data[1, major, minor] = ctx.get(dut.net_857)
            data[2, major, minor] = ctx.get(dut.net_985)
            data[3, major, minor] = ctx.get(dut.net_1034)


sim = Simulator(dut)
sim.add_testbench(testbench)
sim.run()
data = data[:, :11, :11]

fig, axs = plt.subplots(1, 4, sharex="all", sharey="all")

for i in range(4):
    axs[i].imshow(data[i])

plt.show()

fig, axs = plt.subplots(4, 6, sharex="all", sharey="all", squeeze=False)

for permutation, ax in zip(permutations(range(4)), axs.flat, strict=True):
    new_data = sum(pane << shift for pane, shift in zip(data, permutation))
    print(permutation, np.max(new_data))

    ax.set_title(str(permutation))
    ax.imshow(new_data)

plt.show()

print(repr(sum(plane << shift for shift, plane in enumerate(data))))
