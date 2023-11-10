import controller

def getInfo():
    s = input()
    head = s.rstrip('0123456789-').lower()
    tail = s[len(head):]
    tail = int(tail)
    return head, tail

"""
x = a-7, b+7
y = a+4, b+4, c-8
z = a+8, b+8, c+8
"""
# Fine tuning for control
x_fine = 1
y_fine = 1
z_fine = 1

def user(head='', tail=0):
    c = controller.controller()
    while head not in 'abcxyz' or tail == 0:
        head, tail = getInfo()

    if head in 'abc':
        if head == 'a': # there is a back-end error lurking around thonny somewhere
            c.motor_a.step(tail)
        if head == 'b':
            c.motor_b.step(tail)
        if head == 'c':
            c.motor_c.step(tail)
    elif head in 'xyz':
        if tail < 0:
            sign = '-'
            tail = tail * -1
        else:
            sign = '+'
        for i in range(tail):
            c.mov([head,sign])

def moveOnWake():
    heads = ['a','b','c']
    tails = [100,-100,20,-20]
    for t in tails:
        for h in heads:
            user(h,t)