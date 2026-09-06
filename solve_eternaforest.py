#!/usr/bin/env python3


from pyeda.boolalg.minimization import espresso_exprs
from pyeda.boolalg.expr import Xor, Xnor
from pyeda.boolalg.bfarray import exprvar, exprvars

enable = exprvar("self.enable")
I = exprvar("self.I")
output_enable = exprvar("self.output_enable")
char_index = exprvars("self.char_index", 4)
message_select = exprvars("self.message_select", 3)

net_2232 = exprvar("self.net_2232")
net_2006 = exprvar("self.net_2006")
net_1425 = exprvar("self.net_1425")
net_1693 = exprvar("self.net_1693")
net_1694 = exprvar("self.net_1694")
net_1516 = exprvar("self.net_1516")
net_2313 = exprvar("self.net_2313")
net_1977 = exprvar("self.net_1977")
net_1927 = exprvar("self.net_1927")
net_2315 = exprvar("self.net_2315")
net_2088 = exprvar("self.net_2088")
net_2298 = exprvar("self.net_2298")
net_2120 = exprvar("self.net_2120")
net_2460 = exprvar("self.net_2460")
net_2117 = exprvar("self.net_2117")
net_2240 = exprvar("self.net_2240")
net_2189 = exprvar("self.net_2189")
net_1420 = exprvar("self.net_1420")
net_1559 = exprvar("self.net_1559")
net_1816 = exprvar("self.net_1816")
net_1936 = exprvar("self.net_1936")
net_1629 = exprvar("self.net_1629")
net_1472 = exprvar("self.net_1472")
net_2461 = exprvar("self.net_2461")
net_2154 = exprvar("self.net_2154")
net_1905 = exprvar("self.net_1905")
net_1815 = exprvar("self.net_1815")
net_1928 = exprvar("self.net_1928")
net_2479 = exprvar("self.net_2479")
net_2004 = exprvar("self.net_2004")
net_1907 = exprvar("self.net_1907")
net_1822 = exprvar("self.net_1822")

_net_2949 = exprvar("self._net_2949")
_net_2609 = exprvar("self._net_2609")
_net_2676 = exprvar("self._net_2676")
_net_2689 = exprvar("self._net_2689")
_net_2826 = exprvar("self._net_2826")
_net_2674 = exprvar("self._net_2674")
_net_2743 = exprvar("self._net_2743")
_net_2752 = exprvar("self._net_2752")


# fmt: off
sync = [
    ("self._net_2949", (((enable) & (_net_2674)) | ((_net_2949) & (~((output_enable) | (enable)))) | (~((~(~(enable) & (output_enable))) | (~((_net_2676) ^ ((_net_2609) ^ (_net_2743)))))))),
    ("self._net_2609", (((_net_2609) | ((output_enable) | (enable))) & ((~((enable) | (~((_net_2674) ^ ((_net_2609) ^ (_net_2949)))) | ~(~((~((_net_2752) ^ (_net_2609))) ^ (~((_net_2826) ^ (_net_2743))))))) | ((((enable) & (_net_2689)) | ((~((enable) | (~((~((_net_2752) ^ (_net_2609))) ^ (~((_net_2826) ^ (_net_2743))))))) & (~((_net_2674) ^ ((_net_2609) ^ (_net_2949))))) | (~((output_enable) | (enable)))))))),
    ("self._net_2676", (((~(enable) & (output_enable)) & (~((_net_2689) & (~((_net_2676) ^ (~((_net_2752) ^ (_net_2609))))))) & ((_net_2689) | (~((_net_2676) ^ (~((_net_2752) ^ (_net_2609))))))) | ((((enable) & (_net_2826)) | ((~((output_enable) | (enable))) & (_net_2676)))))),
    ("self._net_2689", (((~((_net_2674) ^ (~((_net_2676) ^ (~((_net_2752) ^ (_net_2609)))))) & (~((enable) | (~((~((_net_2752) ^ (_net_2609))) ^ (~((_net_2826) ^ (_net_2743)))))))) | (~(enable) & (~((~((_net_2752) ^ (_net_2609))) ^ (~((_net_2826) ^ (_net_2743))))) & ((_net_2674) ^ (~((_net_2676) ^ (~((_net_2752) ^ (_net_2609))))))) | ((((enable) & (_net_2949)) | (~((output_enable) | (enable)))))) & (((output_enable) | (enable)) | (_net_2689)))),
    ("self._net_2826", (((~(enable) & (output_enable)) & (~((~((_net_2689) ^ (_net_2826))) ^ ((_net_2609) ^ (_net_2949))))) | ((((enable) & (_net_2752)) | ((_net_2826) & (~((output_enable) | (enable)))))))),
    ("self._net_2674", (((_net_2674) | ((output_enable) | (enable))) & ((~(~(enable) & (output_enable))) | (~((_net_2676) ^ (~((_net_2689) ^ (_net_2826)))))) & (~(((I) | (~((~((_net_2752) ^ (_net_2609))) ^ (~((_net_2826) ^ (_net_2743)))))) & (~(((I) & (~((~((_net_2752) ^ (_net_2609))) ^ (~((_net_2826) ^ (_net_2743)))))) | (~(enable)))))))),
    ("self._net_2743", (((enable) & (_net_2676)) | ((_net_2743) & (~((output_enable) | (enable)))) | (~((~((~((_net_2752) ^ (_net_2609))) ^ (~((_net_2826) ^ (_net_2743))))) | (~(~(enable) & (output_enable))))))),
    ("self._net_2752", (((enable) & (_net_2609)) | ((~((output_enable) | (enable))) & (_net_2752)) | (((((_net_2689) ^ (_net_2949)) | ((_net_2674) ^ (_net_2752))) & (~((((_net_2689) ^ (_net_2949)) & ((_net_2674) ^ (_net_2752))) | (~(~(enable) & (output_enable))))))))),
]

