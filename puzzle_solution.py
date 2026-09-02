from sys import argv

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out


def Buf(expr):
    return expr

class Floaroma(wiring.Component):
    net_1508: In(1)
    net_1526: In(1)
    enable: In(1)
    net_934: Out(1)
    net_3136: Out(1)

    def __init__(self):
        self._net_3136 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
            self._net_3136.eq((((self.net_1526) & (self.net_1508) & (~(self._net_3136) & (self.enable))) | (self._net_3136))),
        ]

        m.d.comb += [
            self.net_934.eq(~(self._net_3136) & (self.enable)),
            self.net_3136.eq(self._net_3136),
        ]

        return m

class Jubilife(wiring.Component):
    net_934: In(1)
    net_1526: Out(1)
    net_832: Out(1)
    net_20: Out(1)
    net_380: Out(1)
    net_319: Out(1)

    def __init__(self):
        self._net_1526 = Signal(1)
        self._net_832 = Signal(1, init=0)
        self._net_20 = Signal(1, init=0)
        self._net_319 = Signal(1, init=0)
        self._net_380 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._net_1526.eq(~(self._net_319) & ~(self._net_380) & (self._net_832) & (self._net_20)),
        ]

        m.d.sync += [
            self._net_832.eq(~(((self.net_934) & (self._net_1526)) | (((self._net_20) & (self._net_319) & (self._net_380) & (self.net_934)) & (self._net_832)) | (~(((self._net_20) & (self._net_319) & (self._net_380) & (self.net_934)) | (self._net_832))))),
            self._net_20.eq(~(((self.net_934) & (self._net_1526)) | (~(((self._net_319) & (self.net_934)) | (self._net_20))) | ((self._net_20) & (self._net_319) & (self.net_934)))),
            self._net_319.eq(~((self._net_1526) | (~((self._net_319) ^ (self.net_934))))),
            self._net_380.eq((self._net_380) ^ ((self._net_20) & (self._net_319) & (self.net_934))),
        ]

        m.d.comb += [
            self.net_1526.eq(self._net_1526),
            self.net_832.eq(self._net_832),
            self.net_20.eq(self._net_20),
            self.net_380.eq(self._net_380),
            self.net_319.eq(self._net_319),
        ]

        return m

class Twinleaf(wiring.Component):
    net_934: In(1)
    net_1526: In(1)
    net_1508: Out(1)
    net_435: Out(1)
    net_323: Out(1)
    net_378: Out(1)
    net_377: Out(1)

    def __init__(self):
        self._net_1510 = Signal(1)
        self._net_1531 = Signal(1)
        self._net_1689 = Signal(1)
        self._net_378 = Signal(1, init=0)
        self._net_435 = Signal(1, init=0)
        self._net_323 = Signal(1, init=0)
        self._net_377 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._net_1510.eq(~(~(self._net_435) & (self._net_378) & (self._net_377))),
            self._net_1531.eq(~((self.net_1526) & (self.net_934))),
            self._net_1689.eq((self.net_1526) & (self.net_934) & (self._net_377) & (self._net_323)),
        ]

        m.d.sync += [
            self._net_378.eq((((self._net_323) | (self._net_1510) | (self._net_1531)) & (~((self._net_435) & (self._net_378) & (self._net_1689))) & ((((self._net_435) & (self._net_1689)) | (self._net_378))))),
            self._net_435.eq((self._net_435) ^ (self._net_1689)),
            self._net_323.eq(Mux((self._net_323), (self._net_1531), ((self.net_1526) & (self.net_934) & (self._net_1510)))),
            self._net_377.eq((((self._net_1510) | (self._net_1531)) & ((((self.net_1526) & (self.net_934) & (self._net_323)) | (self._net_377))) & (~(self._net_1689)))),
        ]

        m.d.comb += [
            self.net_1508.eq(~((self._net_323) | (self._net_1510))),
            self.net_435.eq(self._net_435),
            self.net_323.eq(self._net_323),
            self.net_378.eq(self._net_378),
            self.net_377.eq(self._net_377),
        ]

        return m

class Snowpoint(wiring.Component):
    net_934: In(1)
    net_1723: In(1)
    net_1719: In(1)
    I: In(1)
    net_2480: In(1)
    net_2475: In(1)
    net_2416: In(1)
    net_3283: In(1)
    net_2474: In(1)
    net_2471: In(1)
    net_2393: In(1)
    net_3830: In(1)
    net_1628: In(1)
    net_1738: In(1)
    net_2386: In(1)
    net_2463: In(1)
    net_2459: In(1)
    net_2259: Out(1)
    net_2505: Out(1)

    def __init__(self):
        self._net_2173 = Signal(1, init=0)
        self._net_2422 = Signal(1, init=0)
        self._net_2255 = Signal(1, init=0)
        self._net_2507 = Signal(1, init=0)
        self._net_2421 = Signal(1, init=0)
        self._net_2256 = Signal(1, init=0)
        self._net_2218 = Signal(1, init=0)
        self._net_2217 = Signal(1, init=0)
        self._net_2109 = Signal(1, init=0)
        self._net_2140 = Signal(1, init=0)
        self._net_2417 = Signal(1, init=0)
        self._net_2419 = Signal(1, init=0)
        self._net_2073 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
            self._net_2256.eq((((self.I) & (self.net_934) & ((((self.net_1738) & (self._net_2140)) | ((self.net_1628) & (self._net_2218)) | ((((self.net_1719) & (self._net_2422)) | ((self.net_1723) & (self._net_2421))))))) | (self._net_2256))),
        ]

        with m.If(self.net_934):
            m.d.sync += [
                self._net_2173.eq(self._net_2217),
                self._net_2422.eq(self.I),
                self._net_2255.eq(self._net_2417),
                self._net_2507.eq(self._net_2419),
                self._net_2421.eq(self._net_2218),
                self._net_2218.eq(self._net_2140),
                self._net_2217.eq(self._net_2255),
                self._net_2109.eq(self._net_2073),
                self._net_2140.eq(self._net_2109),
                self._net_2417.eq(self._net_2507),
                self._net_2419.eq(self._net_2422),
                self._net_2073.eq(self._net_2173),
            ]

        m.d.comb += [
            self.net_2259.eq(~(self._net_2256)),
            self.net_2505.eq(((self.net_3830) & (self.net_2393) & (self.net_2474) & (self.net_2471)) & ((self.net_3283) & (self.net_2416) & (self.net_2480) & (self.net_2475)) & ((self.net_2463) & (self.net_2459) & (self.net_2386))),
        ]

        return m

class Eterna(wiring.Component):
    net_1526: In(1)
    net_934: In(1)
    net_832: In(1)
    net_20: In(1)
    net_380: In(1)
    net_319: In(1)
    I: In(1)
    net_1723: Out(1)
    net_1719: Out(1)
    net_1628: Out(1)
    net_1738: Out(1)
    net_1557: Out(1)

    def __init__(self):
        self._net_1723 = Signal(1)
        self._net_1669 = Signal(1)
        self._net_1640 = Signal(1, init=0)
        self._net_1495 = Signal(1, init=0)
        self._net_1735 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._net_1723.eq(Buf(((self.net_319) | (self.net_20) | (self.net_380) | (self.net_832)))),
            self._net_1669.eq(~((self._net_1735) & (self.I))),
        ]

        m.d.sync += [
            self._net_1640.eq(~(((~(self._net_1640)) & (self._net_1669)) | (Mux((~(self.net_934)), (~(self._net_1640)), (self.net_1526))))),
            self._net_1495.eq((((self.net_1526) & (self.net_934) & (Mux((self._net_1640), ((self._net_1735) | (self.I)), (self._net_1669)))) | (self._net_1495))),
            self._net_1735.eq((((~(self.net_934)) & (self._net_1735)) | (((((self._net_1640) | (self._net_1669)) & ((self._net_1735) | (self.I)) & (self.net_934))) & (~(self.net_1526))))),
        ]

        m.d.comb += [
            self.net_1723.eq(self._net_1723),
            self.net_1719.eq((self.net_319) | (self.net_20) | (self.net_380) | (self.net_832)),
            self.net_1628.eq(1),
            self.net_1738.eq((self.net_319) | (self.net_380) | ~(self.net_832) | ~(self.net_20)),
            self.net_1557.eq(~(self._net_1495)),
        ]

        return m

class Oreburgh(wiring.Component):
    net_934: In(1)
    I: In(1)
    net_719: Out(1)
    net_1084: Out(1)
    net_791: Out(1)

    def __init__(self):
        self._net_803 = Signal(1)
        self._net_971 = Signal(1)
        self._net_888 = Signal(1)
        self._net_800 = Signal(1)
        self._net_802 = Signal(1, init=0)
        self._net_686 = Signal(1, init=0)
        self._net_684 = Signal(1, init=0)
        self._net_1104 = Signal(1, init=0)
        self._net_982 = Signal(1, init=0)
        self._net_769 = Signal(1, init=0)
        self._net_612 = Signal(1, init=0)
        self._net_919 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._net_803.eq((self._net_1104) & (self.I) & (self.net_934)),
            self._net_971.eq((self._net_684) & (self._net_686) & (self._net_802)),
            self._net_888.eq((self._net_612) & (self._net_769)),
            self._net_800.eq(~((self._net_803) & (self._net_971))),
        ]

        m.d.sync += [
            self._net_802.eq((((self._net_802) | ((self._net_684) & (self._net_686) & (self._net_803))) & (self._net_800))),
            self._net_686.eq(~((self._net_684) & (self._net_686) & (self._net_803)) & ((((self._net_684) & (self._net_803)) | (self._net_686)))),
            self._net_684.eq((((self.I) & (self.net_934) & (~(self._net_684) & (self._net_1104))) | ((~(self._net_803)) & (self._net_684)))),
            self._net_1104.eq(~((self._net_803) | (~(((self.I) & (self.net_934)) | (self._net_1104))))),
            self._net_982.eq((self._net_982) ^ ((self._net_919) & (self._net_888) & (self._net_803) & (self._net_971))),
            self._net_769.eq((((~((self._net_612) & (self._net_769))) | (self._net_800)) & ((((self._net_612) & (self._net_803) & (self._net_971)) | (self._net_769))))),
            self._net_612.eq(~((self._net_612) ^ (self._net_800))),
            self._net_919.eq(~((self._net_919) & (self._net_888) & (self._net_803) & (self._net_971)) & ((((self._net_888) & (self._net_803) & (self._net_971)) | (self._net_919)))),
        ]

        m.d.comb += [
            self.net_719.eq((self._net_684) & (self._net_686) & (self._net_612) & (~((self._net_769) | (self._net_919) | ((self._net_1104) | (self._net_802) | (self._net_982))))),
            self.net_1084.eq((~(self._net_686) & ~(self._net_982) & (self._net_919) & (self._net_802)) & (~(self._net_684) & (self._net_1104)) & (self._net_888)),
            self.net_791.eq(~((self._net_684) | (self._net_686) | (self._net_612) | ~(~((self._net_769) | (self._net_919) | ((self._net_1104) | (self._net_802) | (self._net_982)))))),
        ]

        return m

