import time
from rotary_irq_esp import RotaryIRQ
from machine import Pin
from screen import lcd


class controller():
    def __init__(self,
                 start_pin=Pin(36,Pin.IN),
                 stop_pin=Pin(39,Pin.IN),
                 display=lcd,
                 scale_factor=2
                 ):
        self.start_pin = start_pin
        self.stop_pin = stop_pin
        self.display = display
        self.sf = scale_factor # how many steps per um
        
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
                                    reverse=False, 
                                    range_mode=RotaryIRQ.RANGE_UNBOUNDED)
        
    def run(self, position=[0,0,0]):
        # position: list of current coordinates [x,y,z]
        # Controller values will start at current position
        # method returns co-ordinates to be fed into .move_to()
        # co-ordinates will either be 
        self.x_control.set(value = position[0])
        self.y_control.set(value = position[1])
        self.z_control.set(value = position[2])
        
        accept = False
        
        old_pos = [self.x_control.value(),
                   self.y_control.value(),
                   self.z_control.value()
                   ]
        saved_pos = old_pos
        new_pos = old_pos
        time.sleep_ms(300)
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
            

c = controller()
        
        