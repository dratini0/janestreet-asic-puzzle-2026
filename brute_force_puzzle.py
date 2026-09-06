#!/usr/bin/env python3


def step8(state):
    for _ in range(8):
        state = (
            state << 1 | ((state >> 3) ^ (state >> 4) ^ (state >> 5) ^ (state >> 7)) & 1
        ) & 0xFF
    return state


obfustcated = [
    0x4D,
    0xAD,
    0xFB,
    0x83,
    0x13,
    0x79,
    0x1C,
    0xB5,
    0x79,
    0x63,
    0xC7,
    0x68,
    0x93,
    0xF5,
    0x8F,
    # 0x0, # this is blocked by the output controller anyway
]

step8_table = [step8(i) for i in range(256)]

for initial in range(256):
    keystream = [initial]
    for _ in range(15):
        keystream.append(step8_table[keystream[-1]])

    decrypted = bytes(i ^ j for i, j in zip(keystream, obfustcated))

    if not any(i & 0x80 for i in decrypted):
        print(decrypted.decode())
