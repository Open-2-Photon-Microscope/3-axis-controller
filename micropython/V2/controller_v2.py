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
        
    def run(self, position=[0,0,0]):
        # position: list of current coordinates [x,y,z]
        # Controller values will start at current position
        # method returns co-ordinates to be fed into .move_to()
        
        self.step_size = self.set_step_size()
        self.x_control._incr = self.step_size*self.sf
        self.y_control._incr = self.step_size*self.sf
        self.z_control._incr = self.step_size*self.sf
        
        self.x_control.set(value = position[0])
        self.y_control.set(value = position[1])
        self.z_control.set(value = position[2])
        
        ## DISPLAY STUFF
        x_string = 'X:' + str(position[0])[:6] # Take only 5 or 6 SF
        x_string = x_string + ' '*(8-len(x_string)) # Pad string to length 8 - avoids .clear() making screen flicker
                
        y_string = 'Y:' + str(position[1])[:6]
        y_string = y_string + ' '*(8-len(y_string))
                
        z_string = 'Z:' + str(position[2])[:5]
        z_string = z_string + ' '*(7-len(z_string))
        
        # Update display screen
        self.display.set_cursor(0,0)
        self.display.print(x_string)
        self.display.set_cursor(9,0)
        self.display.print(z_string)
        self.display.set_cursor(0,1)
        self.display.print(y_string)
        self.display.set_cursor(9,1)
        self.display.print('CONTROL')
        
        
        
        accept = False
        
        old_pos = [self.x_control.value(),
                   self.y_control.value(),
                   self.z_control.value()
                   ]
        saved_pos = old_pos
        new_pos = old_pos
        time.sleep_ms(100)
        while self.start_pin.value()==0 and self.stop_pin.value()==0:
            new_pos = [self.x_control.value(),
                       self.y_control.value(),
                       self.z_control.value()
                       ]
            if old_pos != new_pos:
                old_pos = new_pos
                print('X,Y,Z:  ', new_pos)
                
                x_string = 'X:' + str(new_pos[0]/self.sf)[:6] # Take only 5 or 6 SF
                x_string = x_string + ' '*(8-len(x_string)) # Pad string to length 8 - avoids .clear() making screen flicker
                
                y_string = 'Y:' + str(new_pos[1]/self.sf)[:6]
                y_string = y_string + ' '*(8-len(y_string))
                
                z_string = 'Z:' + str(new_pos[2]/self.sf)[:5]
                z_string = z_string + ' '*(7-len(z_string))
                
                # Update display screen
                self.display.set_cursor(0,0)
                self.display.print(x_string)
                self.display.set_cursor(9,0)
                self.display.print(z_string)
                self.display.set_cursor(0,1)
                self.display.print(y_string)
                self.display.set_cursor(9,1)
                self.display.print('CONTROL')
                
            if self.start_pin.value()==1:
                accept = True
            time.sleep_ms(50)
            
        if self.start_pin.value()==1:
            accept = True
        if accept == True:
            return new_pos
        else:
            return saved_pos
    
    def set_step_size(self):
        self.display.clear()
        self.display.set_cursor(0,0)
        self.display.print("STEP SIZE: ")
        self.display.print(str(self.step_size))
        
        self.display.blink()
        
        proposed_size = self.step_size
        
        old_val = self.x_control.value()
        new_val = old_val
        time.sleep_ms(300)
        
        while self.start_pin.value()==0 and self.stop_pin.value()==0:
            self.x_control._incr = 1
            new_val = self.x_control.value()
            if old_val != new_val:
                old_val = new_val
                proposed_size = self.step_presets[new_val % len(self.step_presets)]
                print('Step size: ', proposed_size)
                self.display.set_cursor(11,0)
                self.display.print('         ')
                self.display.set_cursor(11,0)
                self.display.print(str(proposed_size))
                
        if self.start_pin.value() == 1:
            print('New size: ', proposed_size)
            time.sleep_ms(300)
            self.display.clear()
            return proposed_size
        
        if self.stop_pin.value() == 1:
            print('Rejected new size')
            time.sleep_ms(300)
            self.display.clear()
            return self.step_size

c = controller()
        
#c.set_step_size()