class Sandgem(wiring.Component):
    net_204: In(1)
    net_203: In(1)
    net_294: In(1)
    net_226: In(1)
    net_545: In(1)
    net_1185: In(1)
    net_341: In(1)
    net_401: In(1)
    net_399: In(1)
    net_405: In(1)
    net_349: In(1)
    net_343: Out(1)

    def __init__(self):

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
        ]

        m.d.comb += [
            self.net_343.eq(((self.net_226) & (self.net_294) & (self.net_204) & (self.net_203)) & ((self.net_349) & (self.net_405) & (self.net_401) & (self.net_399)) & ((self.net_1185) & (self.net_341) & (self.net_545))),
        ]

        return m

class Celestic(wiring.Component):
    net_934: In(1)
    I: In(1)
    net_319: In(1)
    net_832: In(1)
    net_20: In(1)
    net_380: In(1)
    net_2386: Out(1)
    net_2463: Out(1)
    net_2459: Out(1)

    def __init__(self):
        self._net_4199 = Signal(1, init=0)
        self._net_4274 = Signal(1, init=0)
        self._net_4147 = Signal(1, init=0)
        self._net_4163 = Signal(1, init=0)
        self._net_4160 = Signal(1, init=0)
        self._net_4300 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
            self._net_4199.eq((((self._net_4163) | (~((self.I) & (self.net_934) & (self._net_4199) & (~(self.net_20) & ~(self.net_380) & (self.net_832) & (self.net_319))))) & ((((self.I) & (self.net_934) & (~(self.net_20) & ~(self.net_380) & (self.net_832) & (self.net_319))) | (self._net_4199))))),
            self._net_4274.eq((((self._net_4300) | (~((self.I) & (self.net_934) & (self._net_4274) & (~(self.net_319) & ~(self.net_380) & (self.net_832) & (self.net_20))))) & ((((self.I) & (self.net_934) & (~(self.net_319) & ~(self.net_380) & (self.net_832) & (self.net_20))) | (self._net_4274))))),
            self._net_4147.eq((((self._net_4147) | (~(((self.net_20) | (self.net_319) | (self.net_380) | ~(self.net_832)) | (~((self.I) & (self.net_934)))))) & ((self._net_4160) | (~(self._net_4147)) | ((self.net_20) | (self.net_319) | (self.net_380) | ~(self.net_832)) | (~((self.I) & (self.net_934)))))),
            self._net_4163.eq(~(~(self._net_4163) & (~((self.I) & (self.net_934) & (self._net_4199) & (~(self.net_20) & ~(self.net_380) & (self.net_832) & (self.net_319)))))),
            self._net_4160.eq((((self._net_4147) & (~(((self.net_20) | (self.net_319) | (self.net_380) | ~(self.net_832)) | (~((self.I) & (self.net_934)))))) | (self._net_4160))),
            self._net_4300.eq(~(~(self._net_4300) & (~((self.I) & (self.net_934) & (self._net_4274) & (~(self.net_319) & ~(self.net_380) & (self.net_832) & (self.net_20)))))),
        ]

        m.d.comb += [
            self.net_2386.eq(~(self._net_4274) & (self._net_4300)),
            self.net_2463.eq(~(self._net_4199) & (self._net_4163)),
            self.net_2459.eq((self._net_4160) & (~(self._net_4147))),
        ]

        return m

class Hearthome(wiring.Component):
    net_934: In(1)
    I: In(1)
    net_20: In(1)
    net_319: In(1)
    net_380: In(1)
    net_832: In(1)
    net_2480: Out(1)
    net_2475: Out(1)
    net_3283: Out(1)
    net_2474: Out(1)
    net_2471: Out(1)
    net_2393: Out(1)
    net_3830: Out(1)

    def __init__(self):
        self._net_3755 = Signal(1, init=0)
        self._net_3675 = Signal(1, init=0)
        self._net_3902 = Signal(1, init=0)
        self._net_3325 = Signal(1, init=0)
        self._net_3139 = Signal(1, init=0)
        self._net_4028 = Signal(1, init=0)
        self._net_3470 = Signal(1, init=0)
        self._net_4023 = Signal(1, init=0)
        self._net_3751 = Signal(1, init=0)
        self._net_3676 = Signal(1, init=0)
        self._net_3861 = Signal(1, init=0)
        self._net_3471 = Signal(1, init=0)
        self._net_3320 = Signal(1, init=0)
        self._net_3148 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
            self._net_3755.eq((((self._net_3751) | (~((self.I) & (self.net_934) & (self._net_3755) & (~(self.net_20) & ~(self.net_832) & (self.net_380) & (self.net_319))))) & ((((self.I) & (self.net_934) & (~(self.net_20) & ~(self.net_832) & (self.net_380) & (self.net_319))) | (self._net_3755))))),
            self._net_3675.eq((((self._net_3676) & (~(((self.net_20) | (self.net_319) | (self.net_832) | ~(self.net_380)) | (~((self.I) & (self.net_934)))))) | (self._net_3675))),
            self._net_3902.eq((((self._net_3861) | (~((self.I) & (self.net_934) & (self._net_3902) & (~(self.net_319) & ~(self.net_832) & (self.net_380) & (self.net_20))))) & ((((self.I) & (self.net_934) & (~(self.net_319) & ~(self.net_832) & (self.net_380) & (self.net_20))) | (self._net_3902))))),
            self._net_3325.eq((((self._net_3320) & (~(((self.net_319) | (self.net_832) | (self.net_380) | ~(self.net_20)) | (~((self.I) & (self.net_934)))))) | (self._net_3325))),
            self._net_3139.eq((((self._net_3139) | (~(((self.net_20) | (self.net_832) | (self.net_380) | ~(self.net_319)) | (~((self.I) & (self.net_934)))))) & ((self._net_3148) | (~(self._net_3139)) | ((self.net_20) | (self.net_832) | (self.net_380) | ~(self.net_319)) | (~((self.I) & (self.net_934)))))),
            self._net_4028.eq((((self._net_4023) | (~((self.I) & (self.net_934) & (self._net_4028) & (~(self.net_832) & (self.net_380) & (self.net_319) & (self.net_20))))) & ((((self.I) & (self.net_934) & (~(self.net_832) & (self.net_380) & (self.net_319) & (self.net_20))) | (self._net_4028))))),
            self._net_3470.eq((((self._net_3471) | (~((self.I) & (self.net_934) & (self._net_3470) & (~(self.net_832) & ~(self.net_380) & (self.net_319) & (self.net_20))))) & ((((self.I) & (self.net_934) & (~(self.net_832) & ~(self.net_380) & (self.net_319) & (self.net_20))) | (self._net_3470))))),
            self._net_4023.eq(~(~(self._net_4023) & (~((self.I) & (self.net_934) & (self._net_4028) & (~(self.net_832) & (self.net_380) & (self.net_319) & (self.net_20)))))),
            self._net_3751.eq(~(~(self._net_3751) & (~((self.I) & (self.net_934) & (self._net_3755) & (~(self.net_20) & ~(self.net_832) & (self.net_380) & (self.net_319)))))),
            self._net_3676.eq((((self._net_3676) | (~(((self.net_20) | (self.net_319) | (self.net_832) | ~(self.net_380)) | (~((self.I) & (self.net_934)))))) & ((self._net_3675) | (~(self._net_3676)) | ((self.net_20) | (self.net_319) | (self.net_832) | ~(self.net_380)) | (~((self.I) & (self.net_934)))))),
            self._net_3861.eq(~(~(self._net_3861) & (~((self.I) & (self.net_934) & (self._net_3902) & (~(self.net_319) & ~(self.net_832) & (self.net_380) & (self.net_20)))))),
            self._net_3471.eq(~(~(self._net_3471) & (~((self.I) & (self.net_934) & (self._net_3470) & (~(self.net_832) & ~(self.net_380) & (self.net_319) & (self.net_20)))))),
            self._net_3320.eq((((self._net_3320) | (~(((self.net_319) | (self.net_832) | (self.net_380) | ~(self.net_20)) | (~((self.I) & (self.net_934)))))) & ((self._net_3325) | (~(self._net_3320)) | ((self.net_319) | (self.net_832) | (self.net_380) | ~(self.net_20)) | (~((self.I) & (self.net_934)))))),
            self._net_3148.eq((((self._net_3139) & (~(((self.net_20) | (self.net_832) | (self.net_380) | ~(self.net_319)) | (~((self.I) & (self.net_934)))))) | (self._net_3148))),
        ]

        m.d.comb += [
            self.net_2480.eq(~(self._net_3470) & (self._net_3471)),
            self.net_2475.eq((self._net_3325) & (~(self._net_3320))),
            self.net_3283.eq((self._net_3148) & (~(self._net_3139))),
            self.net_2474.eq(~(self._net_4028) & (self._net_4023)),
            self.net_2471.eq(~(self._net_3902) & (self._net_3861)),
            self.net_2393.eq((self._net_3675) & (~(self._net_3676))),
            self.net_3830.eq(~(self._net_3755) & (self._net_3751)),
        ]

        return m

