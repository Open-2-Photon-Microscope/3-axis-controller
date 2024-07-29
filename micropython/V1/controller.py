from machine import Pin
from time import sleep
import Stepper

# PIN ASSIGNMENT FUNCTIONS
class controller():
    # function that assigns rotary encoders X, Y and Z channels (REC) to pins
    # NB do not use pins 1 or 3 - they are for serial comms only
    def __init__(self):
        self.motor_a = Stepper.create(mode= "HALF_STEP",
                    pin1=Pin(16,Pin.OUT),
                    pin2=Pin(17,Pin.OUT),
                    pin3=Pin(5,Pin.OUT),
                    pin4=Pin(18,Pin.OUT),
                    delay=5)
        self.motor_b = Stepper.create(mode= "HALF_STEP",
                    pin1=Pin(26,Pin.OUT),
                    pin2=Pin(25,Pin.OUT),
                    pin3=Pin(0,Pin.OUT),
                    pin4=Pin(4,Pin.OUT),
                    delay=5)
        self.motor_c = Stepper.create(mode= "HALF_STEP",
                    pin1=Pin(22,Pin.OUT),
                    pin2=Pin(23,Pin.OUT),
                    pin3=Pin(9,Pin.OUT),
                    pin4=Pin(10,Pin.OUT),
                    delay=5)        


    def pins_REC(self,pinA, pinB):
        outPinA = Pin(pinA, Pin.IN)
        outPinB = Pin(pinB, Pin.IN)
        self.outPinA = outPinA
        self.outPinB = outPinB
        return self.outPinA, self.outPinB

# MOTOR FUNCTIONS

# function that assigns motor rotations depending on translation axis
    def mov(self,vector,ctrl=1):
        # clockwise
        print(vector)
        if vector[1]=="+":
            if vector[0] == "x":
                self.motor_a.step(-7*ctrl)
                self.motor_b.step(7*ctrl)
                
            elif vector[0] == "y":
                self.motor_a.step(4*ctrl)
                self.motor_b.step(4*ctrl)
                self.motor_c.step(-8*ctrl)
                
            elif vector[0] == "z":
                self.motor_a.step(8*ctrl)
                self.motor_b.step(8*ctrl)
                self.motor_c.step(8*ctrl)
                
        # counterclockwise
        elif vector[1]=="-":
            if vector[0] == "x":
                self.motor_a.step(7*ctrl)
                self.motor_b.step(-7*ctrl)
                
            elif vector[0] == "y":
                self.motor_a.step(-4*ctrl)
                self.motor_b.step(-4*ctrl)
                self.motor_c.step(8*ctrl)
                
            elif vector[0] == "z":
                self.motor_a.step(-8*ctrl)
                self.motor_b.step(-8*ctrl)
                self.motor_c.step(-8*ctrl)
        return


# ROTARY ENCODER FUNCTION

# function that translates REC signals into motor rotations
    def REC_translation(self,axis, outPinA, outPinB, tick=0):
        oldA = outPinA.value() 
        oldB = outPinB.value()
        sleep(0.005)

        vector = axis  
        A = outPinA.value()
        B = outPinB.value()    
        A_state = A-oldA
        B_state = B-oldB
       
        # channel A / clockwise
        if  A_state == 1 and B==0:
            vector += "+"
            self.mov(vector)
            tick = 0
        # channel B / counterclockwise
        elif B_state == 1 and A==0:
            vector += "-"
            self.mov(vector)
            tick = 0
        else:
            sleep(0.001)
            tick = 1
     
        oldA = A
        oldB = B
    
        return tick


    # PROGRAM
    def run(self,runForever=False,n=1000):
        idle = 0
        # assign pins to the 3 rotary encoders channels (REC)
        xA,xB = self.pins_REC(15,2)
        yA,yB = self.pins_REC(19,21) # 16,17
        zA,zB = self.pins_REC(14,27) # 5, 18
        
        while idle < n: # timeout after n cycles unused
            if runForever == False:
                idle += 1
            # reset idle time if used
            idle = idle * self.REC_translation("x",xA,xB)
            idle = idle * self.REC_translation("y",yA,yB)
            idle = idle * self.REC_translation("z",zA,zB)
            sleep(0.001)
        print('Controller timed out from idling')
