from enum import Enum
from faulthandler import enable
from itertools import chain
from sys import argv

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out


def Buf(expr):
    return expr

class DoneController(wiring.Component):
    y_overflow: In(1)
    x_overflow: In(1)
    enable: In(1)
    enable_gated: Out(1)
    done: Out(1, init=0)

    def elaborate(self, platform):
        m = Module()

        with m.If(self.enable & self.x_overflow & self.y_overflow):
            m.d.sync += [
                self.done.eq(1),
            ]

        m.d.comb += [
            self.enable_gated.eq(self.enable & ~self.done),
        ]

        return m

class Counter11(wiring.Component):
    enable: In(1)
    increment: In(1)
    count: Out(4, init=0)
    overflow: Out(1)

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.overflow.eq(self.count == 10)

        with m.If(self.enable & self.increment):
            with m.If(self.overflow):
                m.d.sync += self.count.eq(0)
            with m.Else():
                m.d.sync += self.count.eq(self.count + 1)

        return m

class EdgeChecker(wiring.Component):
    """
    Check if certain neighbours of the current pixel exist

    It seems like at some point, it was meant to check for a top edge too, but
    this was removed because at the top row, the shift register is reset to 0
    anyway, rendering the top check useless.

    Presumably to avoid this optimization changing the interface, a buffer is
    inserted to make the two output nets separate. I'm assuming this is a
    special feature for this puzzle, but it might be a thing to aid LVS (layout
    versus schematic) checking.

    This has also resulted in one of the constants
    """
    x: In(description=4)
    top_left_available: Out(1)
    top_available: Out(1)
    top_right_available: Out(1)
    left_available: Out(1)

    def __init__(self):
        self._left = Signal(1)
        self._top = Signal(1)
        self._right = Signal(1)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self._left.eq(self.x == 0),
            # self._top.eq(self.y == 0),
            self._top.eq(0),
            self._right.eq(self.x == 10),

            self.top_left_available.eq(~self._top & ~self._left),
            self.top_available.eq(~self._top),
            self.top_right_available.eq(~self._top & ~self._right),
            self.left_available.eq(~self._left),
        ]

        return m