class Solaceon(wiring.Component):
    net_934: In(1)
    I: In(1)
    net_20: In(1)
    net_319: In(1)
    net_832: In(1)
    net_380: In(1)
    net_2416: Out(1)

    def __init__(self):
        self._net_2922 = Signal(1, init=0)
        self._net_2819 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
            self._net_2922.eq((((self._net_2819) | (~((self.I) & (self.net_934) & (self._net_2922) & (~((self.net_20) | (self.net_319) | (self.net_832) | (self.net_380)))))) & ((((self.I) & (self.net_934) & (~((self.net_20) | (self.net_319) | (self.net_832) | (self.net_380)))) | (self._net_2922))))),
            self._net_2819.eq(~(~(self._net_2819) & (~((self.I) & (self.net_934) & (self._net_2922) & (~((self.net_20) | (self.net_319) | (self.net_832) | (self.net_380))))))),
        ]

        m.d.comb += [
            self.net_2416.eq(~(self._net_2922) & (self._net_2819)),
        ]

        return m

class Pastoria(wiring.Component):
    net_934: In(1)
    I: In(1)
    net_736: In(1)
    net_1034: In(1)
    net_857: In(1)
    net_985: In(1)
    net_204: Out(1)
    net_203: Out(1)
    net_294: Out(1)
    net_226: Out(1)
    net_545: Out(1)
    net_1185: Out(1)
    net_341: Out(1)
    net_401: Out(1)
    net_399: Out(1)
    net_405: Out(1)
    net_349: Out(1)

    def __init__(self):
        self._net_2038 = Signal(1, init=0)
        self._net_2221 = Signal(1, init=0)
        self._net_1965 = Signal(1, init=0)
        self._net_2204 = Signal(1, init=0)
        self._net_2017 = Signal(1, init=0)
        self._net_1921 = Signal(1, init=0)
        self._net_1967 = Signal(1, init=0)
        self._net_840 = Signal(1, init=0)
        self._net_1488 = Signal(1, init=0)
        self._net_1748 = Signal(1, init=0)
        self._net_1593 = Signal(1, init=0)
        self._net_1856 = Signal(1, init=0)
        self._net_1193 = Signal(1, init=0)
        self._net_1293 = Signal(1, init=0)
        self._net_1522 = Signal(1, init=0)
        self._net_1439 = Signal(1, init=0)
        self._net_1672 = Signal(1, init=0)
        self._net_1247 = Signal(1, init=0)
        self._net_1288 = Signal(1, init=0)
        self._net_1191 = Signal(1, init=0)
        self._net_1226 = Signal(1, init=0)
        self._net_1032 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
            self._net_2038.eq(~(~(self._net_2038) & (~((self.I) & (self.net_934) & (self._net_1965) & (~(self.net_857) & ~(self.net_985) & (self.net_1034) & (self.net_736)))))),
            self._net_2221.eq(~(~(self._net_2221) & (~((self.I) & (self.net_934) & (self._net_2204) & (~(self.net_736) & ~(self.net_985) & (self.net_1034) & (self.net_857)))))),
            self._net_1965.eq((((self._net_2038) | (~((self.I) & (self.net_934) & (self._net_1965) & (~(self.net_857) & ~(self.net_985) & (self.net_1034) & (self.net_736))))) & ((((self.I) & (self.net_934) & (~(self.net_857) & ~(self.net_985) & (self.net_1034) & (self.net_736))) | (self._net_1965))))),
            self._net_2204.eq((((self._net_2221) | (~((self.I) & (self.net_934) & (self._net_2204) & (~(self.net_736) & ~(self.net_985) & (self.net_1034) & (self.net_857))))) & ((((self.I) & (self.net_934) & (~(self.net_736) & ~(self.net_985) & (self.net_1034) & (self.net_857))) | (self._net_2204))))),
            self._net_2017.eq((((self._net_2017) | (~(((self.net_857) | (self.net_736) | (self.net_985) | ~(self.net_1034)) | (~((self.I) & (self.net_934)))))) & ((self._net_1967) | (~(self._net_2017)) | ((self.net_857) | (self.net_736) | (self.net_985) | ~(self.net_1034)) | (~((self.I) & (self.net_934)))))),
            self._net_1921.eq((((self._net_1856) | (~((self.I) & (self.net_934) & (self._net_1921) & (~(self.net_1034) & (self.net_985) & (self.net_736) & (self.net_857))))) & ((((self.I) & (self.net_934) & (~(self.net_1034) & (self.net_985) & (self.net_736) & (self.net_857))) | (self._net_1921))))),
            self._net_1967.eq((((self._net_2017) & (~(((self.net_857) | (self.net_736) | (self.net_985) | ~(self.net_1034)) | (~((self.I) & (self.net_934)))))) | (self._net_1967))),
            self._net_840.eq(~(~(self._net_840) & (~((self.I) & (self.net_934) & (self._net_1032) & (~((self.net_857) | (self.net_736) | (self.net_1034) | (self.net_985))))))),
            self._net_1488.eq((((self._net_1522) & (~(((self.net_857) | (self.net_736) | (self.net_1034) | ~(self.net_985)) | (~((self.I) & (self.net_934)))))) | (self._net_1488))),
            self._net_1748.eq(~(~(self._net_1748) & (~((self.I) & (self.net_934) & (self._net_1672) & (~(self.net_736) & ~(self.net_1034) & (self.net_985) & (self.net_857)))))),
            self._net_1593.eq(~(~(self._net_1593) & (~((self.I) & (self.net_934) & (self._net_1439) & (~(self.net_857) & ~(self.net_1034) & (self.net_985) & (self.net_736)))))),
            self._net_1856.eq(~(~(self._net_1856) & (~((self.I) & (self.net_934) & (self._net_1921) & (~(self.net_1034) & (self.net_985) & (self.net_736) & (self.net_857)))))),
            self._net_1193.eq((((self._net_1193) | (~(((self.net_736) | (self.net_1034) | (self.net_985) | ~(self.net_857)) | (~((self.I) & (self.net_934)))))) & ((self._net_1288) | (~(self._net_1193)) | ((self.net_736) | (self.net_1034) | (self.net_985) | ~(self.net_857)) | (~((self.I) & (self.net_934)))))),
            self._net_1293.eq((((self._net_1247) | (~((self.I) & (self.net_934) & (self._net_1293) & (~(self.net_1034) & ~(self.net_985) & (self.net_736) & (self.net_857))))) & ((((self.I) & (self.net_934) & (~(self.net_1034) & ~(self.net_985) & (self.net_736) & (self.net_857))) | (self._net_1293))))),
            self._net_1522.eq((((self._net_1522) | (~(((self.net_857) | (self.net_736) | (self.net_1034) | ~(self.net_985)) | (~((self.I) & (self.net_934)))))) & ((self._net_1488) | (~(self._net_1522)) | ((self.net_857) | (self.net_736) | (self.net_1034) | ~(self.net_985)) | (~((self.I) & (self.net_934)))))),
            self._net_1439.eq((((self._net_1593) | (~((self.I) & (self.net_934) & (self._net_1439) & (~(self.net_857) & ~(self.net_1034) & (self.net_985) & (self.net_736))))) & ((((self.I) & (self.net_934) & (~(self.net_857) & ~(self.net_1034) & (self.net_985) & (self.net_736))) | (self._net_1439))))),
            self._net_1672.eq((((self._net_1748) | (~((self.I) & (self.net_934) & (self._net_1672) & (~(self.net_736) & ~(self.net_1034) & (self.net_985) & (self.net_857))))) & ((((self.I) & (self.net_934) & (~(self.net_736) & ~(self.net_1034) & (self.net_985) & (self.net_857))) | (self._net_1672))))),
            self._net_1247.eq(~(~(self._net_1247) & (~((self.I) & (self.net_934) & (self._net_1293) & (~(self.net_1034) & ~(self.net_985) & (self.net_736) & (self.net_857)))))),
            self._net_1288.eq((((self._net_1193) & (~(((self.net_736) | (self.net_1034) | (self.net_985) | ~(self.net_857)) | (~((self.I) & (self.net_934)))))) | (self._net_1288))),
            self._net_1191.eq((((self._net_1226) & (~(((self.net_857) | (self.net_1034) | (self.net_985) | ~(self.net_736)) | (~((self.I) & (self.net_934)))))) | (self._net_1191))),
            self._net_1226.eq((((self._net_1226) | (~(((self.net_857) | (self.net_1034) | (self.net_985) | ~(self.net_736)) | (~((self.I) & (self.net_934)))))) & ((self._net_1191) | (~(self._net_1226)) | ((self.net_857) | (self.net_1034) | (self.net_985) | ~(self.net_736)) | (~((self.I) & (self.net_934)))))),
            self._net_1032.eq((((self._net_840) | (~((self.I) & (self.net_934) & (self._net_1032) & (~((self.net_857) | (self.net_736) | (self.net_1034) | (self.net_985)))))) & ((((self.I) & (self.net_934) & (~((self.net_857) | (self.net_736) | (self.net_1034) | (self.net_985)))) | (self._net_1032))))),
        ]

        m.d.comb += [
            self.net_204.eq(~(self._net_1921) & (self._net_1856)),
            self.net_203.eq(~(self._net_1672) & (self._net_1748)),
            self.net_294.eq((self._net_1488) & (~(self._net_1522))),
            self.net_226.eq(~(self._net_1439) & (self._net_1593)),
            self.net_545.eq(~(self._net_2204) & (self._net_2221)),
            self.net_1185.eq(~(self._net_1965) & (self._net_2038)),
            self.net_341.eq((self._net_1967) & (~(self._net_2017))),
            self.net_401.eq(~(self._net_1293) & (self._net_1247)),
            self.net_399.eq((self._net_1288) & (~(self._net_1193))),
            self.net_405.eq(~(self._net_1032) & (self._net_840)),
            self.net_349.eq((self._net_1191) & (~(self._net_1226))),
        ]

        return m

