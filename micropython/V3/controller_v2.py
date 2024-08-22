import time
from rotary_irq_esp import RotaryIRQ
from machine import Pin
from screen import lcd


class controller():
    def __init__(self,
                 start_pin=Pin(36,Pin.IN),
                 stop_pin=Pin(39,Pin.IN),
                 display=lcd,
                 scale_factor=2,
                 step_size=0.5
                 ):
        self.start_pin = start_pin
        self.stop_pin = stop_pin
        self.display = display
        self.sf = scale_factor # how many steps per um
        self.step_size = step_size # how many steps per tick of encoder
        
        self.step_presets = [0.5, 1, 5, 10, 50, 100, 250]
        
        self.x_control = RotaryIRQ(pin_num_clk=34, 
                                    pin_num_dt=35, 
                                    min_val=0, 
                                    max_val=10000, 
                                    reverse=False, 
                                    range_mode=RotaryIRQ.RANGE_UNBOUNDED)
        
        self.y_control = RotaryIRQ(pin_num_clk=25, 
                                    pin_num_dt=26, 
                                    min_val=0, 
                                    max_val=10000, 
                                    reverse=False, 
                                    range_mode=RotaryIRQ.RANGE_UNBOUNDED)
        
        self.z_control = RotaryIRQ(pin_num_clk=27, 
                                    pin_num_dt=14, 
                                    min_val=0, 
                                    max_val=10000, 
                                    reverse=True, 
                                    range_mode=RotaryIRQ.RANGE_UNBOUNDED)
        
        self.step_size = 0.5
        self.set_step_size()
        


    def set_step_size(self):
        self.display.clear()
        self.display.set_cursor(0,0)
        self.display.print("STEP SIZE: ")
        self.display.print(str(self.step_size))
        
        #self.display.blink()
        
        proposed_size = self.step_size
        
        old_val = self.x_control.value()
        new_val = old_val
        time.sleep_ms(500)
        self.x_control._incr = 1
        
        while self.start_pin.value()==0 and self.stop_pin.value()==0:
            new_val = self.x_control.value()
            if old_val != new_val:
                old_val = new_val
                proposed_size = self.step_presets[new_val % len(self.step_presets)]
                print('Step size: ', proposed_size)
                self.display.set_cursor(11,0)
                self.display.print('         ')
                self.display.set_cursor(11,0)
                self.display.print(str(proposed_size))
                time.sleep_ms(200)
        
        self.step_size = proposed_size
        self.x_control._incr = self.step_size*self.sf
        self.y_control._incr = self.step_size*self.sf
        self.z_control._incr = self.step_size*self.sf
        
        print('New size: ', proposed_size)
        self.x_control.set(value = 0)
        time.sleep_ms(300)
        self.display.clear()
    
    
    
    def live_read(self, cycles, ms=10, steps_taken=[0,0,0]):
        # only reset value if no step was taken prior
        if steps_taken[0] != 0:
            self.x_control.set(value = 0)
        if steps_taken[1] != 0:
            self.y_control.set(value = 0)
        if steps_taken[2] != 0:
            self.z_control.set(value = 0)
        
        old_pos = [self.x_control.value(),
                   self.y_control.value(),
                   self.z_control.value()]
        
        for i in range(cycles):
            new_pos = [self.x_control.value(),
                       self.y_control.value(),
                       self.z_control.value()]
            
            if new_pos != old_pos:
                old_pos = new_pos
                print('X,Y,Z:  ', new_pos)
            
            time.sleep_ms(ms)
        
        return new_pos

#c = controller()