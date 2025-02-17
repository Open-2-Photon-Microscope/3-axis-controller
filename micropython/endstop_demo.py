# endstop demo
import time
import asyncio
from rotary_irq_esp import RotaryIRQ
from machine import Pin, I2C
#from screen import lcd
from stepper import Stepper
import pcf8575

#input
x_control = RotaryIRQ(pin_num_clk=34, 
                                    pin_num_dt=35, 
                                    min_val=0, 
                                    max_val=10000, 
                                    reverse=False, 
                                    range_mode=RotaryIRQ.RANGE_UNBOUNDED)
#motor (duh)
motor = Stepper(15,2,0,4,T=0)

# i2c gpio expander
i2c = I2C(0)
pcf = pcf8575.PCF8575(i2c, 0x20)
pcf.port = 0xFFFF # pull all pins up

def _handler(p):
    print('BEEP!')
    print(f'A: {pcf.pin(10)}')
    print(f'B: {pcf.pin(11)}')
    print(f'C: {pcf.pin(12)}')
    if pcf.pin(10) == 0:
        motor.stop()
        time.sleep(1)
        x_control.reset()

def go(motor, x_control, pcf, multiplier=1):
    print('current state: ', pcf.pin(10))
    x_control.reset()
    while True:
        if x_control.value() != 0:
            motor.run(x_control.value()*multiplier)
            print(x_control.value()*multiplier)
            x_control.reset()
            print(f'A: {pcf.pin(10)}')
            print(f'B: {pcf.pin(11)}')
            print(f'C: {pcf.pin(12)}')
        time.sleep_ms(100)

#interrupt
irq_pin = Pin(13, Pin.IN, Pin.PULL_UP)
irq_pin.irq(trigger=Pin.IRQ_FALLING, handler=_handler)

go(motor, x_control, pcf, 10)