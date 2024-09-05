# set motor pins to 0 on boot
from machine import Pin



def set_pins(pins=[15,20,4, 16,17,5,18, 19,21,22,23], value=0):
    for pin_n in pins:
        pin = Pin(pin_n, Pin.OUT, Pin.PULL_DOWN)
        pin.value(value)
        
def read_pins(pins_to_read = [15,20,4, 16,17,5,18, 19,21,22,23]):

    # Initialize pins as inputs
    pins = [Pin(pin_number, Pin.IN) for pin_number in pins_to_read]

    # Read and print the value of each pin
    for pin in pins:
        pin_value = pin.value()  # Read the digital value (0 or 1)
        print(f"Pin {pin} value: {pin_value}")
