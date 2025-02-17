from machine import Pin, I2C
import pcf8575
from time import sleep_ms

class Endstops():
    def __init__(self, motor_a,
                 motor_b,
                 motor_c,
                 sda_pin=32,
                 scl_pin=33,
                 irq_pin=13,
                 end_a=10,
                 end_b=11,
                 end_c=12):
        
        self.motor_a = motor_a
        self.motor_b = motor_b
        self.motor_c = motor_c
        
        #which pcf pins
        self.end_a = end_a
        self.end_b = end_b
        self.end_c = end_c
        
        #values of endstops (1=open, 0=closed)
        self.a = 1
        self.b = 1
        self.c = 1
        
        self.i2c = I2C(0,sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.pcf = pcf8575.PCF8575(self.i2c, 0x20)
        self.pcf.port = 0xFFFF # pull all pins up
        
        self.irq_pin = Pin(irq_pin, Pin.IN, Pin.PULL_UP)
        self.irq_pin.irq(trigger=Pin.IRQ_FALLING, handler=self._handler)
        
    def _handler(self,p):
        if self.pcf.pin(self.end_a) != 1:
            self.motor_a.stop()
            print('A', end=' ')
        if self.pcf.pin(self.end_b) != 1:
            self.motor_b.stop()
            print('B', end=' ')
        if self.pcf.pin(self.end_c) != 1:
            self.motor_c.stop()
            print('C',end='')
        print()
        #enable or disable motors
        self.a = self.motor_a.functional_multiplier = self.pcf.pin(self.end_a)
        self.b = self.motor_b.functional_multiplier = self.pcf.pin(self.end_b)
        self.c = self.motor_c.functional_multiplier = self.pcf.pin(self.end_c)
    
    def activate_irq(self):
        self.irq_pin.irq(trigger=Pin.IRQ_FALLING, handler=self._handler)
        
    def _zero_handler(self,p):
        if self.pcf.pin(self.end_a) != 1:
            self.motor_a.stop()
            print('A', end=' ')
        if self.pcf.pin(self.end_b) != 1:
            self.motor_b.stop()
            print('B', end=' ')
        if self.pcf.pin(self.end_c) != 1:
            self.motor_c.stop()
            print('C',end='')
        print()
    
    def zero(self):
        self.motor_a.functional_multiplier = 1
        self.motor_b.functional_multiplier = 1
        self.motor_c.functional_multiplier = 1
        #self.irq_pin.irq(None) # disable irq
        
        #raise motors
        while self.pcf.port != 65535:
            if self.a != 1:
                self.motor_a.run(5000)
            if self.b != 1:
                self.motor_b.run(5000)
            if self.c != 1:
                self.motor_c.run(5000)
        
        #lower motors until interrupt
        self.motor_a.run(-500000)
        self.motor_b.run(-500000)
        self.motor_c.run(-500000)
        
        print(self.pcf.port, 'should be 65535')
            
if __name__ == '__main__':
    from stepper import Stepper
    motorA = Stepper(15,2,0,4,T=0)
    motorB = Stepper(16,17,5,18,T=1)
    motorC = Stepper(19,21,22,23,T=2)
    e = Endstops(motorA, motorB, motorC)