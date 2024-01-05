import time
from machine import Pin
from ir_rx.apple import APPLE

buttons = [0, 1, "MENU", 3, "PLAY", 5, 6, ">>", "<<", 9, 10, "+", 12, "-"]


def callback(data, addr, ctrl):
    if data < 0 or data == 6:
        pass
    else:
        try:
            print(buttons[data])
        except:
            print(f"data: {data}")
            pass


ir = APPLE(Pin(5, Pin.IN), callback)

print("waiting for IR signal")
while True:
    time.sleep_ms(500)
