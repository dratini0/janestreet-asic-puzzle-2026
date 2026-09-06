from enum import Enum
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

            with m.If(
                self.I
                & (
                    self.top_left_available & self._sr[11]
                    | self.top_available & self._sr[10]
                    | self.top_right_available & self._sr[9]
                    | self.left_available & self._sr[0]
                )
            ):
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

        with m.If(
            (self.x == self._column) & self.I & self.enable & (self._counter != 3)
        ):
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
                self.success.eq(
                    self.adjacency_property
                    & self.row_property
                    & self.popcnt_property
                    & self.region_property
                    & self.column_property
                ),
                self.almost_success.eq(
                    ~self.adjacency_property
                    & self.row_property
                    & self.popcnt_property
                    & self.region_property
                    & self.column_property
                ),
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


class OutputFlagObfuscator(wiring.Component):
    enable: In(1)
    I: In(1)
    output_enable: In(1)
    char_index: In(4)
    message_select: In(MessageSelect)
    I_empty_sky: In(8)
    I_big_bang: In(8)
    I_try_again: In(8)
    I_two_not_touch: In(8)
    O: Out(8)

    def __init__(self):
        self._state = Signal(8, init=0xA5)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.enable):
            m.d.sync += self._state.eq(
                Cat(
                    self.I
                    ^ self._state[3]
                    ^ self._state[4]
                    ^ self._state[5]
                    ^ self._state[7],
                    self._state[:7],
                )
            )

        # fmt: off
        with m.Elif(self.output_enable):
            m.d.sync += [
                self._state[0].eq(self._state[5] ^ self._state[2] ^ self._state[6]),
                self._state[1].eq(self._state[7] ^ self._state[6] ^ self._state[3]),
                self._state[2].eq(self._state[7] ^ self._state[0] ^ self._state[5] ^ self._state[6]),
                self._state[3].eq(self._state[1] ^ self._state[4] ^ self._state[0] ^ self._state[7] ^ self._state[5]),
                self._state[4].eq(self._state[1] ^ self._state[4] ^ self._state[0] ^ self._state[2]),
                self._state[5].eq(self._state[1] ^ self._state[5] ^ self._state[2] ^ self._state[3]),
                self._state[6].eq(self._state[4] ^ self._state[2] ^ self._state[6] ^ self._state[3]),
                self._state[7].eq(self._state[4] ^ self._state[7] ^ self._state[5] ^ self._state[3]),
            ]
        # fmt: on

        with m.Switch(self.message_select):
            with m.Case(MessageSelect.EMPTY_SKY):
                m.d.comb += self.O.eq(self.I_empty_sky)

            with m.Case(MessageSelect.BIG_BANG):
                m.d.comb += self.O.eq(self.I_big_bang)

            with m.Case(MessageSelect.FLAG):
                with m.Switch(self.char_index):
                    with m.Case(0):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(self._state[1]),
                            self.O[2].eq(~self._state[2]),
                            self.O[3].eq(~self._state[3]),
                            self.O[4].eq(self._state[4]),
                            self.O[5].eq(self._state[5]),
                            self.O[6].eq(~self._state[6]),
                            self.O[7].eq(self._state[7]),
                        ]

                    with m.Case(1):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(self._state[1]),
                            self.O[2].eq(~self._state[2]),
                            self.O[3].eq(~self._state[3]),
                            self.O[4].eq(self._state[4]),
                            self.O[5].eq(~self._state[5]),
                            self.O[6].eq(self._state[6]),
                            self.O[7].eq(~self._state[7]),
                        ]

                    with m.Case(2):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(~self._state[1]),
                            self.O[2].eq(self._state[2]),
                            self.O[3].eq(~self._state[3]),
                            self.O[4].eq(~self._state[4]),
                            self.O[5].eq(~self._state[5]),
                            self.O[6].eq(~self._state[6]),
                            self.O[7].eq(~self._state[7]),
                        ]

                    with m.Case(3):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(~self._state[1]),
                            self.O[2].eq(self._state[2]),
                            self.O[3].eq(self._state[3]),
                            self.O[4].eq(self._state[4]),
                            self.O[5].eq(self._state[5]),
                            self.O[6].eq(self._state[6]),
                            self.O[7].eq(~self._state[7]),
                        ]

                    with m.Case(4):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(~self._state[1]),
                            self.O[2].eq(self._state[2]),
                            self.O[3].eq(self._state[3]),
                            self.O[4].eq(~self._state[4]),
                            self.O[5].eq(self._state[5]),
                            self.O[6].eq(self._state[6]),
                            self.O[7].eq(self._state[7]),
                        ]

                    with m.Case(5):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(self._state[1]),
                            self.O[2].eq(self._state[2]),
                            self.O[3].eq(~self._state[3]),
                            self.O[4].eq(~self._state[4]),
                            self.O[5].eq(~self._state[5]),
                            self.O[6].eq(~self._state[6]),
                            self.O[7].eq(self._state[7]),
                        ]

                    with m.Case(6):
                        m.d.comb += [
                            self.O[0].eq(self._state[0]),
                            self.O[1].eq(self._state[1]),
                            self.O[2].eq(~self._state[2]),
                            self.O[3].eq(~self._state[3]),
                            self.O[4].eq(~self._state[4]),
                            self.O[5].eq(self._state[5]),
                            self.O[6].eq(self._state[6]),
                            self.O[7].eq(self._state[7]),
                        ]

                    with m.Case(7):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(self._state[1]),
                            self.O[2].eq(~self._state[2]),
                            self.O[3].eq(self._state[3]),
                            self.O[4].eq(~self._state[4]),
                            self.O[5].eq(~self._state[5]),
                            self.O[6].eq(self._state[6]),
                            self.O[7].eq(~self._state[7]),
                        ]

                    with m.Case(8):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(self._state[1]),
                            self.O[2].eq(self._state[2]),
                            self.O[3].eq(~self._state[3]),
                            self.O[4].eq(~self._state[4]),
                            self.O[5].eq(~self._state[5]),
                            self.O[6].eq(~self._state[6]),
                            self.O[7].eq(self._state[7]),
                        ]

                    with m.Case(9):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(~self._state[1]),
                            self.O[2].eq(self._state[2]),
                            self.O[3].eq(self._state[3]),
                            self.O[4].eq(self._state[4]),
                            self.O[5].eq(~self._state[5]),
                            self.O[6].eq(~self._state[6]),
                            self.O[7].eq(self._state[7]),
                        ]

                    with m.Case(10):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(~self._state[1]),
                            self.O[2].eq(~self._state[2]),
                            self.O[3].eq(self._state[3]),
                            self.O[4].eq(self._state[4]),
                            self.O[5].eq(self._state[5]),
                            self.O[6].eq(~self._state[6]),
                            self.O[7].eq(~self._state[7]),
                        ]

                    with m.Case(11):
                        m.d.comb += [
                            self.O[0].eq(self._state[0]),
                            self.O[1].eq(self._state[1]),
                            self.O[2].eq(self._state[2]),
                            self.O[3].eq(~self._state[3]),
                            self.O[4].eq(self._state[4]),
                            self.O[5].eq(~self._state[5]),
                            self.O[6].eq(~self._state[6]),
                            self.O[7].eq(self._state[7]),
                        ]

                    with m.Case(12):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(~self._state[1]),
                            self.O[2].eq(self._state[2]),
                            self.O[3].eq(self._state[3]),
                            self.O[4].eq(~self._state[4]),
                            self.O[5].eq(self._state[5]),
                            self.O[6].eq(self._state[6]),
                            self.O[7].eq(~self._state[7]),
                        ]

                    with m.Case(13):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(self._state[1]),
                            self.O[2].eq(~self._state[2]),
                            self.O[3].eq(self._state[3]),
                            self.O[4].eq(~self._state[4]),
                            self.O[5].eq(~self._state[5]),
                            self.O[6].eq(~self._state[6]),
                            self.O[7].eq(~self._state[7]),
                        ]

                    with m.Case(14):
                        m.d.comb += [
                            self.O[0].eq(~self._state[0]),
                            self.O[1].eq(~self._state[1]),
                            self.O[2].eq(~self._state[2]),
                            self.O[3].eq(~self._state[3]),
                            self.O[4].eq(self._state[4]),
                            self.O[5].eq(self._state[5]),
                            self.O[6].eq(self._state[6]),
                            self.O[7].eq(~self._state[7]),
                        ]

                    with m.Case(15):
                        m.d.comb += [
                            self.O[0].eq(self._state[0]),
                            self.O[1].eq(self._state[1]),
                            self.O[2].eq(self._state[2]),
                            self.O[3].eq(self._state[3]),
                            self.O[4].eq(self._state[4]),
                            self.O[5].eq(self._state[5]),
                            self.O[6].eq(self._state[6]),
                            self.O[7].eq(self._state[7]),
                        ]

            with m.Case(MessageSelect.TRY_AGAIN):
                m.d.comb += self.O.eq(self.I_try_again)

            with m.Case(MessageSelect.TWO_NOT_TOUCH):
                m.d.comb += self.O.eq(self.I_two_not_touch)

            with m.Default():
                m.d.comb += self.O.eq(self.I_try_again)

        return m


