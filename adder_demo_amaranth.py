from sys import argv

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out


def Buf(expr):
    return expr

class ShiftRegisterA(wiring.Component):
    en: In(1)
    A: In(1)
    net_91: Out(1)
    net_22: Out(1)
    net_34: Out(1)
    net_37: Out(1)
    net_122: Out(1)
    net_233: Out(1)
    net_15: Out(1)
    net_11: Out(1)

    def __init__(self):
        self._net_37 = Signal(1, init=0)
        self._net_15 = Signal(1, init=0)
        self._net_34 = Signal(1, init=0)
        self._net_91 = Signal(1, init=0)
        self._net_11 = Signal(1, init=0)
        self._net_233 = Signal(1, init=0)
        self._net_22 = Signal(1, init=0)
        self._net_122 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
        ]

        with m.If(self.en):
            m.d.sync += [
                self._net_37.eq(self._net_15),
                self._net_15.eq(self._net_34),
                self._net_34.eq(self._net_91),
                self._net_91.eq(self._net_122),
                self._net_11.eq(self.A),
                self._net_233.eq(self._net_37),
                self._net_22.eq(self._net_233),
                self._net_122.eq(self._net_11),
            ]

        m.d.comb += [
            self.net_91.eq(self._net_91),
            self.net_22.eq(self._net_22),
            self.net_34.eq(self._net_34),
            self.net_37.eq(self._net_37),
            self.net_122.eq(self._net_122),
            self.net_233.eq(self._net_233),
            self.net_15.eq(self._net_15),
            self.net_11.eq(self._net_11),
        ]

        return m

class ShiftRegisterB(wiring.Component):
    en: In(1)
    B: In(1)
    net_46: Out(1)
    net_113: Out(1)
    net_35: Out(1)
    net_33: Out(1)
    net_123: Out(1)
    net_65: Out(1)
    net_14: Out(1)
    net_18: Out(1)

    def __init__(self):
        self._net_65 = Signal(1, init=0)
        self._net_35 = Signal(1, init=0)
        self._net_113 = Signal(1, init=0)
        self._net_46 = Signal(1, init=0)
        self._net_123 = Signal(1, init=0)
        self._net_33 = Signal(1, init=0)
        self._net_18 = Signal(1, init=0)
        self._net_14 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
        ]

        with m.If(self.en):
            m.d.sync += [
                self._net_65.eq(self._net_33),
                self._net_35.eq(self._net_46),
                self._net_113.eq(self._net_65),
                self._net_46.eq(self._net_123),
                self._net_123.eq(self._net_18),
                self._net_33.eq(self._net_14),
                self._net_18.eq(self.B),
                self._net_14.eq(self._net_35),
            ]

        m.d.comb += [
            self.net_46.eq(self._net_46),
            self.net_113.eq(self._net_113),
            self.net_35.eq(self._net_35),
            self.net_33.eq(self._net_33),
            self.net_123.eq(self._net_123),
            self.net_65.eq(self._net_65),
            self.net_14.eq(self._net_14),
            self.net_18.eq(self._net_18),
        ]

        return m

class Compare496(wiring.Component):
    net_335: In(1)
    net_62: In(1)
    net_281: In(1)
    net_177: In(1)
    net_173: In(1)
    net_351: In(1)
    net_333: In(1)
    net_153: In(1)
    net_306: In(1)
    S: Out(1)

    def __init__(self):

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
        ]

        m.d.comb += [
            self.S.eq(~(self.net_153) & ~(self.net_306) & ((self.net_351) & (self.net_333) & (self.net_173)) & (~(self.net_335) & ~(self.net_177) & (self.net_62) & (self.net_281))),
        ]

        return m

