from machine import Pin
import time



# function that assigns rotary encoders X, Y and Z channels (REC) to pins


def pins_REC(pinA, pinB):
    outPinA = Pin(pinA, Pin.IN)
    outPinB = Pin(pinB, Pin.IN)
    return outPinA, outPinB

    # functions that assigns motor to pins
def pins_motor(pIN1, pIN2, pIN3, pIN4):
    IN1 = Pin(pIN1, Pin.OUT)
    IN2 = Pin(pIN2, Pin.OUT)
    IN3 = Pin(pIN3, Pin.OUT)
    IN4 = Pin(pIN4, Pin.OUT)
    pins = [IN1, IN2, IN3, IN4]
    return pins


# MOTOR FUNCTIONS

# function that assigns the step sequence
def step_sequence(n):
    #sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]  
    # clockwise sequence
    if n > 0:
        #print('clockwise sequence')
        sequenceOut = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        # counterclockwise sequence
    elif n < 0:
        #print('counterclockwise sequence')
        sequenceOut = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]
        # freezing sequence
    else:
        sequenceOut = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        #print('freezing sequence')
    
    return sequenceOut
        
# function that runs n steps on motor x
def run_step(n, motor):
    sequence = step_sequence(n)
    #print(sequence)
    pins = motor
    for k in range (0, abs(n)):
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                time.sleep_ms(1)
    return

# function that assigns motor rotations depending on translation axis
def mov(vector,motor_a,motor_b,motor_c):
    # clockwise
    #print(vector)
    if vector[1]=="+":
        if vector[0] == "x":
            run_step(-7, motor_a)
            run_step(7, motor_b)
        elif vector[0] == "y":
            run_step(4, motor_c)
            run_step(4, motor_b)
            run_step(-8, motor_c)
        elif vector[0] == "z":
            run_step(8, motor_a)
            run_step(8, motor_b)
            run_step(8, motor_c)
        # counterclockwise
    elif vector[1]=="-":
        if vector[0] == "x":
            run_step(7, motor_a)
            run_step(-7, motor_b)
        elif vector[0] == "y":
            run_step(-4, motor_a)
            run_step(-4, motor_b)
            run_step(8, motor_c)
        elif vector[0] == "z":
            run_step(-8, motor_a)
            run_step(-8, motor_b)
            run_step(-8, motor_c)
        #time.sleep_ms(1)
    return


# ROTARY ENCODER FUNCTION

# function that translates REC signals into motor rotations
def REC_translation(axis, outPinA, outPinB,motor_a,motor_b,motor_c):
    oldA = outPinA.value() 
    oldB = outPinB.value()
        #print(oldB)
    time.sleep_ms(5)

    vector = axis  
    A = outPinA.value()
    B = outPinB.value()    
    A_state = A-oldA
    B_state = B-oldB
       
    # channel A / clockwise
    if  A_state == 1 and B==0:
        vector += "+"
        mov(vector,motor_a,motor_b,motor_c)
    # channel B / counterclockwise
    elif B_state == 1 and A==0:
        vector += "-"
        mov(vector,motor_a,motor_b,motor_c)
    else:
        time.sleep_ms(1)
     
    oldA = A
    oldB = B
    #print('rec translation')
    
    return


    # PROGRAM
def run():
    # assign pins to the 3 rotary encoders channels (REC)
    xA,xB = pins_REC(15,2)
    yA,yB = pins_REC(16,17)
    zA,zB = pins_REC(5,18)
    #print("here")
    #print(zA)

        # assign pins to the 3 motors
    motor_a = pins_motor(26, 25, 14, 27)
    motor_b = pins_motor(22, 23, 21, 19)
    motor_c = pins_motor(12, 13, 9, 10)
    flag=1
    #print(flag)
    # rotary encoders translation
    while True:
        #if flag==1:
            #print("here")
        #    flag=0
        
        REC_translation("x",xA,xB,motor_a,motor_b,motor_c)
        REC_translation("y",yA,yB,motor_a,motor_b,motor_c)
        REC_translation("z",zA,zB,motor_a,motor_b,motor_c)
        time.sleep_ms(2)