class Veilstone(wiring.Component):
    net_2259: In(1)
    net_3136: In(1)
    net_2505: In(1)
    net_343: In(1)
    net_1557: In(1)
    net_719: In(1)
    net_3771: Out(1)
    net_3920: Out(1)
    success: Out(1)

    def __init__(self):
        self._net_3771 = Signal(1, init=0)
        self._net_3920 = Signal(1, init=0)
        self._success = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
            self._net_3771.eq((self.net_3136) | (self._net_3771)),
            self._net_3920.eq((((~(self.net_2259)) & ((self.net_1557) & (self.net_719)) & (~(self._net_3771) & (self.net_3136) & (self.net_343) & (self.net_2505))) | ((self._net_3920) & (~(~(self._net_3771) & (self.net_3136)))))),
            self._success.eq((((self.net_2259) & ((self.net_1557) & (self.net_719)) & (~(self._net_3771) & (self.net_3136) & (self.net_343) & (self.net_2505))) | ((self._success) & (~(~(self._net_3771) & (self.net_3136)))))),
        ]

        m.d.comb += [
            self.net_3771.eq(self._net_3771),
            self.net_3920.eq(self._net_3920),
            self.success.eq(self._success),
        ]

        return m

class Output_MtCoronet(wiring.Component):
    net_3771: In(1)
    net_3920: In(1)
    net_1084: In(1)
    net_791: In(1)
    net_3617: In(1)
    net_3516: In(1)
    net_3435: In(1)
    net_3543: In(1)
    net_3552: In(1)
    net_3613: In(1)
    success: In(1)
    net_3518: In(1)
    net_3818: In(1)
    net_1351: Out(1)
    net_1365: Out(1)
    net_3037: Out(1)
    net_3419: Out(1)
    net_3420: Out(1)
    net_3384: Out(1)
    net_1505: Out(1)
    net_1363: Out(1)
    O_0_: Out(1)
    O_1_: Out(1)
    O_2_: Out(1)
    O_3_: Out(1)
    O_4_: Out(1)
    O_5_: Out(1)
    O_6_: Out(1)
    O_7_: Out(1)

    def __init__(self):
        self._net_3874 = Signal(1)
        self._net_1365 = Signal(1, reset_less=True)
        self._net_1351 = Signal(1, reset_less=True)
        self._net_1363 = Signal(1, reset_less=True)
        self._net_1505 = Signal(1, reset_less=True)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._net_3874.eq(~((self._net_1505) & (self._net_1365) & (self._net_1363) & (self._net_1351))),
        ]

        m.d.sync += [
            self._net_1365.eq((((self._net_1505) | (~((self._net_1365) & (self._net_1363) & (self._net_1351)))) & ((((self._net_1363) & (self._net_1351)) | (self._net_1365))) & (self.net_3771))),
            self._net_1351.eq(~(((self._net_1351) & (self._net_3874)) | (~(self.net_3771)))),
            self._net_1363.eq(~(((self._net_3874) & (~((self._net_1363) ^ (self._net_1351)))) | (~(self.net_3771)))),
            self._net_1505.eq(~(((~(self._net_1505)) & (~((self._net_1365) & (self._net_1363) & (self._net_1351)))) | (~(self.net_3771)))),
        ]

        m.d.comb += [
            self.net_1351.eq(self._net_1351),
            self.net_1365.eq(self._net_1365),
            self.net_3037.eq((self.net_3771) & (self._net_3874)),
            self.net_3419.eq(~((self.net_791) | ((((self.success) | (self.net_3920)) & ~(self.net_1084))))),
            self.net_3420.eq(~((self.net_791) | (self.success) | (self.net_1084) | ~(self.net_3920))),
            self.net_3384.eq(~(((~(self.success)) & (self.net_3920)) | (self.net_1084) | (self.net_791))),
            self.net_1505.eq(self._net_1505),
            self.net_1363.eq(self._net_1363),
            self.O_0_.eq((self.net_3771) & (self.net_3617) & (self._net_3874)),
            self.O_1_.eq((self.net_3771) & (self.net_3818) & (self._net_3874)),
            self.O_2_.eq((self.net_3771) & (self.net_3516) & (self._net_3874)),
            self.O_3_.eq((self.net_3771) & (self.net_3613) & (self._net_3874)),
            self.O_4_.eq((self.net_3771) & (self.net_3552) & (self._net_3874)),
            self.O_5_.eq((self.net_3771) & (self.net_3543) & (self._net_3874)),
            self.O_6_.eq((self.net_3771) & (self.net_3518) & (self._net_3874)),
            self.O_7_.eq((self.net_3771) & (self.net_3435) & (self._net_3874)),
        ]

        return m

class Output_EternaForest(wiring.Component):
    net_1351: In(1)
    net_1365: In(1)
    net_2232: In(1)
    net_2006: In(1)
    net_1425: In(1)
    net_1693: In(1)
    net_1694: In(1)
    net_1516: In(1)
    net_2313: In(1)
    net_1977: In(1)
    net_1927: In(1)
    net_2315: In(1)
    net_2088: In(1)
    net_2298: In(1)
    net_2120: In(1)
    net_2460: In(1)
    net_2117: In(1)
    net_2240: In(1)
    net_2189: In(1)
    net_1420: In(1)
    net_3037: In(1)
    net_934: In(1)
    net_3419: In(1)
    net_3420: In(1)
    net_3384: In(1)
    net_1559: In(1)
    net_1816: In(1)
    net_1936: In(1)
    net_1629: In(1)
    net_1472: In(1)
    net_2461: In(1)
    net_2154: In(1)
    net_1905: In(1)
    net_1815: In(1)
    net_1928: In(1)
    net_2479: In(1)
    net_2004: In(1)
    net_1907: In(1)
    net_1822: In(1)
    net_1505: In(1)
    I: In(1)
    net_1363: In(1)
    net_3617: Out(1)
    net_3516: Out(1)
    net_3435: Out(1)
    net_3543: Out(1)
    net_3552: Out(1)
    net_3613: Out(1)
    net_3518: Out(1)
    net_3818: Out(1)

    def __init__(self):
        self._net_2834 = Signal(1)
        self._net_2687 = Signal(1)
        self._net_3408 = Signal(1)
        self._net_3593 = Signal(1)
        self._net_3488 = Signal(1)
        self._net_3258 = Signal(1)
        self._net_3251 = Signal(1)
        self._net_3265 = Signal(1)
        self._net_2515 = Signal(1)
        self._net_2593 = Signal(1)
        self._net_2599 = Signal(1)
        self._net_2754 = Signal(1)
        self._net_2513 = Signal(1)
        self._net_2543 = Signal(1)
        self._net_2829 = Signal(1)
        self._net_2667 = Signal(1)
        self._net_2576 = Signal(1)
        self._net_2949 = Signal(1, init=0)
        self._net_2609 = Signal(1, init=0)
        self._net_2676 = Signal(1, init=0)
        self._net_2689 = Signal(1, init=1)
        self._net_2826 = Signal(1, init=1)
        self._net_2674 = Signal(1, init=1)
        self._net_2743 = Signal(1, init=1)
        self._net_2752 = Signal(1, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._net_2834.eq(~((self._net_2676) ^ (~((self._net_2752) ^ (self._net_2609))))),
            self._net_2687.eq(~(~(self.net_934) & (self.net_3037))),
            self._net_3408.eq(~((self._net_3251) | (self._net_3265))),
            self._net_3593.eq(~((self.net_3384) | (self.net_3419) | (self.net_3420))),
            self._net_3488.eq(~((self.net_3384) | (self.net_3420) | ~(self.net_3419))),
            self._net_3258.eq(~((self.net_3384) | (self.net_3419) | ~(self.net_3420))),
            self._net_3251.eq(~((self.net_3419) | (self.net_3420) | ~(self.net_3384))),
            self._net_3265.eq(~(((self.net_3419) & (self.net_3420)) | (self.net_3384))),
            self._net_2515.eq(~((~((self._net_2752) ^ (self._net_2609))) ^ (~((self._net_2826) ^ (self._net_2743))))),
            self._net_2593.eq(~(self.net_1505)),
            self._net_2599.eq(~(self.net_1351) & (self.net_1363)),
            self._net_2754.eq(~((self.net_3037) | (self.net_934))),
            self._net_2513.eq(~((self.net_1351) & (self.net_1363))),
            self._net_2543.eq((self.net_1363) | (self.net_1365)),
            self._net_2829.eq((self.net_3037) | (self.net_934)),
            self._net_2667.eq(~((self.net_1351) | (self._net_2593))),
            self._net_2576.eq(~((self.net_1505) ^ ((self.net_1351) & (self.net_1363) & (self.net_1365)))),
        ]

        m.d.sync += [
            self._net_2949.eq((((self.net_934) & (self._net_2674)) | ((self._net_2949) & (self._net_2754)) | (~((self._net_2687) | (~((self._net_2676) ^ ((self._net_2609) ^ (self._net_2743)))))))),
            self._net_2609.eq((((self._net_2609) | (self._net_2829)) & ((~((self.net_934) | (~((self._net_2674) ^ ((self._net_2609) ^ (self._net_2949)))) | ~(self._net_2515))) | ((((self.net_934) & (self._net_2689)) | ((~((self.net_934) | (self._net_2515))) & (~((self._net_2674) ^ ((self._net_2609) ^ (self._net_2949))))) | (self._net_2754)))))),
            self._net_2676.eq((((~(self.net_934) & (self.net_3037)) & (~((self._net_2689) & (self._net_2834))) & ((self._net_2689) | (self._net_2834))) | ((((self.net_934) & (self._net_2826)) | ((self._net_2754) & (self._net_2676)))))),
            self._net_2689.eq((((~((self._net_2674) ^ (self._net_2834)) & (~((self.net_934) | (self._net_2515)))) | (~(self.net_934) & (self._net_2515) & ((self._net_2674) ^ (self._net_2834))) | ((((self.net_934) & (self._net_2949)) | (self._net_2754)))) & ((self._net_2829) | (self._net_2689)))),
            self._net_2826.eq((((~(self.net_934) & (self.net_3037)) & (~((~((self._net_2689) ^ (self._net_2826))) ^ ((self._net_2609) ^ (self._net_2949))))) | ((((self.net_934) & (self._net_2752)) | ((self._net_2826) & (self._net_2754)))))),
            self._net_2674.eq((((self._net_2674) | (self._net_2829)) & ((self._net_2687) | (~((self._net_2676) ^ (~((self._net_2689) ^ (self._net_2826)))))) & (~(((self.I) | (self._net_2515)) & (~(((self.I) & (self._net_2515)) | (~(self.net_934)))))))),
            self._net_2743.eq((((self.net_934) & (self._net_2676)) | ((self._net_2743) & (self._net_2754)) | (~((self._net_2515) | (self._net_2687))))),
            self._net_2752.eq((((self.net_934) & (self._net_2609)) | ((self._net_2754) & (self._net_2752)) | (((((self._net_2689) ^ (self._net_2949)) | ((self._net_2674) ^ (self._net_2752))) & (~((((self._net_2689) ^ (self._net_2949)) & ((self._net_2674) ^ (self._net_2752))) | (self._net_2687))))))),
        ]

        m.d.comb += [
            self.net_3617.eq((((self._net_3408) | ((((self.net_2232) & (self._net_3488)) | ((self._net_3593) & (self.net_2006)))) | ((((~((self._net_2674) ^ (~(((~((self.net_1365) & (self._net_2599))) & (~((self.net_1363) & (self.net_1505)))) | (self._net_2667))))) & (self._net_3251)) | ((self._net_3258) & (self.net_1559))))) & ((self.net_1816) | (self._net_3251) | (self._net_3265)))),
            self.net_3516.eq((((self._net_3408) | ((((self.net_2313) & (self._net_3488)) | ((self._net_3593) & (self.net_1977)))) | ((((~((self._net_2689) ^ (~(((~(~((self.net_1365) & (self._net_2599)))) | (~((self._net_2543) & (self._net_2576)))) & ((((self.net_1351) & (self.net_1365)) | (self._net_2593) | (self._net_2599))))))) & (self._net_3251)) | ((self._net_3258) & (self.net_1694))))) & ((self.net_1907) | (self._net_3251) | (self._net_3265)))),
            self.net_3435.eq((((self._net_3408) | ((((self.net_2479) & (self._net_3488)) | ((self._net_3593) & (self.net_2004)))) | ((((~((self._net_2743) ^ ((((self.net_1365) & (self._net_2593) & (self._net_2513)) | (~(((self.net_1351) & (self._net_2593)) | ((self._net_2543) & (self._net_2513)))))))) & (self._net_3251)) | ((self._net_3258) & (self.net_1425))))) & ((self.net_1815) | (self._net_3251) | (self._net_3265)))),
            self.net_3543.eq((((self._net_3408) | ((((self.net_2298) & (self._net_3488)) | ((self._net_3593) & (self.net_2120)))) | (((((self._net_2826) ^ (~((~(~(self.net_1363) & (self.net_1351))) & ((((self._net_2667) & (self._net_2543)) | ((self._net_2576) & ((self.net_1351) | (self.net_1365) | ~(self.net_1363)))))))) & (self._net_3251)) | ((self._net_3258) & (self.net_1693))))) & ((self.net_1905) | (self._net_3251) | (self._net_3265)))),
            self.net_3552.eq((((self._net_3408) | ((((self.net_2240) & (self._net_3488)) | ((self._net_3593) & (self.net_2189)))) | (((((self._net_2752) ^ ((((self.net_1365) | (self._net_2667) | (self._net_2599)) & (~((self.net_1363) & (self.net_1505)))))) & (self._net_3251)) | ((self._net_3258) & (self.net_1472))))) & ((self.net_1927) | (self._net_3251) | (self._net_3265)))),
            self.net_3613.eq((((self._net_3408) | ((((self.net_2460) & (self._net_3488)) | ((self._net_3593) & (self.net_2117)))) | (((((self._net_2609) ^ ((((~(~((self.net_1365) & (self._net_2599)))) | (self._net_2576) | (~((self.net_1365) | (~(~((self.net_1351) | (self.net_1363))) & (self._net_2513))))) & ((~(~((self.net_1351) | (self.net_1363))) & (self._net_2513)) | (~((self._net_2543) & (self._net_2576))))))) & (self._net_3251)) | ((self._net_3258) & (self.net_1516))))) & ((self.net_1936) | (self._net_3251) | (self._net_3265)))),
            self.net_3518.eq((((self._net_3408) | ((((self.net_2461) & (self._net_3488)) | ((self._net_3593) & (self.net_2154)))) | ((((~((self._net_2676) ^ ((((self.net_1351) & (~((self.net_1365) | (self.net_1505)))) | ((~(~(self.net_1363) & (self.net_1351))) & (self.net_1365)))))) & (self._net_3251)) | ((self._net_3258) & (self.net_1629))))) & ((self.net_1928) | (self._net_3251) | (self._net_3265)))),
            self.net_3818.eq((((self._net_3408) | ((((self.net_2315) & (self._net_3488)) | ((self._net_3593) & (self.net_2088)))) | ((((~(((self._net_2667) | (~((self.net_1351) | (self.net_1363))) | (~((self.net_1365) | (self.net_1505)))) ^ ((self._net_2949) ^ (self._net_2543)))) & (self._net_3251)) | ((self._net_3258) & (self.net_1420))))) & ((self.net_1822) | (self._net_3251) | (self._net_3265)))),
        ]

        return m