comb = [
    ("self.O[0]", (((~((~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1]))))) | ((((net_2232) & (~((message_select[1]) | (message_select[2]) | ~(message_select[0])))) | ((~((message_select[1]) | (message_select[0]) | (message_select[2]))) & (net_2006)))) | ((((~((_net_2674) ^ (~(((~((char_index[2]) & (~(char_index[0]) & (char_index[1])))) & (~((char_index[1]) & (char_index[3])))) | (~((char_index[0]) | (~(char_index[3])))))))) & (~((message_select[0]) | (message_select[2]) | ~(message_select[1])))) | ((~((message_select[1]) | (message_select[0]) | ~(message_select[2]))) & (net_1559))))) & ((net_1816) | (~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1])))))),
    ("self.O[1]", (((~((~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1]))))) | ((((net_2315) & (~((message_select[1]) | (message_select[2]) | ~(message_select[0])))) | ((~((message_select[1]) | (message_select[0]) | (message_select[2]))) & (net_2088)))) | ((((~(((~((char_index[0]) | (~(char_index[3])))) | (~((char_index[0]) | (char_index[1]))) | (~((char_index[2]) | (char_index[3])))) ^ ((_net_2949) ^ ((char_index[1]) | (char_index[2]))))) & (~((message_select[0]) | (message_select[2]) | ~(message_select[1])))) | ((~((message_select[1]) | (message_select[0]) | ~(message_select[2]))) & (net_1420))))) & ((net_1822) | (~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1])))))),
    ("self.O[2]", (((~((~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1]))))) | ((((net_2313) & (~((message_select[1]) | (message_select[2]) | ~(message_select[0])))) | ((~((message_select[1]) | (message_select[0]) | (message_select[2]))) & (net_1977)))) | ((((~((_net_2689) ^ (~(((~(~((char_index[2]) & (~(char_index[0]) & (char_index[1]))))) | (~(((char_index[1]) | (char_index[2])) & (~((char_index[3]) ^ ((char_index[0]) & (char_index[1]) & (char_index[2]))))))) & ((((char_index[0]) & (char_index[2])) | (~(char_index[3])) | (~(char_index[0]) & (char_index[1])))))))) & (~((message_select[0]) | (message_select[2]) | ~(message_select[1])))) | ((~((message_select[1]) | (message_select[0]) | ~(message_select[2]))) & (net_1694))))) & ((net_1907) | (~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1])))))),
    ("self.O[3]", (((~((~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1]))))) | ((((net_2460) & (~((message_select[1]) | (message_select[2]) | ~(message_select[0])))) | ((~((message_select[1]) | (message_select[0]) | (message_select[2]))) & (net_2117)))) | (((((_net_2609) ^ ((((~(~((char_index[2]) & (~(char_index[0]) & (char_index[1]))))) | (~((char_index[3]) ^ ((char_index[0]) & (char_index[1]) & (char_index[2])))) | (~((char_index[2]) | (~(~((char_index[0]) | (char_index[1]))) & (~((char_index[0]) & (char_index[1]))))))) & ((~(~((char_index[0]) | (char_index[1]))) & (~((char_index[0]) & (char_index[1])))) | (~(((char_index[1]) | (char_index[2])) & (~((char_index[3]) ^ ((char_index[0]) & (char_index[1]) & (char_index[2])))))))))) & (~((message_select[0]) | (message_select[2]) | ~(message_select[1])))) | ((~((message_select[1]) | (message_select[0]) | ~(message_select[2]))) & (net_1516))))) & ((net_1936) | (~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1])))))),
    ("self.O[4]", (((~((~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1]))))) | ((((net_2240) & (~((message_select[1]) | (message_select[2]) | ~(message_select[0])))) | ((~((message_select[1]) | (message_select[0]) | (message_select[2]))) & (net_2189)))) | (((((_net_2752) ^ ((((char_index[2]) | (~((char_index[0]) | (~(char_index[3])))) | (~(char_index[0]) & (char_index[1]))) & (~((char_index[1]) & (char_index[3])))))) & (~((message_select[0]) | (message_select[2]) | ~(message_select[1])))) | ((~((message_select[1]) | (message_select[0]) | ~(message_select[2]))) & (net_1472))))) & ((net_1927) | (~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1])))))),
    ("self.O[5]", (((~((~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1]))))) | ((((net_2298) & (~((message_select[1]) | (message_select[2]) | ~(message_select[0])))) | ((~((message_select[1]) | (message_select[0]) | (message_select[2]))) & (net_2120)))) | (((((_net_2826) ^ (~((~(~(char_index[1]) & (char_index[0]))) & ((((~((char_index[0]) | (~(char_index[3])))) & ((char_index[1]) | (char_index[2]))) | ((~((char_index[3]) ^ ((char_index[0]) & (char_index[1]) & (char_index[2])))) & ((char_index[0]) | (char_index[2]) | ~(char_index[1])))))))) & (~((message_select[0]) | (message_select[2]) | ~(message_select[1])))) | ((~((message_select[1]) | (message_select[0]) | ~(message_select[2]))) & (net_1693))))) & ((net_1905) | (~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1])))))),
    ("self.O[6]", (((~((~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1]))))) | ((((net_2461) & (~((message_select[1]) | (message_select[2]) | ~(message_select[0])))) | ((~((message_select[1]) | (message_select[0]) | (message_select[2]))) & (net_2154)))) | ((((~((_net_2676) ^ ((((char_index[0]) & (~((char_index[2]) | (char_index[3])))) | ((~(~(char_index[1]) & (char_index[0]))) & (char_index[2])))))) & (~((message_select[0]) | (message_select[2]) | ~(message_select[1])))) | ((~((message_select[1]) | (message_select[0]) | ~(message_select[2]))) & (net_1629))))) & ((net_1928) | (~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1])))))),
    ("self.O[7]", (((~((~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1]))))) | ((((net_2479) & (~((message_select[1]) | (message_select[2]) | ~(message_select[0])))) | ((~((message_select[1]) | (message_select[0]) | (message_select[2]))) & (net_2004)))) | ((((~((_net_2743) ^ ((((char_index[2]) & (~(char_index[3])) & (~((char_index[0]) & (char_index[1])))) | (~(((char_index[0]) & (~(char_index[3]))) | (((char_index[1]) | (char_index[2])) & (~((char_index[0]) & (char_index[1])))))))))) & (~((message_select[0]) | (message_select[2]) | ~(message_select[1])))) | ((~((message_select[1]) | (message_select[0]) | ~(message_select[2]))) & (net_1425))))) & ((net_1815) | (~((message_select[0]) | (message_select[2]) | ~(message_select[1]))) | (~(((message_select[0]) & (message_select[2])) | (message_select[1])))))),
]
# fmt: on