class OutputStringGenerator(wiring.Component):
    char_index: In(4)
    O: Out(8)

    def __init__(self, string: str):
        self._string = string

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.submodules.rom = Memory(width=8, depth=16, init=self._string.encode())
        rd_port = m.submodules.rom.read_port(domain="comb")

        m.d.comb += [
            rd_port.addr.eq(self.char_index),
            self.O.eq(rd_port.data),
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

        m.submodules.rom = Memory(
            width=4, depth=256, init=list(chain.from_iterable(self.IMAGE))
        )
        rd_port = m.submodules.rom.read_port(domain="comb")

        m.d.comb += [
            rd_port.addr.eq(
                11 * self.y + self.x
            ),  # Yes, this is specifically how it's implemented, you can tell from the artifacts it generates with out-of-range inputs!
            self.out.eq(rd_port.data),
        ]

        return m


class puzzle(wiring.Component):
    I: In(1)
    enable: In(1)
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
        m.submodules.output_flag_obfuscator = OutputFlagObfuscator()
        m.submodules.output_string_big_bang = OutputStringGenerator("BIG BANG")
        m.submodules.output_string_empty_sky = OutputStringGenerator("EMPTY SKY")
        m.submodules.output_string_try_again = OutputStringGenerator("TRY AGAIN")
        m.submodules.output_string_two_not_touch = OutputStringGenerator(
            "TWO NOT TOUCH"
        )
        m.submodules.regions = Regions()

        # fmt: off
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
            m.submodules.output_controller.I.eq(m.submodules.output_flag_obfuscator.O),
            m.submodules.output_flag_obfuscator.enable.eq(m.submodules.done_controller.enable_gated),
            m.submodules.output_flag_obfuscator.I.eq(self.I),
            m.submodules.output_flag_obfuscator.output_enable.eq(m.submodules.output_controller.output_enable),
            m.submodules.output_flag_obfuscator.char_index.eq(m.submodules.output_controller.char_index),
            m.submodules.output_flag_obfuscator.message_select.eq(m.submodules.output_controller.message_select),
            m.submodules.output_flag_obfuscator.I_big_bang.eq(m.submodules.output_string_big_bang.O),
            m.submodules.output_flag_obfuscator.I_empty_sky.eq(m.submodules.output_string_empty_sky.O),
            m.submodules.output_flag_obfuscator.I_try_again.eq(m.submodules.output_string_try_again.O),
            m.submodules.output_flag_obfuscator.I_two_not_touch.eq(m.submodules.output_string_two_not_touch.O),
            m.submodules.output_string_big_bang.char_index.eq(m.submodules.output_controller.char_index),
            m.submodules.output_string_empty_sky.char_index.eq(m.submodules.output_controller.char_index),
            m.submodules.output_string_try_again.char_index.eq(m.submodules.output_controller.char_index),
            m.submodules.output_string_two_not_touch.char_index.eq(m.submodules.output_controller.char_index),
            m.submodules.regions.x.eq(m.submodules.x_counter.count),
            m.submodules.regions.y.eq(m.submodules.y_counter.count),
        ]
        # fmt: on

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
            self.net_3617.eq(m.submodules.output_flag_obfuscator.O[0]),
            self.net_3516.eq(m.submodules.output_flag_obfuscator.O[2]),
            self.net_3435.eq(m.submodules.output_flag_obfuscator.O[7]),
            self.net_3543.eq(m.submodules.output_flag_obfuscator.O[5]),
            self.net_3552.eq(m.submodules.output_flag_obfuscator.O[4]),
            self.net_3613.eq(m.submodules.output_flag_obfuscator.O[3]),
            self.net_3518.eq(m.submodules.output_flag_obfuscator.O[6]),
            self.net_3818.eq(m.submodules.output_flag_obfuscator.O[1]),
            self.net_2232.eq(m.submodules.output_string_big_bang.O[0]),
            self.net_2006.eq(m.submodules.output_string_empty_sky.O[0]),
            self.net_2313.eq(m.submodules.output_string_big_bang.O[2]),
            self.net_1977.eq(m.submodules.output_string_empty_sky.O[2]),
            self.net_2315.eq(m.submodules.output_string_big_bang.O[1]),
            self.net_2088.eq(m.submodules.output_string_empty_sky.O[1]),
            self.net_2298.eq(m.submodules.output_string_big_bang.O[5]),
            self.net_2120.eq(m.submodules.output_string_empty_sky.O[5]),
            self.net_2460.eq(m.submodules.output_string_big_bang.O[3]),
            self.net_2117.eq(m.submodules.output_string_empty_sky.O[3]),
            self.net_2240.eq(m.submodules.output_string_big_bang.O[4]),
            self.net_2189.eq(m.submodules.output_string_empty_sky.O[4]),
            self.net_2461.eq(m.submodules.output_string_big_bang.O[6]),
            self.net_2154.eq(m.submodules.output_string_empty_sky.O[6]),
            self.net_2479.eq(m.submodules.output_string_big_bang.O[7]),
            self.net_2004.eq(m.submodules.output_string_empty_sky.O[7]),
            self.net_1927.eq(m.submodules.output_string_try_again.O[4]),
            self.net_1816.eq(m.submodules.output_string_try_again.O[0]),
            self.net_1936.eq(m.submodules.output_string_try_again.O[3]),
            self.net_1905.eq(m.submodules.output_string_try_again.O[5]),
            self.net_1815.eq(m.submodules.output_string_try_again.O[7]),
            self.net_1928.eq(m.submodules.output_string_try_again.O[6]),
            self.net_1907.eq(m.submodules.output_string_try_again.O[2]),
            self.net_1822.eq(m.submodules.output_string_try_again.O[1]),
            self.net_1425.eq(m.submodules.output_string_two_not_touch.O[7]),
            self.net_1693.eq(m.submodules.output_string_two_not_touch.O[5]),
            self.net_1694.eq(m.submodules.output_string_two_not_touch.O[2]),
            self.net_1516.eq(m.submodules.output_string_two_not_touch.O[3]),
            self.net_1420.eq(m.submodules.output_string_two_not_touch.O[1]),
            self.net_1559.eq(m.submodules.output_string_two_not_touch.O[0]),
            self.net_1629.eq(m.submodules.output_string_two_not_touch.O[6]),
            self.net_1472.eq(m.submodules.output_string_two_not_touch.O[4]),
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
        f.write(
            verilog.convert(
                top,
                name="puzzle_solution",
                ports=[
                    top.I,
                    top.enable,
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
                ],
            )
        )
