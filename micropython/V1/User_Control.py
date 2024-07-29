import controller

def getInfo():
    s = input()
    head = s.rstrip('0123456789-').lower()
    if head != 'q':
        tail = s[len(head):]
        tail = int(tail)
    else:
        tail = 0
    return head, tail


# Fine tuning for control
x_fine = 1
y_fine = 1
z_fine = 1

def user(head='', tail=0):
    c = controller.controller()
    while head != 'q':
        head = ''
        tail = 0
        print("Enter a command (e.g. a10 or z-50) or press 'q' to quit")
        while head not in 'abcxyzq' or tail == 0:
            head, tail = getInfo()
            if head == 'q':
                tail = 1
        # Individual motor movements
        if head in 'abc':
            if head == 'a': # there is a back-end error lurking around thonny somewhere
                c.motor_a.step(tail)
            if head == 'b':
                c.motor_b.step(tail)
            if head == 'c':
                c.motor_c.step(tail)
                
        # Axis movements
        elif head in 'xyz':
            if tail < 0:
                sign = '-'
                tail = tail * -1
            else:
                sign = '+'
            for i in range(tail):
                c.mov([head,sign])
    return

def moveOnWake():
    heads = ['a','b','c']
    tails = [100,-100,20,-20]
    for t in tails:
        for h in heads:
            user(h,t)