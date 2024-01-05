# apple.py Decoder for Apple Remote A1156
# https://en.wikipedia.org/wiki/Apple_Remote

# Author: Pax
# Copyright Peter Hinch 2020-2022 Released under the MIT license
# Version 1.0.1

from utime import ticks_diff
from ir_rx import IR_RX


class APPLE_ABC(IR_RX):
    def __init__(self, pin, extended, callback, *args):
        super().__init__(pin, 68, 80, callback, *args)
        self._extended = extended
        self._addr = 0
        self._leader = 9000

    def decode(self, _):
        try:
            if self.edge > 68:
                raise RuntimeError(self.OVERRUN)
            width = ticks_diff(self._times[1], self._times[0])
            if width < self._leader:
                raise RuntimeError(self.BADSTART)
            width = ticks_diff(self._times[2], self._times[1])
            if width > 2250:
                if self.edge < 68:
                    raise RuntimeError(self.BADBLOCK)
                val = 0
                for edge in range(3, 68 - 2, 2):
                    val >>= 1
                    if ticks_diff(self._times[edge + 1], self._times[edge]) > 1120:
                        val |= 0x80000000
            elif width > 1700:
                raise RuntimeError(self.REPEAT if self.edge == 4 else self.BADREP)
            else:
                raise RuntimeError(self.BADSTART)
            addr = val & 0xFF
            cmd = (val >> 16) & 0xFF

            if addr != ((val >> 8) ^ 0xFF) & 0xFF:
                if not self._extended:
                    raise RuntimeError(self.BADADDR)
                addr |= val & 0xFF00
            self._addr = addr
        except RuntimeError as e:
            cmd = e.args[0]
            addr = self._addr if cmd == self.REPEAT else 0

        self.do_callback(cmd, addr, 0, self.REPEAT)


class APPLE(APPLE_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, True, callback, *args)