class AdjacencyChecker(wiring.Component):
    """No two adjacent pixels can be set (Moore neighbourhood)"""
    enable: In(1)
    I: In(1)
    top_left_available: In(1)
    top_available: In(1)
    top_right_available: In(1)
    left_available: In(1)
    result: Out(1, init=1)

    def __init__(self):
        self._failed = Signal(1, init=0)
        self._sr = Signal(12, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()


        with m.If(self.enable):
            m.d.sync += self._sr.eq(Cat(self.I, self._sr[:11]))

            with m.If(self.I & (self.top_left_available & self._sr[11] | self.top_available & self._sr[10] | self.top_right_available & self._sr[9] | self.left_available & self._sr[0])):
                m.d.sync += self.result.eq(0)

        return m

class RowChecker(wiring.Component):
    """Every line has exactly 2 bits set"""
    enable: In(1)
    I: In(1)
    x_overflow: In(1)
    result: Out(1, init=1)

    def __init__(self):
        self._counter = Signal(2, init=0)
        self._counter_next = Signal(2)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        with m.If(self._counter == 3):
            m.d.comb += self._counter_next.eq(3)
        with m.Else():
            m.d.comb += self._counter_next.eq(self._counter + self.I)

        with m.If(self.enable):
            m.d.sync += self._counter.eq(self._counter_next)
            with m.If(self.x_overflow):
                m.d.sync += self._counter.eq(0)
                with m.If(self._counter_next != 2):
                    m.d.sync += self.result.eq(0)

        return m

class PopCntChecker(wiring.Component):
    """
    Asserts that there are exactly 22 bits set
    
    This is redundan with the row, column, and region properties.

    Also triggers an easter egg when empty or full grids are supplied
    """
    enable: In(1)
    I: In(1)
    result: Out(1)
    full: Out(1)
    empty: Out(1)

    def __init__(self):
        self._counter = Signal(8, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.enable & self.I):
            m.d.sync += self._counter.eq(self._counter + 1)

        m.d.comb += [
            self.result.eq(self._counter == 22),
            self.full.eq(self._counter == 121),
            self.empty.eq(self._counter == 0),
        ]

        return m


class SingleColumnChecker(wiring.Component):
    enable: In(1)
    I: In(1)
    x: In(4)
    result: Out(1)

    def __init__(self, column: int):
        self._column = column
        self._counter = Signal(2, init=0)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        with m.If((self.x == self._column) & self.I & self.enable & (self._counter != 3)):
            m.d.sync += self._counter.eq(self._counter + 1)

        m.d.comb += self.result.eq(self._counter == 2)

        return m

class ColumnChecker(wiring.Component):
    enable: In(1)
    I: In(1)
    x: In(4)
    results: Out(11)
    result: Out(1)

    def elaborate(self, platform):
        m = Module()

        for column in range(11):
            column_checker = SingleColumnChecker(column)
            m.submodules[f"column_{column}"] = column_checker
            m.d.comb += [
                column_checker.enable.eq(self.enable),
                column_checker.I.eq(self.I),
                column_checker.x.eq(self.x),
                self.results[column].eq(column_checker.result),
            ]

        m.d.comb += self.result.eq(self.results.all())

        return m

class SuccessController(wiring.Component):
    done: In(1)
    adjacency_property: In(1)
    column_property: In(1)
    region_property: In(1)
    row_property: In(1)
    popcnt_property: In(1)

    done_delayed: Out(1, init=0)
    almost_success: Out(1, init=0)
    success: Out(1, init=0)

    def elaborate(self, platform):
        m = Module()

        with m.If(self.done):
            m.d.sync += self.done_delayed.eq(1)

        with m.If(self.done & ~self.done_delayed):
            m.d.sync += [
                self.success.eq(self.adjacency_property & self.row_property & self.popcnt_property & self.region_property & self.column_property),
                self.almost_success.eq(~self.adjacency_property & self.row_property & self.popcnt_property & self.region_property & self.column_property),
            ]

        return m

class MessageSelect(Enum):
    EMPTY_SKY = 0
    BIG_BANG = 1
    FLAG = 2
    TRY_AGAIN = 3
    TWO_NOT_TOUCH = 4

class OutputController(wiring.Component):
    done_delayed: In(1)
    egg_almost_success: In(1)
    egg_full: In(1)
    egg_empty: In(1)
    success: In(1)
    I: In(8)
    output_enable: Out(1)
    message_select: Out(MessageSelect)
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
        ]

        # Which order these are in is completely irrelevant, as the incoming
        # signals are guaranteed to be one-hot-or-zero encoded. Still, I try to
        # be faithful to the operation of each module!
        # However, this order does make the bit order make a bit more sense.
        with m.If(self.egg_empty):
            m.d.comb += self.message_select.eq(MessageSelect.EMPTY_SKY)
        with m.Elif(self.egg_full):
            m.d.comb += self.message_select.eq(MessageSelect.BIG_BANG)
        with m.Elif(self.success):
            m.d.comb += self.message_select.eq(MessageSelect.FLAG)
        with m.Elif(self.egg_almost_success):
            m.d.comb += self.message_select.eq(MessageSelect.TWO_NOT_TOUCH)
        with m.Else():
            m.d.comb += self.message_select.eq(MessageSelect.TRY_AGAIN)

        with m.If(self.output_enable):
            m.d.comb += self.O.eq(self.I)
        with m.Else():
            m.d.comb += self.O.eq(0)

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
    O: Out(8)

    def __init__(self):
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

        m.d.sync += [
            self._net_2949.eq((((self.net_934) & (self._net_2674)) | ((self._net_2949) & (~((self.net_3037) | (self.net_934)))) | (~((~(~(self.net_934) & (self.net_3037))) | (~((self._net_2676) ^ ((self._net_2609) ^ (self._net_2743)))))))),
            self._net_2609.eq((((self._net_2609) | ((self.net_3037) | (self.net_934))) & ((~((self.net_934) | (~((self._net_2674) ^ ((self._net_2609) ^ (self._net_2949)))) | ~(~((~((self._net_2752) ^ (self._net_2609))) ^ (~((self._net_2826) ^ (self._net_2743))))))) | ((((self.net_934) & (self._net_2689)) | ((~((self.net_934) | (~((~((self._net_2752) ^ (self._net_2609))) ^ (~((self._net_2826) ^ (self._net_2743))))))) & (~((self._net_2674) ^ ((self._net_2609) ^ (self._net_2949))))) | (~((self.net_3037) | (self.net_934)))))))),
            self._net_2676.eq((((~(self.net_934) & (self.net_3037)) & (~((self._net_2689) & (~((self._net_2676) ^ (~((self._net_2752) ^ (self._net_2609))))))) & ((self._net_2689) | (~((self._net_2676) ^ (~((self._net_2752) ^ (self._net_2609))))))) | ((((self.net_934) & (self._net_2826)) | ((~((self.net_3037) | (self.net_934))) & (self._net_2676)))))),
            self._net_2689.eq((((~((self._net_2674) ^ (~((self._net_2676) ^ (~((self._net_2752) ^ (self._net_2609)))))) & (~((self.net_934) | (~((~((self._net_2752) ^ (self._net_2609))) ^ (~((self._net_2826) ^ (self._net_2743)))))))) | (~(self.net_934) & (~((~((self._net_2752) ^ (self._net_2609))) ^ (~((self._net_2826) ^ (self._net_2743))))) & ((self._net_2674) ^ (~((self._net_2676) ^ (~((self._net_2752) ^ (self._net_2609))))))) | ((((self.net_934) & (self._net_2949)) | (~((self.net_3037) | (self.net_934)))))) & (((self.net_3037) | (self.net_934)) | (self._net_2689)))),
            self._net_2826.eq((((~(self.net_934) & (self.net_3037)) & (~((~((self._net_2689) ^ (self._net_2826))) ^ ((self._net_2609) ^ (self._net_2949))))) | ((((self.net_934) & (self._net_2752)) | ((self._net_2826) & (~((self.net_3037) | (self.net_934)))))))),
            self._net_2674.eq((((self._net_2674) | ((self.net_3037) | (self.net_934))) & ((~(~(self.net_934) & (self.net_3037))) | (~((self._net_2676) ^ (~((self._net_2689) ^ (self._net_2826)))))) & (~(((self.I) | (~((~((self._net_2752) ^ (self._net_2609))) ^ (~((self._net_2826) ^ (self._net_2743)))))) & (~(((self.I) & (~((~((self._net_2752) ^ (self._net_2609))) ^ (~((self._net_2826) ^ (self._net_2743)))))) | (~(self.net_934)))))))),
            self._net_2743.eq((((self.net_934) & (self._net_2676)) | ((self._net_2743) & (~((self.net_3037) | (self.net_934)))) | (~((~((~((self._net_2752) ^ (self._net_2609))) ^ (~((self._net_2826) ^ (self._net_2743))))) | (~(~(self.net_934) & (self.net_3037))))))),
            self._net_2752.eq((((self.net_934) & (self._net_2609)) | ((~((self.net_3037) | (self.net_934))) & (self._net_2752)) | (((((self._net_2689) ^ (self._net_2949)) | ((self._net_2674) ^ (self._net_2752))) & (~((((self._net_2689) ^ (self._net_2949)) & ((self._net_2674) ^ (self._net_2752))) | (~(~(self.net_934) & (self.net_3037))))))))),
        ]

        m.d.comb += [
            self.O[0].eq((((~((~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384))))) | ((((self.net_2232) & (~((self.net_3384) | (self.net_3420) | ~(self.net_3419)))) | ((~((self.net_3384) | (self.net_3419) | (self.net_3420))) & (self.net_2006)))) | ((((~((self._net_2674) ^ (~(((~((self.net_1365) & (~(self.net_1351) & (self.net_1363)))) & (~((self.net_1363) & (self.net_1505)))) | (~((self.net_1351) | (~(self.net_1505)))))))) & (~((self.net_3419) | (self.net_3420) | ~(self.net_3384)))) | ((~((self.net_3384) | (self.net_3419) | ~(self.net_3420))) & (self.net_1559))))) & ((self.net_1816) | (~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384)))))),
            self.O[1].eq((((~((~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384))))) | ((((self.net_2315) & (~((self.net_3384) | (self.net_3420) | ~(self.net_3419)))) | ((~((self.net_3384) | (self.net_3419) | (self.net_3420))) & (self.net_2088)))) | ((((~(((~((self.net_1351) | (~(self.net_1505)))) | (~((self.net_1351) | (self.net_1363))) | (~((self.net_1365) | (self.net_1505)))) ^ ((self._net_2949) ^ ((self.net_1363) | (self.net_1365))))) & (~((self.net_3419) | (self.net_3420) | ~(self.net_3384)))) | ((~((self.net_3384) | (self.net_3419) | ~(self.net_3420))) & (self.net_1420))))) & ((self.net_1822) | (~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384)))))),
            self.O[2].eq((((~((~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384))))) | ((((self.net_2313) & (~((self.net_3384) | (self.net_3420) | ~(self.net_3419)))) | ((~((self.net_3384) | (self.net_3419) | (self.net_3420))) & (self.net_1977)))) | ((((~((self._net_2689) ^ (~(((~(~((self.net_1365) & (~(self.net_1351) & (self.net_1363))))) | (~(((self.net_1363) | (self.net_1365)) & (~((self.net_1505) ^ ((self.net_1351) & (self.net_1363) & (self.net_1365))))))) & ((((self.net_1351) & (self.net_1365)) | (~(self.net_1505)) | (~(self.net_1351) & (self.net_1363)))))))) & (~((self.net_3419) | (self.net_3420) | ~(self.net_3384)))) | ((~((self.net_3384) | (self.net_3419) | ~(self.net_3420))) & (self.net_1694))))) & ((self.net_1907) | (~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384)))))),
            self.O[3].eq((((~((~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384))))) | ((((self.net_2460) & (~((self.net_3384) | (self.net_3420) | ~(self.net_3419)))) | ((~((self.net_3384) | (self.net_3419) | (self.net_3420))) & (self.net_2117)))) | (((((self._net_2609) ^ ((((~(~((self.net_1365) & (~(self.net_1351) & (self.net_1363))))) | (~((self.net_1505) ^ ((self.net_1351) & (self.net_1363) & (self.net_1365)))) | (~((self.net_1365) | (~(~((self.net_1351) | (self.net_1363))) & (~((self.net_1351) & (self.net_1363))))))) & ((~(~((self.net_1351) | (self.net_1363))) & (~((self.net_1351) & (self.net_1363)))) | (~(((self.net_1363) | (self.net_1365)) & (~((self.net_1505) ^ ((self.net_1351) & (self.net_1363) & (self.net_1365)))))))))) & (~((self.net_3419) | (self.net_3420) | ~(self.net_3384)))) | ((~((self.net_3384) | (self.net_3419) | ~(self.net_3420))) & (self.net_1516))))) & ((self.net_1936) | (~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384)))))),
            self.O[4].eq((((~((~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384))))) | ((((self.net_2240) & (~((self.net_3384) | (self.net_3420) | ~(self.net_3419)))) | ((~((self.net_3384) | (self.net_3419) | (self.net_3420))) & (self.net_2189)))) | (((((self._net_2752) ^ ((((self.net_1365) | (~((self.net_1351) | (~(self.net_1505)))) | (~(self.net_1351) & (self.net_1363))) & (~((self.net_1363) & (self.net_1505)))))) & (~((self.net_3419) | (self.net_3420) | ~(self.net_3384)))) | ((~((self.net_3384) | (self.net_3419) | ~(self.net_3420))) & (self.net_1472))))) & ((self.net_1927) | (~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384)))))),
            self.O[5].eq((((~((~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384))))) | ((((self.net_2298) & (~((self.net_3384) | (self.net_3420) | ~(self.net_3419)))) | ((~((self.net_3384) | (self.net_3419) | (self.net_3420))) & (self.net_2120)))) | (((((self._net_2826) ^ (~((~(~(self.net_1363) & (self.net_1351))) & ((((~((self.net_1351) | (~(self.net_1505)))) & ((self.net_1363) | (self.net_1365))) | ((~((self.net_1505) ^ ((self.net_1351) & (self.net_1363) & (self.net_1365)))) & ((self.net_1351) | (self.net_1365) | ~(self.net_1363)))))))) & (~((self.net_3419) | (self.net_3420) | ~(self.net_3384)))) | ((~((self.net_3384) | (self.net_3419) | ~(self.net_3420))) & (self.net_1693))))) & ((self.net_1905) | (~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384)))))),
            self.O[6].eq((((~((~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384))))) | ((((self.net_2461) & (~((self.net_3384) | (self.net_3420) | ~(self.net_3419)))) | ((~((self.net_3384) | (self.net_3419) | (self.net_3420))) & (self.net_2154)))) | ((((~((self._net_2676) ^ ((((self.net_1351) & (~((self.net_1365) | (self.net_1505)))) | ((~(~(self.net_1363) & (self.net_1351))) & (self.net_1365)))))) & (~((self.net_3419) | (self.net_3420) | ~(self.net_3384)))) | ((~((self.net_3384) | (self.net_3419) | ~(self.net_3420))) & (self.net_1629))))) & ((self.net_1928) | (~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384)))))),
            self.O[7].eq((((~((~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384))))) | ((((self.net_2479) & (~((self.net_3384) | (self.net_3420) | ~(self.net_3419)))) | ((~((self.net_3384) | (self.net_3419) | (self.net_3420))) & (self.net_2004)))) | ((((~((self._net_2743) ^ ((((self.net_1365) & (~(self.net_1505)) & (~((self.net_1351) & (self.net_1363)))) | (~(((self.net_1351) & (~(self.net_1505))) | (((self.net_1363) | (self.net_1365)) & (~((self.net_1351) & (self.net_1363)))))))))) & (~((self.net_3419) | (self.net_3420) | ~(self.net_3384)))) | ((~((self.net_3384) | (self.net_3419) | ~(self.net_3420))) & (self.net_1425))))) & ((self.net_1815) | (~((self.net_3419) | (self.net_3420) | ~(self.net_3384))) | (~(((self.net_3419) & (self.net_3420)) | (self.net_3384)))))),
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