class Add(wiring.Component):
    net_91: In(1)
    net_46: In(1)
    net_113: In(1)
    net_22: In(1)
    net_35: In(1)
    net_34: In(1)
    net_33: In(1)
    net_37: In(1)
    net_123: In(1)
    net_122: In(1)
    net_65: In(1)
    net_233: In(1)
    net_14: In(1)
    net_15: In(1)
    net_11: In(1)
    net_18: In(1)
    net_335: Out(1)
    net_62: Out(1)
    net_281: Out(1)
    net_177: Out(1)
    net_173: Out(1)
    net_351: Out(1)
    net_333: Out(1)
    net_153: Out(1)
    net_306: Out(1)

    def __init__(self):

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
        ]

        m.d.comb += [
            self.net_335.eq((~((~((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34)))) ^ (((((((self.net_18) & (self.net_11) & ((self.net_123) ^ (self.net_122))) | ((self.net_123) & (self.net_122)))) & (((self.net_46) | (self.net_91)) & (~((self.net_46) & (self.net_91))))) | (~(~((self.net_46) & (self.net_91))))))),
            self.net_62.eq((~(((self.net_14) & (self.net_15)) | (~((self.net_14) | (self.net_15))))) ^ (((((((self.net_18) & (self.net_11) & ((self.net_123) ^ (self.net_122))) | ((self.net_123) & (self.net_122)))) & (((self.net_46) | (self.net_91)) & (~((self.net_46) & (self.net_91)))) & (~((~((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34))))) | ((((self.net_46) & (self.net_91) & ((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34))))))),
            self.net_281.eq((~((~((self.net_33) | (self.net_37))) | ((self.net_33) & (self.net_37)))) ^ ((((~(((self.net_14) & (self.net_15)) | (~((self.net_14) | (self.net_15))))) & (((((((self.net_18) & (self.net_11) & ((self.net_123) ^ (self.net_122))) | ((self.net_123) & (self.net_122)))) & (((self.net_46) | (self.net_91)) & (~((self.net_46) & (self.net_91)))) & (~((~((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34))))) | ((((self.net_46) & (self.net_91) & ((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34))))))) | ((self.net_14) & (self.net_15))))),
            self.net_177.eq(((((self.net_18) & (self.net_11) & ((self.net_123) ^ (self.net_122))) | ((self.net_123) & (self.net_122)))) ^ (((self.net_46) | (self.net_91)) & (~((self.net_46) & (self.net_91))))),
            self.net_173.eq(~(((~((self.net_113) | (self.net_22))) | (~((((self.net_65) | (self.net_233)) & ((((~(((self.net_14) & (self.net_15)) | (~((self.net_14) | (self.net_15))))) & (((((((self.net_18) & (self.net_11) & ((self.net_123) ^ (self.net_122))) | ((self.net_123) & (self.net_122)))) & (((self.net_46) | (self.net_91)) & (~((self.net_46) & (self.net_91)))) & (~((~((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34))))) | ((((self.net_46) & (self.net_91) & ((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34)))))) & (~((~((self.net_33) | (self.net_37))) | ((self.net_33) & (self.net_37))))) | ((((self.net_14) & (self.net_15) & ((self.net_33) | (self.net_37))) | ((self.net_33) & (self.net_37))))))) | (~(~((self.net_65) & (self.net_233))))))) & ~((self.net_113) & (self.net_22)))),
            self.net_351.eq(~((~((~((self.net_65) & (self.net_233))) & ((self.net_65) | (self.net_233)))) ^ ((((~(((self.net_14) & (self.net_15)) | (~((self.net_14) | (self.net_15))))) & (((((((self.net_18) & (self.net_11) & ((self.net_123) ^ (self.net_122))) | ((self.net_123) & (self.net_122)))) & (((self.net_46) | (self.net_91)) & (~((self.net_46) & (self.net_91)))) & (~((~((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34))))) | ((((self.net_46) & (self.net_91) & ((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34)))))) & (~((~((self.net_33) | (self.net_37))) | ((self.net_33) & (self.net_37))))) | ((((self.net_14) & (self.net_15) & ((self.net_33) | (self.net_37))) | ((self.net_33) & (self.net_37)))))))),
            self.net_333.eq(~((~(((self.net_113) & (self.net_22)) | (~((self.net_113) | (self.net_22))))) ^ (~((((self.net_65) | (self.net_233)) & ((((~(((self.net_14) & (self.net_15)) | (~((self.net_14) | (self.net_15))))) & (((((((self.net_18) & (self.net_11) & ((self.net_123) ^ (self.net_122))) | ((self.net_123) & (self.net_122)))) & (((self.net_46) | (self.net_91)) & (~((self.net_46) & (self.net_91)))) & (~((~((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34))))) | ((((self.net_46) & (self.net_91) & ((self.net_35) | (self.net_34))) | ((self.net_35) & (self.net_34)))))) & (~((~((self.net_33) | (self.net_37))) | ((self.net_33) & (self.net_37))))) | ((((self.net_14) & (self.net_15) & ((self.net_33) | (self.net_37))) | ((self.net_33) & (self.net_37))))))) | (~(~((self.net_65) & (self.net_233)))))))),
            self.net_153.eq(~((~((self.net_18) & (self.net_11))) ^ ((self.net_123) ^ (self.net_122)))),
            self.net_306.eq((~((self.net_18) & (self.net_11))) & ((self.net_18) | (self.net_11))),
        ]

        return m

class adder_demo(wiring.Component):
    A: In(1)
    B: In(1)
    en: In(1)
    S: Out(1)

    def elaborate(self, platform):
        m = Module()

        m.submodules.shiftregistera = ShiftRegisterA()
        m.submodules.shiftregisterb = ShiftRegisterB()
        m.submodules.compare496 = Compare496()
        m.submodules.add = Add()

        m.d.comb += [
            m.submodules.shiftregistera.en.eq(self.en),
            m.submodules.shiftregistera.A.eq(self.A),
            m.submodules.shiftregisterb.en.eq(self.en),
            m.submodules.shiftregisterb.B.eq(self.B),
            m.submodules.compare496.net_335.eq(m.submodules.add.net_335),
            m.submodules.compare496.net_62.eq(m.submodules.add.net_62),
            m.submodules.compare496.net_281.eq(m.submodules.add.net_281),
            m.submodules.compare496.net_177.eq(m.submodules.add.net_177),
            m.submodules.compare496.net_173.eq(m.submodules.add.net_173),
            m.submodules.compare496.net_351.eq(m.submodules.add.net_351),
            m.submodules.compare496.net_333.eq(m.submodules.add.net_333),
            m.submodules.compare496.net_153.eq(m.submodules.add.net_153),
            m.submodules.compare496.net_306.eq(m.submodules.add.net_306),
            m.submodules.add.net_91.eq(m.submodules.shiftregistera.net_91),
            m.submodules.add.net_46.eq(m.submodules.shiftregisterb.net_46),
            m.submodules.add.net_113.eq(m.submodules.shiftregisterb.net_113),
            m.submodules.add.net_22.eq(m.submodules.shiftregistera.net_22),
            m.submodules.add.net_35.eq(m.submodules.shiftregisterb.net_35),
            m.submodules.add.net_34.eq(m.submodules.shiftregistera.net_34),
            m.submodules.add.net_33.eq(m.submodules.shiftregisterb.net_33),
            m.submodules.add.net_37.eq(m.submodules.shiftregistera.net_37),
            m.submodules.add.net_123.eq(m.submodules.shiftregisterb.net_123),
            m.submodules.add.net_122.eq(m.submodules.shiftregistera.net_122),
            m.submodules.add.net_65.eq(m.submodules.shiftregisterb.net_65),
            m.submodules.add.net_233.eq(m.submodules.shiftregistera.net_233),
            m.submodules.add.net_14.eq(m.submodules.shiftregisterb.net_14),
            m.submodules.add.net_15.eq(m.submodules.shiftregistera.net_15),
            m.submodules.add.net_11.eq(m.submodules.shiftregistera.net_11),
            m.submodules.add.net_18.eq(m.submodules.shiftregisterb.net_18),
        ]

        m.d.comb += [
            self.S.eq(m.submodules.compare496.net_18),
        ]

        return m

if __name__ == "__main__":
    from amaranth.back import verilog
    top = adder_demo()
    with open(argv[1], "wt") as f:
        f.write(verilog.convert(top, name="adder_demo_amaranth", ports=[top.A, top.B, top.en, top.S]))
