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
                 end_c=12,
                 back_a=0,
                 back_b=0,
                 back_c=0):
        
        self.motor_a = motor_a
        self.motor_b = motor_b
        self.motor_c = motor_c
        
        #which pcf pins
        self.end_a = end_a
        self.end_b = end_b
        self.end_c = end_c
        
        #backlash
        self.back_a = back_a
        self.back_b = back_b
        self.back_c = back_c
        
        self.i2c = I2C(0,sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.pcf = pcf8575.PCF8575(self.i2c, 0x20)
        self.pcf.port = 0xFFFF # pull all pins up
        
        #values of endstops (1=open, 0=closed)
        self.a = self.pcf.pin(end_a)
        self.b = self.pcf.pin(end_b)
        self.c = self.pcf.pin(end_c)
        
        self.irq_pin = Pin(irq_pin, Pin.IN, Pin.PULL_UP)
        self.irq_pin.irq(trigger=Pin.IRQ_FALLING, handler=self._handler)
        
    def _handler(self,p):
        print(f'A:{self.pcf.pin(self.end_a)}\nB:{self.pcf.pin(self.end_b)}\nC:{self.pcf.pin(self.end_c)}')
        #just freeze all motors until reactivated by zeroing
        if 0 in [self.pcf.pin(self.end_a),self.pcf.pin(self.end_b),self.pcf.pin(self.end_c)]:
            self.motor_a.stop()
            self.motor_b.stop()
            self.motor_c.stop()
            self.a = self.motor_a.functional_multiplier = 0
            self.b = self.motor_b.functional_multiplier = 0
            self.c = self.motor_c.functional_multiplier = 0
    
    def activate_irq(self, default=True):
        if default == True:
            self.irq_pin.irq(trigger = Pin.IRQ_FALLING, handler = self._handler)
        elif default == False:
            self.irq_pin.irq(trigger = Pin.IRQ_FALLING, handler = self._zero_handler)
        
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
        #enable or disable motors
        self.a = self.motor_a.functional_multiplier = self.pcf.pin(self.end_a)
        self.b = self.motor_b.functional_multiplier = self.pcf.pin(self.end_b)
        self.c = self.motor_c.functional_multiplier = self.pcf.pin(self.end_c)
    
    def zero(self, return_to_normal=True, backlash=False):
        self.motor_a.functional_multiplier = 1
        self.motor_b.functional_multiplier = 1
        self.motor_c.functional_multiplier = 1
        
        self.a = self.pcf.pin(self.end_a)
        self.b = self.pcf.pin(self.end_b)
        self.c = self.pcf.pin(self.end_c)
        
        if backlash == True:
            self.motor_a.backlash = 0
            self.motor_b.backlash = 0
            self.motor_c.backlash = 0
        
        print(f'a = {self.a}\nb = {self.b}\nc = {self.c}')
        if backlash == False:
            print('Begin zero!')
        if backlash == True:
            print('Begin backlash')
        #raise motors
        self.irq_pin.irq(None)
        #regardless of endstop state, raising motors will set backlash in the correct direction
        self.motor_a.run(1000)
        self.motor_b.run(1000)
        self.motor_c.run(1000)
        while self.pcf.pin(self.end_a) == 0 or self.pcf.pin(self.end_b) == 0 or self.pcf.pin(self.end_c) == 0:
            if self.pcf.pin(self.end_a) != 1 and self.motor_a._run_remaining ==0:
                self.motor_a.run(5000)
            if self.pcf.pin(self.end_b) != 1 and self.motor_b._run_remaining ==0:
                self.motor_b.run(5000)
            if self.pcf.pin(self.end_c) != 1 and self.motor_c._run_remaining ==0: 
                self.motor_c.run(5000)
            sleep_ms(50)
        print('Motors raised')
        
        #lower motors until interrupt
        self.activate_irq(default=False) # enable secondary irq
        print('Lowering motors')
        while self.pcf.pin(self.end_a) == 1 or self.pcf.pin(self.end_b) == 1 or self.pcf.pin(self.end_c) == 1:
            if self.pcf.pin(self.end_a) != 0 and self.motor_a._run_remaining ==0:
                self.motor_a.run(-5000)
            if self.pcf.pin(self.end_b) != 0 and self.motor_b._run_remaining ==0:
                self.motor_b.run(-5000)
            if self.pcf.pin(self.end_c) != 0 and self.motor_c._run_remaining ==0: 
                self.motor_c.run(-5000)
            sleep_ms(50)
        
        self.irq_pin.irq(None)
        
        if backlash == False:
            print('Raising motors again')
            self.motor_a.functional_multiplier = self.motor_b.functional_multiplier = self.motor_c.functional_multiplier = 1
            while self.pcf.pin(self.end_a) == 0 or self.pcf.pin(self.end_b) == 0 or self.pcf.pin(self.end_c) == 0:
                if self.pcf.pin(self.end_a) != 1 and self.motor_a._run_remaining ==0:
                    self.motor_a.run(5000)
                if self.pcf.pin(self.end_b) != 1 and self.motor_b._run_remaining ==0:
                    self.motor_b.run(5000)
                if self.pcf.pin(self.end_c) != 1 and self.motor_c._run_remaining ==0: 
                    self.motor_c.run(5000)
                sleep_ms(50)
            print('Motors raised')
            while self.motor_a._run_remaining != 0 or self.motor_b._run_remaining != 0 or self.motor_c._run_remaining != 0:
                sleep_ms(100)
            print('Finished zero!')
        
        if backlash == True:
            #note the movement differential (MD) for the switch is 0.5mm
            #now I just need to calculate how much vertical travel per step I'm dealing with
            print('Calculating backlash')
            self.back_a = 0
            self.back_b = 0
            self.back_c = 0
            self.motor_a.functional_multiplier = self.motor_b.functional_multiplier = self.motor_c.functional_multiplier = 1
            while self.pcf.pin(self.end_a) == 0 or self.pcf.pin(self.end_b) == 0 or self.pcf.pin(self.end_c) == 0:
                if self.pcf.pin(self.end_a) == 0 and self.motor_a._run_remaining ==0:
                    self.motor_a.run(20)
                    self.back_a += 1
                if self.pcf.pin(self.end_b) != 1 and self.motor_b._run_remaining ==0:
                    self.motor_b.run(20)
                    self.back_b += 1
                if self.pcf.pin(self.end_c) != 1 and self.motor_c._run_remaining ==0: 
                    self.motor_c.run(20)
                    self.back_c += 1
                sleep_ms(10)
            print(f'Backlash values are:\nA:{self.back_a}\nB:{self.back_b}\nC:{self.back_c}')
            self.activate_irq()
            return [self.back_a, self.back_b, self.back_c]
        
        if return_to_normal == True:
            self.motor_a.run(5000)
            self.motor_b.run(5000)
            self.motor_c.run(5000)
            self.activate_irq()
        return
            
if __name__ == '__main__':
    from stepper import Stepper
    motorA = Stepper(15,2,0,4,T=0)
    motorB = Stepper(16,17,5,18,T=1)
    motorC = Stepper(19,21,22,23,T=2)
    e = Endstops(motorA, motorB, motorC)
    e.zero()