from stepper import Stepper
from rotary_irq_esp import RotaryIRQ
from machine import Pin
import time

motorA = Stepper(15,2,0,4,T=0)

x_control = RotaryIRQ(pin_num_clk=34, 
                                    pin_num_dt=35, 
                                    min_val=0, 
                                    max_val=10000, 
                                    reverse=False, 
                                    range_mode=RotaryIRQ.RANGE_UNBOUNDED)

class proto_move():
    def __init__(self,
                 motor,
                 control,
                 break_pin=39,
                 incr=10):
        
        self.motor = motor
        self.control = control
        self.break_pin = Pin(break_pin,Pin.IN)
        #self.control._incr = incr
        self.incr = incr
    
    def go(self):
        old_pos = self.control.value()
        new_pos = old_pos
        
        time.sleep_ms(100)
        
        while self.break_pin.value() == 0:
            new_pos = self.control.value()
            if old_pos != new_pos:
                #self.motor.stop()
                self.motor.run((new_pos - old_pos)*self.incr)
                old_pos = new_pos
                print(new_pos)
    
test = proto_move(motorA, x_control)

test.go()