class Output_LakeAcuity(wiring.Component):
    net_1351: In(1)
    net_1505: In(1)
    net_1365: In(1)
    net_1363: In(1)
    net_2232: Out(1)
    net_2006: Out(1)
    net_2313: Out(1)
    net_1977: Out(1)
    net_2315: Out(1)
    net_2088: Out(1)
    net_2298: Out(1)
    net_2120: Out(1)
    net_2460: Out(1)
    net_2117: Out(1)
    net_2240: Out(1)
    net_2189: Out(1)
    net_2461: Out(1)
    net_2154: Out(1)
    net_2479: Out(1)
    net_2004: Out(1)

    def __init__(self):
        self._net_2303 = Signal(1)
        self._net_2224 = Signal(1)
        self._net_1992 = Signal(1)
        self._net_1973 = Signal(1)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._net_2303.eq(~(self.net_1365) & (self.net_1363)),
            self._net_2224.eq(~(self.net_1505)),
            self._net_1992.eq((self.net_1365) | (self.net_1505)),
            self._net_1973.eq(~(self.net_1363) & (self.net_1351)),
        ]

        m.d.sync += [
        ]

        m.d.comb += [
            self.net_2232.eq(((((self.net_1351) & (self.net_1363) & (self.net_1365)) | (~(self.net_1363) & (self.net_1351)) | (~((self.net_1351) | (self.net_1365) | ~(self.net_1363)))) & (self._net_2224))),
            self.net_2006.eq(~(((self._net_1992) & (self._net_1973)) | (Mux((self.net_1365), (self.net_1505), (self.net_1363))))),
            self.net_2313.eq((((~(self.net_1351)) | (self.net_1365)) & (self._net_2224) & (self.net_1363))),
            self.net_1977.eq(~(self._net_1992) & (~(~(self.net_1351) & (self.net_1363)))),
            self.net_2315.eq((((~(self.net_1351)) | ((self.net_1351) & (self.net_1363) & (self.net_1365))) & (self._net_2224))),
            self.net_2088.eq(~(self.net_1505) & (self.net_1365) & (self.net_1363)),
            self.net_2298.eq((self.net_1351) & (self._net_2224) & (self._net_2303)),
            self.net_2120.eq(~(self.net_1505) & (self._net_1973) & (self.net_1365)),
            self.net_2460.eq(~(((self.net_1351) & (self.net_1365)) | (self.net_1505) | (self._net_2303) | (~((self.net_1351) | (self.net_1363))))),
            self.net_2117.eq((((self._net_1992) | (self._net_1973)) & ((~((self.net_1505) | (self._net_1973))) | (~(((self.net_1351) & (self.net_1505)) | (self.net_1365)))) & (~(~(self.net_1351) & (self.net_1363))))),
            self.net_2240.eq(0),
            self.net_2189.eq((((self.net_1363) | (self._net_1992)) & (~((self.net_1351) & (self._net_1992))) & (~(((self.net_1363) | (self.net_1365)) & (self.net_1505))))),
            self.net_2461.eq(~(((self.net_1351) & (self._net_2303)) | (self.net_1505))),
            self.net_2154.eq((((self.net_1363) | (~((self.net_1351) & (self._net_1992)))) & (~(((self.net_1363) | (self.net_1365)) & (self.net_1505))))),
            self.net_2479.eq(0),
            self.net_2004.eq(0),
        ]

        return m

class Output_LakeVerity(wiring.Component):
    net_1363: In(1)
    net_1365: In(1)
    net_1351: In(1)
    net_1505: In(1)
    net_1927: Out(1)
    net_1816: Out(1)
    net_1936: Out(1)
    net_1905: Out(1)
    net_1815: Out(1)
    net_1928: Out(1)
    net_1907: Out(1)
    net_1822: Out(1)

    def __init__(self):
        self._net_1827 = Signal(1)
        self._net_1880 = Signal(1)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._net_1827.eq(~((self.net_1351) | (self.net_1363) | (self.net_1365) | ~(self.net_1505))),
            self._net_1880.eq(~(self.net_1505) & (self.net_1365) & (self.net_1363) & (self.net_1351)),
        ]

        m.d.sync += [
        ]

        m.d.comb += [
            self.net_1927.eq(~(((self.net_1351) & (self.net_1363)) | (self.net_1365) | (self.net_1505))),
            self.net_1816.eq((((self.net_1363) | (self.net_1365)) & ((~(((self.net_1351) & (self.net_1363)) | (self.net_1505))) | (self._net_1880)))),
            self.net_1936.eq((((self.net_1363) & (~(((self.net_1351) & (self.net_1363)) | (self.net_1365) | (self.net_1505)))) | (self._net_1827) | (self._net_1880))),
            self.net_1905.eq(~(self.net_1365) & ~(self.net_1505) & (self.net_1351) & (self.net_1363)),
            self.net_1815.eq(0),
            self.net_1928.eq((~(((self.net_1351) & (self.net_1363)) | (self.net_1505))) | (self._net_1880) | (self._net_1827)),
            self.net_1907.eq((((self.net_1351) & (self.net_1365) & (~((self.net_1363) | (self.net_1505)))) | (~((self.net_1351) | (self.net_1363) | (self.net_1365))))),
            self.net_1822.eq((((self.net_1351) & (~((self.net_1363) | (self.net_1505)))) | (self._net_1827))),
        ]

        return m