class Regions(wiring.Component):
    """
    Decides which region of the image a particular bit is in

    Represents an image with the letters JSC written across it

    JSC presumably stands for Jane Street Capital

    This permutation of bits was chosen because:
    * The letters J, S and C, correspond nicely to values 0, 1 and 2
    * The maximum value of the image is 10, much like the counters

    Actually, bit order doesn't really matter, but it does make the checker look nicer
    """
    x: In(4)
    y: In(4)
    out: Out(4)

    IMAGE = (
        (6, 6, 6, 6, 6, 8, 8, 5, 4, 4, 9),
        (6, 6, 0, 6, 6, 8, 5, 5, 4, 4, 9),
        (6, 6, 0, 8, 8, 8, 8, 5, 5, 4, 9),
        (6, 6, 0, 8, 1, 1, 1, 9, 5, 5, 9),
        (0, 6, 0, 8, 1, 9, 9, 9, 9, 9, 9),
        (0, 0, 0, 8, 1, 1, 1, 9, 2, 2, 2),
        (8, 8, 8, 8, 8, 8, 1, 9, 2, 10, 10),
        (8, 7, 7, 7, 1, 1, 1, 9, 2, 10, 10),
        (8, 7, 7, 3, 9, 9, 9, 9, 2, 10, 10),
        (8, 8, 7, 3, 3, 9, 9, 9, 2, 2, 2),
        (8, 7, 7, 3, 9, 9, 9, 9, 9, 9, 9),
    )

    def elaborate(self, platform):
        m = Module()

        m.submodules.rom = Memory(width=4, depth=256, init=list(chain.from_iterable(self.IMAGE)))
        rd_port = m.submodules.rom.read_port(domain="comb")

        m.d.comb += [
            rd_port.addr.eq(11 * self.y + self.x), # Yes, this is specifically how it's implemented, you can tell from the artifacts it generates with out-of-range inputs!
            self.out.eq(rd_port.data),
        ]

        return m

