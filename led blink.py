import machine
import time

pin = machine.Pin(2, machine.Pin.OUT)

while True:
    pin.on()
    time.sleep_ms(1000)
    pin.off()
    time.sleep_ms(1000)