def print_with_assumption(exprs, assumption):
    for name, formula in exprs:
        print(F"        {name}.eq({formula.restrict(assumption)}),")

print("with m.If(~self.enable & ~self.output_enable):")
print("    m.d.sync += [")
print_with_assumption(sync, {enable: 0, output_enable: 0})
print("    ]\n")

print("with m.If(self.enable & ~self.output_enable):")
print("    m.d.sync += [")
print_with_assumption(sync, {enable: 1, output_enable: 0})
print("    ]\n")

print("with m.If(~self.enable & self.output_enable):")
print("    m.d.sync += [")
print_with_assumption(sync, {enable: 0, output_enable: 1})
print("    ]\n")

print("with m.If(self.enable & self.output_enable):")
print("    m.d.sync += [")
print_with_assumption(sync, {enable: 1, output_enable: 1})
print("    ]\n")

for i in range(8):
    print(f"with m.If(self.message_select == {i}):")
    print("    m.d.sync += [")
    print_with_assumption(comb, {message_select[bit]: (i >> bit) & 1 for bit in range(3)})
    print("    ]\n")

print("with m.If(~self.enable & self.output_enable):")
print("    m.d.sync += [")
for name, formula in sync:
    formula = formula.restrict({enable: 0, output_enable: 1})
    formula = espresso_exprs(formula.to_dnf())[0]
    if formula.equivalent(Xor(*formula.support)):
        print(f"        {name}.eq({" ^ ".join(map(str, formula.support))})")
    elif formula.equivalent(Xnor(*formula.support)):
        print(f"        {name}.eq(~({" ^ ".join(map(str, formula.support))}))")
    else:
        print(F"        {name}.eq({formula}),")
print("    ]\n")

for i in range(16):
    print(f"with m.If((self.message_select == 2) & (self.char_index == {i})):")
    print("    m.d.sync += [")
    print_with_assumption(comb, {message_select[0]: 0, message_select[1]: 1, message_select[2]: 0, **{char_index[bit]: (i >> bit) & 1 for bit in range(4)}})
    print("    ]\n")

