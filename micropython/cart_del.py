# cartesian to delta conversion

import umatrix
import screen
import time
from ulinalg import det_inv, dot
from math import sqrt
from machine import Pin
from stepper import Stepper
from controller_v2 import controller
from endstops_v2 import Endstops

class Stage():
    
    def __init__(self, X_pos=0, Y_pos=0, Z_pos=0, skip_init=False):
        # Position values can be preset if needed
        self.X_pos:float = X_pos
        self.Y_pos:float = Y_pos
        self.Z_pos:float = Z_pos
        
        self.sf = 2 # scale factor ie steps per um
        
        # I2C Screen
        self.lcd = screen.lcd
        self.lcd.begin()
        
        self.x_string = 'X:     '
        self.y_string = 'Y:     '
        self.z_string = 'Z:     '
        
        # custom mu character
        self.lcd.create_char(0,[0x00,
                                0x00,
                                0x00,
                                0x11,
                                0x11,
                                0x1B,
                                0x15,
                                0x10])
        
        # Stepper motors
        self.motorA = Stepper(15,2,0,4,T=0)
        self.motorB = Stepper(16,17,5,18,T=1)
        self.motorC = Stepper(19,21,22,23,T=2)
        
        self.endstops = Endstops(self.motorA, self.motorB, self.motorC)
        
        # Rotary encoders + relevant buttons
        self.start_pin = Pin(36,Pin.IN)
        self.stop_pin = Pin(39,Pin.IN)
        
        self.c = controller(self.start_pin,
                            self.stop_pin,
                            self.lcd,
                            skip_init = skip_init)
        
        # DELTA GEOMETRY HANDLING
        # unedited values from https://gitlab.com/openflexure/openflexure-microscope-server/-/blob/master/openflexure_microscope/stage/sanga.py?ref_type=heads
        # see page https://openflexure.discourse.group/t/delta-stage-geometry/628/2
        flex_a = 35
        flex_b = 47
        flex_h = 70
        self.x_fac: float = -1 * ((2 / sqrt(3)) * (flex_b / flex_h))
        self.y_fac: float = -1 * (flex_b / flex_a)
        self.z_fac: float = (1 / 3) * (flex_b / flex_a)
        
        # Matrix for Delta to Cartesian
        self.d2c = umatrix.matrix([
                        [-self.x_fac, self.x_fac, 0],
                        [0.5 * self.y_fac, 0.5 * self.y_fac, -self.y_fac],
                        [self.z_fac, self.z_fac, self.z_fac],
                        ])
        # Matrix for Cartesian to Delta
        self.c2d = det_inv(self.d2c)[1]
        self.update_pos([X_pos,Y_pos,Z_pos], update=True)
        
    def move_rel(self,vector:list):
        # relative movement vector in the form [X, Y, Z] to be given by another function
        # convert to [[X],[Y],[Z]] for matrix shape
        cart_vector = [[vector[0]],
                       [vector[1]],
                       [vector[2]]]
        
        cart_vector = umatrix.matrix(cart_vector)
        
        # Convert cartesian to delta
        delta_vector = dot(self.c2d, cart_vector) # Should return motor vector [A, B, C]
        
        # Values to be given to stepper motors
        rounded_vector = delta_vector.apply(round)
        
        # do the move
        self.motorA.run(rounded_vector.data[0])
        self.motorB.run(rounded_vector.data[1])
        self.motorC.run(rounded_vector.data[2])
        
        # Real movement given by stepper motion
        position_vector = dot(self.d2c, rounded_vector)
        
        self.update_pos(position_vector.data)
        
        return position_vector.data # returns actual distance moved
        
    def move_to(self, vector):
        # vector: list [X, Y, Z]
        # Take difference from current position and use as movement vector in move_rel
        dX = vector[0] - self.X_pos
        dY = vector[1] - self.Y_pos
        dZ = vector[2] - self.Z_pos
        self.move_rel([dX, dY, dZ])
        return
    
    def update_pos(self, vector=[0,0,0], update=False):
        # vector: list [X, Y, Z]
        self.X_pos += vector[0]
        self.Y_pos += vector[1]
        self.Z_pos += vector[2]
        
        clr = '        '
            
        if vector[0] != 0 or update == True:
            print_x = self.X_pos / self.sf
            self.x_string = 'X:' + str(print_x)[:6]
            self.x_string = self.x_string + ' '*(len(self.x_string)-8)
            
            self.lcd.set_cursor(2,0)
            self.lcd.print(clr[:6])
            self.lcd.set_cursor(0,0)
            self.lcd.print(self.x_string)
        
        if vector[1] != 0 or update == True:
            print_y = self.Y_pos / self.sf
            self.y_string = 'Y:' + str(print_y)[:6]
            self.y_string = self.y_string + ' '*(len(self.y_string)-8)
            
            self.lcd.set_cursor(2,1)
            self.lcd.print(clr)
            self.lcd.set_cursor(0,1)
            self.lcd.print(self.y_string)
            self.lcd.print(chr(0))
            self.lcd.print('M')
            
            
        
        if vector[2] != 0 or update == True:
            print_z = self.Z_pos / self.sf
            self.z_string = 'Z:' + str(print_z)[:5]
            # this is hoping that z doesn't get too large for readability
            self.z_string = self.z_string + ' '*(len(self.z_string)-7)
            
            self.lcd.set_cursor(11,0)
            self.lcd.print(clr)
            self.lcd.set_cursor(9,0)
            self.lcd.print(self.z_string)
        
        
        #print(f'({self.c.step_size})')
        self.lcd.set_cursor(11,1)
        self.lcd.print(f'({self.c.step_size})')
        return
    
    def zero(self):
        # provide option to zero
        self.lcd.set_cursor(9,1)
        self.lcd.print('##Zero?')
        time.sleep_ms(500)
        
        while self.stop_pin.value() == 0 and self.start_pin.value() == 0:
            time.sleep_ms(50)
            
        if self.start_pin.value() == 1: #accept zero
            self.X_pos = 0
            self.Y_pos = 0
            self.Z_pos = 0
            self.update_pos()
            time.sleep_ms(300)
            
        else: # decline zero
            self.update_pos(update=True)
        
        
    def tune(self, vector):
        # vector for motor movements [A, B, C]
        # does not affect position - possibly worth doing a zero() but not always...
        self.motorA.run(vector[0])
        self.motorB.run(vector[1])
        self.motorC.run(vector[2])

    def live_move(self, cycles=50, ms=5):
        steps_taken = [0,0,0]
        
        # both buttons breaks loop
        while self.stop_pin.value() == 0 or self.start_pin.value() == 0:
            vector = self.c.live_read(cycles, ms, steps_taken)
            steps_taken = self.move_rel(vector)
            print(steps_taken)
            print('position = ', [self.X_pos, self. Y_pos, self.Z_pos])
            
            if self.stop_pin.value() == 1 and self.start_pin.value() == 0:
                self.zero()
                self.update_pos(update=True)
            if self.start_pin.value() == 1 and self.stop_pin.value() == 0:
                time.sleep_ms(100)
                self.c.set_step_size()
                self.update_pos(update=True)
        
        print('Both buttons pressed')     
        self.lcd.set_cursor(11,1)
        self.lcd.print('#STOP')
    
    def _switch_handler(self, p):
        self.stop_pin.irq(None)
        self.start_pin.irq(None)
        self.motorA.stop()
        self.motorB.stop()
        self.motorC.stop()
    
    def enable_switches(self):
        self.stop_pin.irq(trigger=Pin.IRQ_RISING, handler=self._switch_handler)
        self.start_pin.irq(trigger=Pin.IRQ_RISING, handler=self._switch_handler)

    def smooth_move(self):
        self.c.x_control.reset()
        self.c.y_control.reset()
        self.c.z_control.reset()
        self.enable_switches()
        vector = []
        
        while self.stop_pin.value() == 0 or self.start_pin.value() == 0:
            vector = [self.c.x_control.value(),
                  self.c.y_control.value(),
                  self.c.z_control.value()]
            if vector != [0,0,0]:
                self.move_rel(vector)
                vector = [0,0,0]
                self.c.x_control.reset()
                self.c.y_control.reset()
                self.c.z_control.reset()
            time.sleep_ms(100)
        
            if self.stop_pin.value() == 1 and self.start_pin.value() == 0:
                    self.zero()
                    self.update_pos(update=True)
            if self.start_pin.value() == 1 and self.stop_pin.value() == 0:
                time.sleep_ms(100)
                self.c.set_step_size()
                self.update_pos(update=True)
        print('Both buttons pressed')     
        self.lcd.set_cursor(11,1)
        self.lcd.print('#STOP')
                

if __name__ == '__main__':
    stage = Stage()
    stage.smooth_move()