class Output_LakeValor(wiring.Component):
    net_1365: In(1)
    net_1351: In(1)
    net_1505: In(1)
    net_1363: In(1)
    net_1447: In(1)
    net_1425: Out(1)
    net_1693: Out(1)
    net_1694: Out(1)
    net_1516: Out(1)
    net_1420: Out(1)
    net_1559: Out(1)
    net_1629: Out(1)
    net_1472: Out(1)

    def __init__(self):
        self._net_1598 = Signal(1)
        self._net_1469 = Signal(1)
        self._net_1445 = Signal(1)
        self._net_1448 = Signal(1)
        self._net_1443 = Signal(1)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._net_1598.eq(~((self.net_1351) & (self.net_1363))),
            self._net_1469.eq(~((self.net_1351) | (self.net_1363))),
            self._net_1445.eq(~(((self.net_1351) & (self.net_1363)) | (self.net_1505))),
            self._net_1448.eq(~(~(self.net_1365) & (self.net_1505))),
            self._net_1443.eq(~(~(self.net_1351) & (self.net_1365))),
        ]

        m.d.sync += [
        ]

        m.d.comb += [
            self.net_1425.eq(0),
            self.net_1693.eq(~((self.net_1505) | (self._net_1598))),
            self.net_1694.eq((self._net_1598) & (~((self.net_1365) & (self.net_1505)))),
            self.net_1516.eq(~((~(self._net_1469) & (self._net_1443) & (self._net_1445)) ^ ((((self._net_1443) & (~(~(self.net_1365) & (self.net_1351)))) | (self.net_1363))))),
            self.net_1420.eq((((~(self.net_1363) & (self.net_1365)) | (~(((self.net_1447) & (self._net_1448) & (~(~(self.net_1505) & (self.net_1365)))) | (self._net_1445))) | (~((self.net_1365) | (self._net_1469) | ((self.net_1351) & (self.net_1363))))) & ((((self.net_1447) & (self._net_1448) & (~(~(self.net_1505) & (self.net_1365)))) | (~(self.net_1365) & (self.net_1351)) | (self._net_1445))))),
            self.net_1559.eq(~(((self._net_1469) | (self._net_1448)) & ~(~(self._net_1469) & (self._net_1443) & (self._net_1445)))),
            self.net_1629.eq((((self.net_1505) | (self._net_1598)) & ((~((self.net_1365) & (self.net_1505))) | (self._net_1469)))),
            self.net_1472.eq(~(((~(self.net_1363) & (self.net_1365)) | (~(((self.net_1447) & (self._net_1448) & (~(~(self.net_1505) & (self.net_1365)))) | (self._net_1445))) | ((self.net_1363) & (self._net_1443))) & ((self._net_1448) | (self.net_1351)))),
        ]

        return m

class Sunyshore(wiring.Component):
    net_435: In(1)
    net_380: In(1)
    net_323: In(1)
    net_378: In(1)
    net_377: In(1)
    net_832: In(1)
    net_20: In(1)
    net_319: In(1)
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
            self._net_561.eq(((((((self._net_270) & (~((self._net_659) & (self._net_565)))) | (~((self._net_659) | (self._net_565))))) & (~((~(((~(~(self._net_606) & ((self.net_378) ^ (self._net_510)))) & (~((self.net_832) & (~((self._net_606) ^ ((self.net_378) ^ (self._net_510))))))) | ((~((self.net_377) | (self._net_523))) | (self._net_574) | ((~((self.net_323) & (self.net_435))) & (self._net_523) & (~((self.net_377) ^ (self.net_378))))))) | ((~(~(self._net_606) & ((self.net_378) ^ (self._net_510)))) & (~((self.net_832) & (~((self._net_606) ^ ((self.net_378) ^ (self._net_510)))))) & ((~((self.net_377) | (self._net_523))) | (self._net_574) | ((~((self.net_323) & (self.net_435))) & (self._net_523) & (~((self.net_377) ^ (self.net_378))))))))) | (~(((~(~(self._net_606) & ((self.net_378) ^ (self._net_510)))) & (~((self.net_832) & (~((self._net_606) ^ ((self.net_378) ^ (self._net_510))))))) | ((~((self.net_377) | (self._net_523))) | (self._net_574) | ((~((self.net_323) & (self.net_435))) & (self._net_523) & (~((self.net_377) ^ (self.net_378))))))))),
            self._net_40.eq(~((self._net_25) | (self._net_179))),
            self._net_102.eq(~((self._net_561) ^ (~(~(self.net_323) & ~(self.net_377) & (self.net_435) & (self.net_378)) & (~(((self.net_377) | (self._net_523)) & ((~(((self.net_377) & (self.net_378)) | (self.net_435))) | ((((self.net_377) & (self.net_435) & (self.net_378)) | (self._net_574))))))))),
            self._net_39.eq(((((self._net_270) & (~((self._net_659) & (self._net_565)))) | (~((self._net_659) | (self._net_565))))) ^ (~((~(((~(~(self._net_606) & ((self.net_378) ^ (self._net_510)))) & (~((self.net_832) & (~((self._net_606) ^ ((self.net_378) ^ (self._net_510))))))) | ((~((self.net_377) | (self._net_523))) | (self._net_574) | ((~((self.net_323) & (self.net_435))) & (self._net_523) & (~((self.net_377) ^ (self.net_378))))))) | ((~(~(self._net_606) & ((self.net_378) ^ (self._net_510)))) & (~((self.net_832) & (~((self._net_606) ^ ((self.net_378) ^ (self._net_510)))))) & ((~((self.net_377) | (self._net_523))) | (self._net_574) | ((~((self.net_323) & (self.net_435))) & (self._net_523) & (~((self.net_377) ^ (self.net_378))))))))),
            self._net_494.eq((self._net_25) & (self._net_53) & (self._net_59)),
            self._net_270.eq((((self.net_20) & (self._net_51) & ((self.net_380) ^ (~(((self.net_377) & (self._net_510)) | (~((self.net_377) | (self.net_435))))))) | ((self._net_58) & (self._net_151)))),
            self._net_510.eq((self.net_323) ^ (self.net_435)),
            self._net_574.eq(~((~((self.net_323) & (self.net_435))) | (~((self.net_377) ^ (self.net_378))))),
            self._net_523.eq(~((self.net_378) & (self._net_510))),
            self._net_56.eq(~((self._net_240) | (~((self._net_145) & (~((self.net_319) & (self.net_323))))))),
            self._net_536.eq((self._net_561) ^ (~(~(self.net_323) & ~(self.net_377) & (self.net_435) & (self.net_378)) & (~(((self.net_377) | (self._net_523)) & ((~(((self.net_377) & (self.net_378)) | (self.net_435))) | ((((self.net_377) & (self.net_435) & (self.net_378)) | (self._net_574)))))))),
            self._net_15.eq(~((self._net_53) & (self._net_14))),
            self._net_704.eq((self._net_772) ^ (self._net_773)),
            self._net_775.eq(~((~((self._net_772) | (self._net_773))) | ((((self.net_323) | (self.net_377)) & (self.net_435) & (self.net_378))))),
            self._net_823.eq(~((self._net_772) ^ (self._net_773))),
            self._net_565.eq((~((self.net_380) & (~(((self.net_377) & (self._net_510)) | (~((self.net_377) | (self.net_435)))))) & ((~((self.net_323) & (self.net_377))) | (self.net_435)))),
            self._net_659.eq(~((self.net_832) ^ (~((self._net_606) ^ ((self.net_378) ^ (self._net_510)))))),
            self._net_773.eq((((self._net_606) & (self._net_574)) | (~(((self.net_378) & (self._net_606)) | (self._net_574))))),
            self._net_772.eq(~(((self._net_561) & (~(((self.net_377) | (self._net_523)) & ((~(((self.net_377) & (self.net_378)) | (self.net_435))) | ((((self.net_377) & (self.net_435) & (self.net_378)) | (self._net_574))))))) | (~(self.net_323) & ~(self.net_377) & (self.net_435) & (self.net_378)))),
            self._net_45.eq((self._net_99) | (self._net_38)),
            self._net_606.eq(~((self.net_377) & (self.net_435))),
            self._net_21.eq(~((self._net_122) & (self._net_53))),
            self._net_151.eq(~((self._net_145) | (~((self.net_319) & (self.net_323))))),
            self._net_58.eq(~((~((self.net_20) & (self._net_51))) ^ ((self.net_380) ^ (~(((self.net_377) & (self._net_510)) | (~((self.net_377) | (self.net_435)))))))),
            self._net_17.eq((self._net_25) | (self._net_45)),
            self._net_99.eq((self._net_58) ^ (self._net_151)),
            self._net_42.eq(~((self._net_145) | (self._net_122))),
            self._net_16.eq((self._net_99) | (self._net_14)),
            self._net_61.eq((self._net_42) | (self._net_53) | (self._net_14)),
            self._net_14.eq(~((~(((self.net_319) & (self.net_323)) | (self._net_240))) | (self._net_38))),
            self._net_137.eq(~((self._net_53) | (self._net_56))),
            self._net_53.eq(~((self._net_58) ^ (self._net_151))),
            self._net_59.eq((self._net_122) & (self._net_38)),
            self._net_51.eq((self.net_323) ^ (self.net_377)),
            self._net_38.eq(~(self._net_151) & (~((self._net_145) & (~((self.net_319) & (self.net_323)))))),
            self._net_240.eq(~((self.net_319) | (self.net_323))),
            self._net_145.eq(~((self.net_20) ^ (self._net_51))),
            self._net_122.eq(((self.net_319) & (self.net_323)) | (self._net_240)),
        ]

        m.d.sync += [
        ]

        m.d.comb += [
            self.net_736.eq(((((((~((self._net_109) | (self._net_25))) | (self._net_39) | (self._net_494)) & (self._net_102) & (~((self._net_39) & (Mux((self._net_23), ((self._net_42) | (self._net_14) | (self._net_137)), (self._net_61))))))) | ((((self._net_536) & ((((self._net_53) & ((self._net_25) | (self._net_14))) | (~(~(((self._net_23) & (self._net_179)) | (self._net_39)))))) & (~((self._net_39) & (~(((self._net_42) | (self._net_23) | (self._net_99)) & (self._net_109)))))) | (self._net_704)))) & (self._net_775) & ((self._net_823) | ((((~((self._net_39) & (self._net_43))) | (self._net_40)) & (self._net_102) & ((self._net_39) | (~((self._net_23) | (self._net_103))) | (~((self._net_23) | (self._net_45)))))) | (~(((~((self._net_39) & (self._net_43))) & ((self._net_39) | (self._net_40) | ((((self._net_42) | (self._net_99)) & (self._net_25) & (self._net_109))))) | (self._net_102)))))),
            self.net_1034.eq((((self._net_704) | (Mux((self._net_536), (Mux((self._net_39), ((((self._net_23) & (self._net_103) & (self._net_21)) | (self._net_59))), ((((self._net_42) | (self._net_43)) & ((self._net_25) | (self._net_14)))))), ((((self._net_39) | (self._net_494) | (~((self._net_25) | (self._net_61)))) & ((~((self._net_179) | (self._net_43))) | (~(((self._net_25) | (self._net_137) | (~(self._net_16))) & (self._net_39))))))))) & ((((self._net_536) & ((((self._net_39) & (self._net_43) & (self._net_17)) | (((((self._net_23) | (~(~(self._net_59) & (self._net_45)))) & ((self._net_17) | (~(((self.net_319) & (self.net_323)) | (self._net_240)))))) & (~(((self._net_23) & (self._net_179)) | (self._net_39))))))) | ((((self._net_137) | (~(((self._net_23) | (~(self._net_16))) & (self._net_39)))) & (((((self._net_23) | ((self._net_103) & (self._net_21))) & (self._net_17))) | (self._net_39)) & (self._net_102))) | (self._net_823))) & (self._net_775))),
            self.net_857.eq((((self._net_704) | ((((self._net_536) & ((((self._net_39) & (~((self._net_109) | (self._net_23)))) | (~((((self._net_25) & (~((self._net_58) & (self._net_56)))) | ((((self._net_42) | (self._net_16)) & (self._net_23))) | (self._net_39))))))) | ((self._net_102) & ((((self._net_58) & (self._net_39) & (self._net_38)) | (self._net_40) | ((self._net_25) & (~(self._net_56)) & (self._net_21)))) & (~(((self._net_40) | ((self._net_25) & (~(self._net_56)) & (self._net_21))) & (self._net_39))))))) & (~(((self._net_536) | (Mux((self._net_39), ((((self._net_15) & (self._net_40)) | ((self._net_16) & (self._net_25)))), ((~((self._net_23) | (self._net_45))) | ((((self._net_23) | (self._net_56)) & (self._net_45))))))) & ((((self._net_39) & (self._net_45)) | (Mux((~(~(self._net_59) & (self._net_45))), (self._net_25), (self._net_40))) | (self._net_102))) & (self._net_704))) & (self._net_775))),
            self.net_985.eq((((self._net_704) | (~(((self._net_536) | ((((self._net_39) | (self._net_494) | (~(((self._net_25) & (self._net_59)) | (self._net_61)))) & ((~(((self._net_25) | (self._net_137) | (~(self._net_16))) & (self._net_39))) | (~((self._net_23) | (self._net_179))))))) & ((self._net_39) | (self._net_102) | ((self._net_42) | (self._net_14) | (self._net_137)) | ((((self._net_42) | (self._net_16)) & (self._net_23))))))) & ((((self._net_39) & (~(((self._net_25) | (self._net_15)) & (((self._net_42) | (self._net_23) | (self._net_16)) | (self._net_536))))) | (((self._net_536) | (~((self._net_23) | (self._net_103)))) & (~(((self._net_536) & ((((self._net_25) | (~((self._net_58) & (self._net_56)))) & ~(~((self._net_109) | (self._net_23)))))) | (self._net_39)))) | (self._net_823))) & (self._net_775))),
        ]

        return m

