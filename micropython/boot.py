# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from startup import set_pins, read_pins
set_pins()

#from cart_del import Stage

#stage = Stage()
#stage.zero(True)
#stage.smooth_move()