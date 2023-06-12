import Stepper

from machine import Pin
'''
IN1 -->  16
IN2 -->  17
IN3 -->  5
IN4 -->  18
'''
s1 = Stepper.create(mode= "HALF_STEP",
                    pin1=Pin(16,Pin.OUT),
                    pin2=Pin(17,Pin.OUT),
                    pin3=Pin(5,Pin.OUT),
                    pin4=Pin(18,Pin.OUT),
                    delay=5)

s1.step(100)