class puzzle(wiring.Component):
    I: In(1)
    enable: In(1)
    net_1447: In(1)
    O: Out(8)
    success: Out(1)

    # Testing outputs
    net_934: Out(1)
    net_3136: Out(1)
    net_1526: Out(1)
    net_832: Out(1)
    net_20: Out(1)
    net_380: Out(1)
    net_319: Out(1)
    net_1508: Out(1)
    net_435: Out(1)
    net_323: Out(1)
    net_378: Out(1)
    net_377: Out(1)
    net_2259: Out(1)
    net_2505: Out(1)
    net_1723: Out(1)
    net_1719: Out(1)
    net_1628: Out(1)
    net_1738: Out(1)
    net_1557: Out(1)
    net_719: Out(1)
    net_1084: Out(1)
    net_791: Out(1)
    net_343: Out(1)
    net_2386: Out(1)
    net_2463: Out(1)
    net_2459: Out(1)
    net_2480: Out(1)
    net_2475: Out(1)
    net_3283: Out(1)
    net_2474: Out(1)
    net_2471: Out(1)
    net_2393: Out(1)
    net_3830: Out(1)
    net_2416: Out(1)
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
    net_3771: Out(1)
    net_3920: Out(1)
    net_1351: Out(1)
    net_1365: Out(1)
    net_3037: Out(1)
    net_3419: Out(1)
    net_3420: Out(1)
    net_3384: Out(1)
    net_1505: Out(1)
    net_1363: Out(1)
    net_3617: Out(1)
    net_3516: Out(1)
    net_3435: Out(1)
    net_3543: Out(1)
    net_3552: Out(1)
    net_3613: Out(1)
    net_3518: Out(1)
    net_3818: Out(1)
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
    net_1927: Out(1)
    net_1816: Out(1)
    net_1936: Out(1)
    net_1905: Out(1)
    net_1815: Out(1)
    net_1928: Out(1)
    net_1907: Out(1)
    net_1822: Out(1)
    net_1425: Out(1)
    net_1693: Out(1)
    net_1694: Out(1)
    net_1516: Out(1)
    net_1420: Out(1)
    net_1559: Out(1)
    net_1629: Out(1)
    net_1472: Out(1)
    net_736: Out(1)
    net_1034: Out(1)
    net_857: Out(1)
    net_985: Out(1)

    def elaborate(self, platform):
        m = Module()

        m.submodules.done_controller = DoneController()
        m.submodules.x_counter = Counter11()
        m.submodules.y_counter = Counter11()
        m.submodules.adjacency_checker = AdjacencyChecker()
        m.submodules.row_checker = RowChecker()
        m.submodules.edge_checker = EdgeChecker()
        m.submodules.popcnt_checker = PopCntChecker()
        m.submodules.column_checker = ColumnChecker()
        m.submodules.region_checker = ColumnChecker()
        m.submodules.success_controller = SuccessController()
        m.submodules.output_controller = OutputController()
        m.submodules.output_eternaforest = Output_EternaForest()
        m.submodules.output_lakeacuity = Output_LakeAcuity()
        m.submodules.output_lakeverity = Output_LakeVerity()
        m.submodules.output_lakevalor = Output_LakeValor()
        m.submodules.regions = Regions()

        m.d.comb += [
            m.submodules.done_controller.y_overflow.eq(m.submodules.y_counter.overflow),
            m.submodules.done_controller.x_overflow.eq(m.submodules.x_counter.overflow),
            m.submodules.done_controller.enable.eq(self.enable),
            m.submodules.x_counter.enable.eq(m.submodules.done_controller.enable_gated),
            m.submodules.x_counter.increment.eq(1),
            m.submodules.y_counter.enable.eq(m.submodules.done_controller.enable_gated),
            m.submodules.y_counter.increment.eq(m.submodules.x_counter.overflow),
            m.submodules.adjacency_checker.enable.eq(m.submodules.done_controller.enable_gated),
            m.submodules.adjacency_checker.I.eq(self.I),
            m.submodules.adjacency_checker.top_left_available.eq(m.submodules.edge_checker.top_left_available),
            m.submodules.adjacency_checker.top_available.eq(m.submodules.edge_checker.top_available),
            m.submodules.adjacency_checker.top_right_available.eq(m.submodules.edge_checker.top_right_available),
            m.submodules.adjacency_checker.left_available.eq(m.submodules.edge_checker.left_available),
            m.submodules.row_checker.enable.eq(m.submodules.done_controller.enable_gated),
            m.submodules.row_checker.I.eq(self.I),
            m.submodules.row_checker.x_overflow.eq(m.submodules.x_counter.overflow),
            m.submodules.edge_checker.x.eq(m.submodules.x_counter.count),
            m.submodules.popcnt_checker.enable.eq(m.submodules.done_controller.enable_gated),
            m.submodules.popcnt_checker.I.eq(self.I),
            m.submodules.column_checker.enable.eq(m.submodules.done_controller.enable_gated),
            m.submodules.column_checker.I.eq(self.I),
            m.submodules.column_checker.x.eq(m.submodules.x_counter.count),
            m.submodules.region_checker.enable.eq(m.submodules.done_controller.enable_gated),
            m.submodules.region_checker.I.eq(self.I),
            m.submodules.region_checker.x.eq(m.submodules.regions.out),
            m.submodules.success_controller.done.eq(m.submodules.done_controller.done),
            m.submodules.success_controller.adjacency_property.eq(m.submodules.adjacency_checker.result),
            m.submodules.success_controller.column_property.eq(m.submodules.column_checker.result),
            m.submodules.success_controller.region_property.eq(m.submodules.region_checker.result),
            m.submodules.success_controller.row_property.eq(m.submodules.row_checker.result),
            m.submodules.success_controller.popcnt_property.eq(m.submodules.popcnt_checker.result),
            m.submodules.output_controller.done_delayed.eq(m.submodules.success_controller.done_delayed),
            m.submodules.output_controller.egg_almost_success.eq(m.submodules.success_controller.almost_success),
            m.submodules.output_controller.egg_full.eq(m.submodules.popcnt_checker.full),
            m.submodules.output_controller.egg_empty.eq(m.submodules.popcnt_checker.empty),
            m.submodules.output_controller.success.eq(m.submodules.success_controller.success),
            m.submodules.output_controller.I.eq(m.submodules.output_eternaforest.O),
            m.submodules.output_eternaforest.net_1351.eq(m.submodules.output_controller.char_index[0]),
            m.submodules.output_eternaforest.net_1365.eq(m.submodules.output_controller.char_index[2]),
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
            m.submodules.output_eternaforest.net_3037.eq(m.submodules.output_controller.output_enable),
            m.submodules.output_eternaforest.net_934.eq(m.submodules.done_controller.enable_gated),
            m.submodules.output_eternaforest.net_3419.eq(m.submodules.output_controller.message_select[0]),
            m.submodules.output_eternaforest.net_3420.eq(m.submodules.output_controller.message_select[2]),
            m.submodules.output_eternaforest.net_3384.eq(m.submodules.output_controller.message_select[1]),
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
            m.submodules.output_eternaforest.net_1505.eq(m.submodules.output_controller.char_index[3]),
            m.submodules.output_eternaforest.I.eq(self.I),
            m.submodules.output_eternaforest.net_1363.eq(m.submodules.output_controller.char_index[1]),
            m.submodules.output_lakeacuity.net_1351.eq(m.submodules.output_controller.char_index[0]),
            m.submodules.output_lakeacuity.net_1505.eq(m.submodules.output_controller.char_index[3]),
            m.submodules.output_lakeacuity.net_1365.eq(m.submodules.output_controller.char_index[2]),
            m.submodules.output_lakeacuity.net_1363.eq(m.submodules.output_controller.char_index[1]),
            m.submodules.output_lakeverity.net_1363.eq(m.submodules.output_controller.char_index[1]),
            m.submodules.output_lakeverity.net_1365.eq(m.submodules.output_controller.char_index[2]),
            m.submodules.output_lakeverity.net_1351.eq(m.submodules.output_controller.char_index[0]),
            m.submodules.output_lakeverity.net_1505.eq(m.submodules.output_controller.char_index[3]),
            m.submodules.output_lakevalor.net_1365.eq(m.submodules.output_controller.char_index[2]),
            m.submodules.output_lakevalor.net_1351.eq(m.submodules.output_controller.char_index[0]),
            m.submodules.output_lakevalor.net_1505.eq(m.submodules.output_controller.char_index[3]),
            m.submodules.output_lakevalor.net_1363.eq(m.submodules.output_controller.char_index[1]),
            m.submodules.output_lakevalor.net_1447.eq(self.net_1447),
            m.submodules.regions.x.eq(m.submodules.x_counter.count),
            m.submodules.regions.y.eq(m.submodules.y_counter.count),
        ]

        m.d.comb += [
            self.O.eq(m.submodules.output_controller.O),
            self.success.eq(m.submodules.success_controller.success),
        ]

        # Testing outputs
        m.d.comb += [
            self.net_934.eq(m.submodules.done_controller.enable_gated),
            self.net_3136.eq(m.submodules.done_controller.done),
            self.net_1526.eq(m.submodules.x_counter.overflow),
            self.net_832.eq(m.submodules.x_counter.count[3]),
            self.net_20.eq(m.submodules.x_counter.count[1]),
            self.net_380.eq(m.submodules.x_counter.count[2]),
            self.net_319.eq(m.submodules.x_counter.count[0]),
            self.net_1508.eq(m.submodules.y_counter.overflow),
            self.net_435.eq(m.submodules.y_counter.count[2]),
            self.net_323.eq(m.submodules.y_counter.count[0]),
            self.net_378.eq(m.submodules.y_counter.count[3]),
            self.net_377.eq(m.submodules.y_counter.count[1]),
            self.net_2259.eq(m.submodules.adjacency_checker.result),
            self.net_2505.eq(m.submodules.column_checker.result),
            self.net_1723.eq(m.submodules.edge_checker.top_left_available),
            self.net_1719.eq(m.submodules.edge_checker.left_available),
            self.net_1628.eq(m.submodules.edge_checker.top_available),
            self.net_1738.eq(m.submodules.edge_checker.top_right_available),
            self.net_1557.eq(m.submodules.row_checker.result),
            self.net_719.eq(m.submodules.popcnt_checker.result),
            self.net_1084.eq(m.submodules.popcnt_checker.full),
            self.net_791.eq(m.submodules.popcnt_checker.empty),
            self.net_343.eq(m.submodules.region_checker.result),
            self.net_2386.eq(m.submodules.column_checker.results[10]),
            self.net_2463.eq(m.submodules.column_checker.results[9]),
            self.net_2459.eq(m.submodules.column_checker.results[8]),
            self.net_2480.eq(m.submodules.column_checker.results[3]),
            self.net_2475.eq(m.submodules.column_checker.results[2]),
            self.net_3283.eq(m.submodules.column_checker.results[1]),
            self.net_2474.eq(m.submodules.column_checker.results[7]),
            self.net_2471.eq(m.submodules.column_checker.results[6]),
            self.net_2393.eq(m.submodules.column_checker.results[4]),
            self.net_3830.eq(m.submodules.column_checker.results[5]),
            self.net_2416.eq(m.submodules.column_checker.results[0]),
            self.net_204.eq(m.submodules.region_checker.results[7]),
            self.net_203.eq(m.submodules.region_checker.results[6]),
            self.net_294.eq(m.submodules.region_checker.results[4]),
            self.net_226.eq(m.submodules.region_checker.results[5]),
            self.net_545.eq(m.submodules.region_checker.results[10]),
            self.net_1185.eq(m.submodules.region_checker.results[9]),
            self.net_341.eq(m.submodules.region_checker.results[8]),
            self.net_401.eq(m.submodules.region_checker.results[3]),
            self.net_399.eq(m.submodules.region_checker.results[2]),
            self.net_405.eq(m.submodules.region_checker.results[0]),
            self.net_349.eq(m.submodules.region_checker.results[1]),
            self.net_3771.eq(m.submodules.success_controller.done_delayed),
            self.net_3920.eq(m.submodules.success_controller.almost_success),
            self.net_1351.eq(m.submodules.output_controller.char_index[0]),
            self.net_1365.eq(m.submodules.output_controller.char_index[2]),
            self.net_3037.eq(m.submodules.output_controller.output_enable),
            self.net_3419.eq(m.submodules.output_controller.message_select[0]),
            self.net_3420.eq(m.submodules.output_controller.message_select[2]),
            self.net_3384.eq(m.submodules.output_controller.message_select[1]),
            self.net_1505.eq(m.submodules.output_controller.char_index[3]),
            self.net_1363.eq(m.submodules.output_controller.char_index[1]),
            self.net_3617.eq(m.submodules.output_eternaforest.O[0]),
            self.net_3516.eq(m.submodules.output_eternaforest.O[2]),
            self.net_3435.eq(m.submodules.output_eternaforest.O[7]),
            self.net_3543.eq(m.submodules.output_eternaforest.O[5]),
            self.net_3552.eq(m.submodules.output_eternaforest.O[4]),
            self.net_3613.eq(m.submodules.output_eternaforest.O[3]),
            self.net_3518.eq(m.submodules.output_eternaforest.O[6]),
            self.net_3818.eq(m.submodules.output_eternaforest.O[1]),
            self.net_2232.eq(m.submodules.output_lakeacuity.net_2232),
            self.net_2006.eq(m.submodules.output_lakeacuity.net_2006),
            self.net_2313.eq(m.submodules.output_lakeacuity.net_2313),
            self.net_1977.eq(m.submodules.output_lakeacuity.net_1977),
            self.net_2315.eq(m.submodules.output_lakeacuity.net_2315),
            self.net_2088.eq(m.submodules.output_lakeacuity.net_2088),
            self.net_2298.eq(m.submodules.output_lakeacuity.net_2298),
            self.net_2120.eq(m.submodules.output_lakeacuity.net_2120),
            self.net_2460.eq(m.submodules.output_lakeacuity.net_2460),
            self.net_2117.eq(m.submodules.output_lakeacuity.net_2117),
            self.net_2240.eq(m.submodules.output_lakeacuity.net_2240),
            self.net_2189.eq(m.submodules.output_lakeacuity.net_2189),
            self.net_2461.eq(m.submodules.output_lakeacuity.net_2461),
            self.net_2154.eq(m.submodules.output_lakeacuity.net_2154),
            self.net_2479.eq(m.submodules.output_lakeacuity.net_2479),
            self.net_2004.eq(m.submodules.output_lakeacuity.net_2004),
            self.net_1927.eq(m.submodules.output_lakeverity.net_1927),
            self.net_1816.eq(m.submodules.output_lakeverity.net_1816),
            self.net_1936.eq(m.submodules.output_lakeverity.net_1936),
            self.net_1905.eq(m.submodules.output_lakeverity.net_1905),
            self.net_1815.eq(m.submodules.output_lakeverity.net_1815),
            self.net_1928.eq(m.submodules.output_lakeverity.net_1928),
            self.net_1907.eq(m.submodules.output_lakeverity.net_1907),
            self.net_1822.eq(m.submodules.output_lakeverity.net_1822),
            self.net_1425.eq(m.submodules.output_lakevalor.net_1425),
            self.net_1693.eq(m.submodules.output_lakevalor.net_1693),
            self.net_1694.eq(m.submodules.output_lakevalor.net_1694),
            self.net_1516.eq(m.submodules.output_lakevalor.net_1516),
            self.net_1420.eq(m.submodules.output_lakevalor.net_1420),
            self.net_1559.eq(m.submodules.output_lakevalor.net_1559),
            self.net_1629.eq(m.submodules.output_lakevalor.net_1629),
            self.net_1472.eq(m.submodules.output_lakevalor.net_1472),
            self.net_736.eq(m.submodules.regions.out[0]),
            self.net_1034.eq(m.submodules.regions.out[3]),
            self.net_857.eq(m.submodules.regions.out[1]),
            self.net_985.eq(m.submodules.regions.out[2]),
        ]

        return m

