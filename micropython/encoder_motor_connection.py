%serialconnect to --port COM5 --baud=115200

from machine import Pin
from time import sleep

pA = Pin(14, Pin.IN)
pB = Pin(27, Pin.IN)

ledA = Pin(2, Pin.OUT)
ledB = Pin(15, Pin.OUT)

IN1 = Pin(0, Pin.OUT)
IN2 = Pin(4, Pin.OUT)
IN3 = Pin(18, Pin.OUT)
IN4 = Pin(5, Pin.OUT)
pins = [IN1, IN2, IN3, IN4]

oldA = pA.value() 
oldB = pB.value()

while True:
    
    A = pA.value()
    B = pB.value()
    
    Astate = A-oldA
    Bstate = B-oldB
       
    #channel A / clockwise
    if  Astate == 1 and B==0:
        ledA.on()
        ledB.off()
        sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

    #channel B / counterclockwise
    elif Bstate == 1 and A==0:
        ledA.off()
        ledB.on()
        sequence = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)
                
    else:
        ledA.off()
        ledB.off()
        sleep(0.001)
        
    oldA = A
    oldB = B           