# User input to manually control stage movement

from cart_del import stage

def user(direction="", distance=0, Move_Relative=True):
    # takes user-friendly input
    
    while direction not in "abcxyzq_":
        command = input().lower()