if __name__ == "__main__":
    from amaranth.back import verilog
    top = puzzle()
    with open(argv[1], "wt") as f:
        f.write(verilog.convert(top, name="puzzle_solution", ports=[
            top.I,
            top.enable,
            top.net_1447,
            top.net_934,
            top.net_3136,
            top.net_1526,
            top.net_832,
            top.net_20,
            top.net_380,
            top.net_319,
            top.net_1508,
            top.net_435,
            top.net_323,
            top.net_378,
            top.net_377,
            top.net_2259,
            top.net_2505,
            top.net_1723,
            top.net_1719,
            top.net_1628,
            top.net_1738,
            top.net_1557,
            top.net_719,
            top.net_1084,
            top.net_791,
            top.net_343,
            top.net_2386,
            top.net_2463,
            top.net_2459,
            top.net_2480,
            top.net_2475,
            top.net_3283,
            top.net_2474,
            top.net_2471,
            top.net_2393,
            top.net_3830,
            top.net_2416,
            top.net_204,
            top.net_203,
            top.net_294,
            top.net_226,
            top.net_545,
            top.net_1185,
            top.net_341,
            top.net_401,
            top.net_399,
            top.net_405,
            top.net_349,
            top.net_3771,
            top.net_3920,
            top.success,
            top.net_1351,
            top.net_1365,
            top.net_3037,
            top.net_3419,
            top.net_3420,
            top.net_3384,
            top.net_1505,
            top.net_1363,
            top.O,
            top.net_3617,
            top.net_3516,
            top.net_3435,
            top.net_3543,
            top.net_3552,
            top.net_3613,
            top.net_3518,
            top.net_3818,
            top.net_2232,
            top.net_2006,
            top.net_2313,
            top.net_1977,
            top.net_2315,
            top.net_2088,
            top.net_2298,
            top.net_2120,
            top.net_2460,
            top.net_2117,
            top.net_2240,
            top.net_2189,
            top.net_2461,
            top.net_2154,
            top.net_2479,
            top.net_2004,
            top.net_1927,
            top.net_1816,
            top.net_1936,
            top.net_1905,
            top.net_1815,
            top.net_1928,
            top.net_1907,
            top.net_1822,
            top.net_1425,
            top.net_1693,
            top.net_1694,
            top.net_1516,
            top.net_1420,
            top.net_1559,
            top.net_1629,
            top.net_1472,
            top.net_736,
            top.net_1034,
            top.net_857,
            top.net_985,
        ]))
