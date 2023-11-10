from machine import Pin
from time import sleep
import Stepper

# PIN ASSIGNMENT FUNCTIONS
class controller():
    # function that assigns rotary encoders X, Y and Z channels (REC) to pins
    #        motor_a = self.pins_motor(26, 25, 14, 27)
#        motor_b = self.pins_motor(22, 23, 21, 19)
#        motor_c = self.pins_motor(1, 3, 9, 10)
    def __init__(self):
        self.motor_a = Stepper.create(mode= "HALF_STEP",
                    pin1=Pin(16,Pin.OUT),
                    pin2=Pin(17,Pin.OUT),
                    pin3=Pin(5,Pin.OUT),
                    pin4=Pin(18,Pin.OUT),
                    delay=5)
        self.motor_b = Stepper.create(mode= "HALF_STEP", # 26,25,22,23
                    pin1=Pin(26,Pin.OUT),
                    pin2=Pin(25,Pin.OUT),
                    pin3=Pin(0,Pin.OUT),
                    pin4=Pin(4,Pin.OUT),
                    delay=5)
        self.motor_c = Stepper.create(mode= "HALF_STEP", #1,3,9,10
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

    # functions that assigns motor to pins
#    def pins_motor(self,pIN1, pIN2, pIN3, pIN4):
#        IN1 = Pin(pIN1, Pin.OUT)
#        IN2 = Pin(pIN2, Pin.OUT)
#        IN3 = Pin(pIN3, Pin.OUT)
#        IN4 = Pin(pIN4, Pin.OUT)
#        pins = [IN1, IN2, IN3, IN4]
#        self.pins = pins
#        return self.pins


# MOTOR FUNCTIONS

# function that assigns the step sequence
#    def step_sequence(self,n):
#        # clockwise sequence
#        if n > 0:
#            print('clockwise sequence')
#            sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]  
#        # counterclockwise sequence
#        elif n < 0:
#            print('counterclockwise sequence')
#            sequence = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]
#        # freezing sequence
#        else:
#            sequence = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
#            print('freezing sequence')
#        self.sequence = sequence
#        return self.sequence
        
# function that runs n steps on motor x
#    def run_step(self, n, motor_x):
#        sequence = step_sequence(n)
#        pins = motor_x
#        for k in range (0, abs(n)):
#            for step in sequence:
#                for i in range(len(pins)):
#                    pins[i].value(step[i])
#                    sleep(0.001)
#        return

# function that assigns motor rotations depending on translation axis
    def mov(self,vector,ctrl=1):
        # clockwise
        print(vector)
        if vector[1]=="+":
            if vector[0] == "x":
                self.motor_a.step(-7*ctrl)
                self.motor_b.step(7*ctrl)
                #self.run_step(-7, motor_a)
                #self.run_step(7, motor_b)
            elif vector[0] == "y":
                self.motor_a.step(4*ctrl)
                self.motor_b.step(4*ctrl)
                self.motor_c.step(-8*ctrl)
                
                #self.run_step(4, motor_a)
                #self.run_step(4, motor_b)
                #self.run_step(-8, motor_c)
            elif vector[0] == "z":
                self.motor_a.step(8*ctrl)
                self.motor_b.step(8*ctrl)
                self.motor_c.step(8*ctrl)
                
                #self.run_step(8, motor_a)
                #self.run_step(8, motor_b)
                #self.run_step(8, motor_c)
        # counterclockwise
        elif vector[1]=="-":
            if vector[0] == "x":
                self.motor_a.step(7*ctrl)
                self.motor_b.step(-7*ctrl)
                #self.run_step(7, motor_a)
                #self.run_step(-7, motor_b)
            elif vector[0] == "y":
                self.motor_a.step(-4*ctrl)
                self.motor_b.step(-4*ctrl)
                self.motor_c.step(8*ctrl)
                #self.run_step(-4, motor_a)
                #self.run_step(-4, motor_b)
                #self.run_step(8, motor_c)
            elif vector[0] == "z":
                self.motor_a.step(-8*ctrl)
                self.motor_b.step(-8*ctrl)
                self.motor_c.step(-8*ctrl)
                #self.run_step(-8, motor_a)
                #self.run_step(-8, motor_b)
                #self.run_step(-8, motor_c)
        return


# ROTARY ENCODER FUNCTION

# function that translates REC signals into motor rotations
    def REC_translation(self,axis, outPinA, outPinB, tick=0):
        oldA = outPinA.value() 
        oldB = outPinB.value()
        #print(oldB)
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
            #print(vector)
            tick = 0
        # channel B / counterclockwise
        elif B_state == 1 and A==0:
            vector += "-"
            self.mov(vector)
            #print(vector)
            tick = 0
        else:
            sleep(0.001)
            tick = 1
     
        oldA = A
        oldB = B
        # print('rec translation')
    
        return tick


    # PROGRAM
    def run(self,n=1000):
        idle = 0
        # assign pins to the 3 rotary encoders channels (REC)
        # marcus moved outside while loop
        xA,xB = self.pins_REC(15,2)
        yA,yB = self.pins_REC(19,21) # 16,17
        zA,zB = self.pins_REC(14,27) # 5, 18
        
        while idle < n: # timeout after n cycles unused
            idle += 1
        # assign pins to the 3 motors
#        motor_a = self.pins_motor(26, 25, 14, 27)
#        motor_b = self.pins_motor(22, 23, 21, 19)
#        motor_c = self.pins_motor(1, 3, 9, 10)
#        flag=1
        # rotary encoders translation
        
#            if flag==1:
#                print("here")
#                flag=0
        
            idle = idle * self.REC_translation("x",xA,xB)
            idle = idle * self.REC_translation("y",yA,yB)
            idle = idle * self.REC_translation("z",zA,zB)
            sleep(0.001)
        print('Controller timed out from idling')