class puzzle(wiring.Component):
    I: In(1)
    enable: In(1)
    net_1447: In(1)
    O_0_: Out(1)
    O_1_: Out(1)
    O_2_: Out(1)
    O_3_: Out(1)
    O_4_: Out(1)
    O_5_: Out(1)
    O_6_: Out(1)
    O_7_: Out(1)
    success: Out(1)

    def elaborate(self, platform):
        m = Module()

        m.submodules.floaroma = Floaroma()
        m.submodules.jubilife = Jubilife()
        m.submodules.twinleaf = Twinleaf()
        m.submodules.snowpoint = Snowpoint()
        m.submodules.eterna = Eterna()
        m.submodules.oreburgh = Oreburgh()
        m.submodules.sandgem = Sandgem()
        m.submodules.celestic = Celestic()
        m.submodules.hearthome = Hearthome()
        m.submodules.solaceon = Solaceon()
        m.submodules.pastoria = Pastoria()
        m.submodules.veilstone = Veilstone()
        m.submodules.output_mtcoronet = Output_MtCoronet()
        m.submodules.output_eternaforest = Output_EternaForest()
        m.submodules.output_lakeacuity = Output_LakeAcuity()
        m.submodules.output_lakeverity = Output_LakeVerity()
        m.submodules.output_lakevalor = Output_LakeValor()
        m.submodules.sunyshore = Sunyshore()

        m.d.comb += [
            m.submodules.floaroma.net_1508.eq(m.submodules.twinleaf.net_1508),
            m.submodules.floaroma.net_1526.eq(m.submodules.jubilife.net_1526),
            m.submodules.floaroma.enable.eq(self.enable),
            m.submodules.jubilife.net_934.eq(m.submodules.floaroma.net_934),
            m.submodules.twinleaf.net_934.eq(m.submodules.floaroma.net_934),
            m.submodules.twinleaf.net_1526.eq(m.submodules.jubilife.net_1526),
            m.submodules.snowpoint.net_934.eq(m.submodules.floaroma.net_934),
            m.submodules.snowpoint.net_1723.eq(m.submodules.eterna.net_1723),
            m.submodules.snowpoint.net_1719.eq(m.submodules.eterna.net_1719),
            m.submodules.snowpoint.I.eq(self.I),
            m.submodules.snowpoint.net_2480.eq(m.submodules.hearthome.net_2480),
            m.submodules.snowpoint.net_2475.eq(m.submodules.hearthome.net_2475),
            m.submodules.snowpoint.net_2416.eq(m.submodules.solaceon.net_2416),
            m.submodules.snowpoint.net_3283.eq(m.submodules.hearthome.net_3283),
            m.submodules.snowpoint.net_2474.eq(m.submodules.hearthome.net_2474),
            m.submodules.snowpoint.net_2471.eq(m.submodules.hearthome.net_2471),
            m.submodules.snowpoint.net_2393.eq(m.submodules.hearthome.net_2393),
            m.submodules.snowpoint.net_3830.eq(m.submodules.hearthome.net_3830),
            m.submodules.snowpoint.net_1628.eq(m.submodules.eterna.net_1628),
            m.submodules.snowpoint.net_1738.eq(m.submodules.eterna.net_1738),
            m.submodules.snowpoint.net_2386.eq(m.submodules.celestic.net_2386),
            m.submodules.snowpoint.net_2463.eq(m.submodules.celestic.net_2463),
            m.submodules.snowpoint.net_2459.eq(m.submodules.celestic.net_2459),
            m.submodules.eterna.net_1526.eq(m.submodules.jubilife.net_1526),
            m.submodules.eterna.net_934.eq(m.submodules.floaroma.net_934),
            m.submodules.eterna.net_832.eq(m.submodules.jubilife.net_832),
            m.submodules.eterna.net_20.eq(m.submodules.jubilife.net_20),
            m.submodules.eterna.net_380.eq(m.submodules.jubilife.net_380),
            m.submodules.eterna.net_319.eq(m.submodules.jubilife.net_319),
            m.submodules.eterna.I.eq(self.I),
            m.submodules.oreburgh.net_934.eq(m.submodules.floaroma.net_934),
            m.submodules.oreburgh.I.eq(self.I),
            m.submodules.sandgem.net_204.eq(m.submodules.pastoria.net_204),
            m.submodules.sandgem.net_203.eq(m.submodules.pastoria.net_203),
            m.submodules.sandgem.net_294.eq(m.submodules.pastoria.net_294),
            m.submodules.sandgem.net_226.eq(m.submodules.pastoria.net_226),
            m.submodules.sandgem.net_545.eq(m.submodules.pastoria.net_545),
            m.submodules.sandgem.net_1185.eq(m.submodules.pastoria.net_1185),
            m.submodules.sandgem.net_341.eq(m.submodules.pastoria.net_341),
            m.submodules.sandgem.net_401.eq(m.submodules.pastoria.net_401),
            m.submodules.sandgem.net_399.eq(m.submodules.pastoria.net_399),
            m.submodules.sandgem.net_405.eq(m.submodules.pastoria.net_405),
            m.submodules.sandgem.net_349.eq(m.submodules.pastoria.net_349),
            m.submodules.celestic.net_934.eq(m.submodules.floaroma.net_934),
            m.submodules.celestic.I.eq(self.I),
            m.submodules.celestic.net_319.eq(m.submodules.jubilife.net_319),
            m.submodules.celestic.net_832.eq(m.submodules.jubilife.net_832),
            m.submodules.celestic.net_20.eq(m.submodules.jubilife.net_20),
            m.submodules.celestic.net_380.eq(m.submodules.jubilife.net_380),
            m.submodules.hearthome.net_934.eq(m.submodules.floaroma.net_934),
            m.submodules.hearthome.I.eq(self.I),
            m.submodules.hearthome.net_20.eq(m.submodules.jubilife.net_20),
            m.submodules.hearthome.net_319.eq(m.submodules.jubilife.net_319),
            m.submodules.hearthome.net_380.eq(m.submodules.jubilife.net_380),
            m.submodules.hearthome.net_832.eq(m.submodules.jubilife.net_832),
            m.submodules.solaceon.net_934.eq(m.submodules.floaroma.net_934),
            m.submodules.solaceon.I.eq(self.I),
            m.submodules.solaceon.net_20.eq(m.submodules.jubilife.net_20),
            m.submodules.solaceon.net_319.eq(m.submodules.jubilife.net_319),
            m.submodules.solaceon.net_832.eq(m.submodules.jubilife.net_832),
            m.submodules.solaceon.net_380.eq(m.submodules.jubilife.net_380),
            m.submodules.pastoria.net_934.eq(m.submodules.floaroma.net_934),
            m.submodules.pastoria.I.eq(self.I),
            m.submodules.pastoria.net_736.eq(m.submodules.sunyshore.net_736),
            m.submodules.pastoria.net_1034.eq(m.submodules.sunyshore.net_1034),
            m.submodules.pastoria.net_857.eq(m.submodules.sunyshore.net_857),
            m.submodules.pastoria.net_985.eq(m.submodules.sunyshore.net_985),
            m.submodules.veilstone.net_2259.eq(m.submodules.snowpoint.net_2259),
            m.submodules.veilstone.net_3136.eq(m.submodules.floaroma.net_3136),
            m.submodules.veilstone.net_2505.eq(m.submodules.snowpoint.net_2505),
            m.submodules.veilstone.net_343.eq(m.submodules.sandgem.net_343),
            m.submodules.veilstone.net_1557.eq(m.submodules.eterna.net_1557),
            m.submodules.veilstone.net_719.eq(m.submodules.oreburgh.net_719),
            m.submodules.output_mtcoronet.net_3771.eq(m.submodules.veilstone.net_3771),
            m.submodules.output_mtcoronet.net_3920.eq(m.submodules.veilstone.net_3920),
            m.submodules.output_mtcoronet.net_1084.eq(m.submodules.oreburgh.net_1084),
            m.submodules.output_mtcoronet.net_791.eq(m.submodules.oreburgh.net_791),
            m.submodules.output_mtcoronet.net_3617.eq(m.submodules.output_eternaforest.net_3617),
            m.submodules.output_mtcoronet.net_3516.eq(m.submodules.output_eternaforest.net_3516),
            m.submodules.output_mtcoronet.net_3435.eq(m.submodules.output_eternaforest.net_3435),
            m.submodules.output_mtcoronet.net_3543.eq(m.submodules.output_eternaforest.net_3543),
            m.submodules.output_mtcoronet.net_3552.eq(m.submodules.output_eternaforest.net_3552),
            m.submodules.output_mtcoronet.net_3613.eq(m.submodules.output_eternaforest.net_3613),
            m.submodules.output_mtcoronet.success.eq(m.submodules.veilstone.success),
            m.submodules.output_mtcoronet.net_3518.eq(m.submodules.output_eternaforest.net_3518),
            m.submodules.output_mtcoronet.net_3818.eq(m.submodules.output_eternaforest.net_3818),
            m.submodules.output_eternaforest.net_1351.eq(m.submodules.output_mtcoronet.net_1351),
            m.submodules.output_eternaforest.net_1365.eq(m.submodules.output_mtcoronet.net_1365),
            m.submodules.output_eternaforest.net_2232.eq(m.submodules.output_lakeacuity.net_2232),
            m.submodules.output_eternaforest.net_2006.eq(m.submodules.output_lakeacuity.net_2006),
            m.submodules.output_eternaforest.net_1425.eq(m.submodules.output_lakevalor.net_1425),
            m.submodules.output_eternaforest.net_1693.eq(m.submodules.output_lakevalor.net_1693),
            m.submodules.output_eternaforest.net_1694.eq(m.submodules.output_lakevalor.net_1694),
            m.submodules.output_eternaforest.net_1516.eq(m.submodules.output_lakevalor.net_1516),
            m.submodules.output_eternaforest.net_2313.eq(m.submodules.output_lakeacuity.net_2313),
            m.submodules.output_eternaforest.net_1977.eq(m.submodules.output_lakeacuity.net_1977),
            m.submodules.output_eternaforest.net_1927.eq(m.submodules.output_lakeverity.net_1927),
            m.submodules.output_eternaforest.net_2315.eq(m.submodules.output_lakeacuity.net_2315),
            m.submodules.output_eternaforest.net_2088.eq(m.submodules.output_lakeacuity.net_2088),
            m.submodules.output_eternaforest.net_2298.eq(m.submodules.output_lakeacuity.net_2298),
            m.submodules.output_eternaforest.net_2120.eq(m.submodules.output_lakeacuity.net_2120),
            m.submodules.output_eternaforest.net_2460.eq(m.submodules.output_lakeacuity.net_2460),
            m.submodules.output_eternaforest.net_2117.eq(m.submodules.output_lakeacuity.net_2117),
            m.submodules.output_eternaforest.net_2240.eq(m.submodules.output_lakeacuity.net_2240),
            m.submodules.output_eternaforest.net_2189.eq(m.submodules.output_lakeacuity.net_2189),
            m.submodules.output_eternaforest.net_1420.eq(m.submodules.output_lakevalor.net_1420),
            m.submodules.output_eternaforest.net_3037.eq(m.submodules.output_mtcoronet.net_3037),
            m.submodules.output_eternaforest.net_934.eq(m.submodules.floaroma.net_934),
            m.submodules.output_eternaforest.net_3419.eq(m.submodules.output_mtcoronet.net_3419),
            m.submodules.output_eternaforest.net_3420.eq(m.submodules.output_mtcoronet.net_3420),
            m.submodules.output_eternaforest.net_3384.eq(m.submodules.output_mtcoronet.net_3384),
            m.submodules.output_eternaforest.net_1559.eq(m.submodules.output_lakevalor.net_1559),
            m.submodules.output_eternaforest.net_1816.eq(m.submodules.output_lakeverity.net_1816),
            m.submodules.output_eternaforest.net_1936.eq(m.submodules.output_lakeverity.net_1936),
            m.submodules.output_eternaforest.net_1629.eq(m.submodules.output_lakevalor.net_1629),
            m.submodules.output_eternaforest.net_1472.eq(m.submodules.output_lakevalor.net_1472),
            m.submodules.output_eternaforest.net_2461.eq(m.submodules.output_lakeacuity.net_2461),
            m.submodules.output_eternaforest.net_2154.eq(m.submodules.output_lakeacuity.net_2154),
            m.submodules.output_eternaforest.net_1905.eq(m.submodules.output_lakeverity.net_1905),
            m.submodules.output_eternaforest.net_1815.eq(m.submodules.output_lakeverity.net_1815),
            m.submodules.output_eternaforest.net_1928.eq(m.submodules.output_lakeverity.net_1928),
            m.submodules.output_eternaforest.net_2479.eq(m.submodules.output_lakeacuity.net_2479),
            m.submodules.output_eternaforest.net_2004.eq(m.submodules.output_lakeacuity.net_2004),
            m.submodules.output_eternaforest.net_1907.eq(m.submodules.output_lakeverity.net_1907),
            m.submodules.output_eternaforest.net_1822.eq(m.submodules.output_lakeverity.net_1822),
            m.submodules.output_eternaforest.net_1505.eq(m.submodules.output_mtcoronet.net_1505),
            m.submodules.output_eternaforest.I.eq(self.I),
            m.submodules.output_eternaforest.net_1363.eq(m.submodules.output_mtcoronet.net_1363),
            m.submodules.output_lakeacuity.net_1351.eq(m.submodules.output_mtcoronet.net_1351),
            m.submodules.output_lakeacuity.net_1505.eq(m.submodules.output_mtcoronet.net_1505),
            m.submodules.output_lakeacuity.net_1365.eq(m.submodules.output_mtcoronet.net_1365),
            m.submodules.output_lakeacuity.net_1363.eq(m.submodules.output_mtcoronet.net_1363),
            m.submodules.output_lakeverity.net_1363.eq(m.submodules.output_mtcoronet.net_1363),
            m.submodules.output_lakeverity.net_1365.eq(m.submodules.output_mtcoronet.net_1365),
            m.submodules.output_lakeverity.net_1351.eq(m.submodules.output_mtcoronet.net_1351),
            m.submodules.output_lakeverity.net_1505.eq(m.submodules.output_mtcoronet.net_1505),
            m.submodules.output_lakevalor.net_1365.eq(m.submodules.output_mtcoronet.net_1365),
            m.submodules.output_lakevalor.net_1351.eq(m.submodules.output_mtcoronet.net_1351),
            m.submodules.output_lakevalor.net_1505.eq(m.submodules.output_mtcoronet.net_1505),
            m.submodules.output_lakevalor.net_1363.eq(m.submodules.output_mtcoronet.net_1363),
            m.submodules.output_lakevalor.net_1447.eq(self.net_1447),
            m.submodules.sunyshore.net_435.eq(m.submodules.twinleaf.net_435),
            m.submodules.sunyshore.net_380.eq(m.submodules.jubilife.net_380),
            m.submodules.sunyshore.net_323.eq(m.submodules.twinleaf.net_323),
            m.submodules.sunyshore.net_378.eq(m.submodules.twinleaf.net_378),
            m.submodules.sunyshore.net_377.eq(m.submodules.twinleaf.net_377),
            m.submodules.sunyshore.net_832.eq(m.submodules.jubilife.net_832),
            m.submodules.sunyshore.net_20.eq(m.submodules.jubilife.net_20),
            m.submodules.sunyshore.net_319.eq(m.submodules.jubilife.net_319),
        ]

        m.d.comb += [
            self.O_0_.eq(m.submodules.output_mtcoronet.O_0_),
            self.O_1_.eq(m.submodules.output_mtcoronet.O_1_),
            self.O_2_.eq(m.submodules.output_mtcoronet.O_2_),
            self.O_3_.eq(m.submodules.output_mtcoronet.O_3_),
            self.O_4_.eq(m.submodules.output_mtcoronet.O_4_),
            self.O_5_.eq(m.submodules.output_mtcoronet.O_5_),
            self.O_6_.eq(m.submodules.output_mtcoronet.O_6_),
            self.O_7_.eq(m.submodules.output_mtcoronet.O_7_),
            self.success.eq(m.submodules.veilstone.success),
        ]

        return m

if __name__ == "__main__":
    from amaranth.back import verilog
    top = puzzle()
    with open(argv[1], "wt") as f:
        f.write(verilog.convert(top, name="puzzle_solution", ports=[top.I, top.enable, top.net_1447, top.O_0_, top.O_1_, top.O_2_, top.O_3_, top.O_4_, top.O_5_, top.O_6_, top.O_7_, top.success]))
