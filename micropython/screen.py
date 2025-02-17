from lcd_i2c import LCD
from machine import I2C, Pin

# Define custom pins for SCL and SDA
scl_pin = Pin(33)  # Replace with your desired SCL pin
sda_pin = Pin(32)  # Replace with your desired SDA pin



# PCF8574 on 0x27
I2C_ADDR = 0x27
NUM_ROWS = 2
NUM_COLS = 16

# define custom I2C interface, default is 'I2C(0)'
i2c = I2C(0, scl=scl_pin, sda=sda_pin, freq=800000)
lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)

# get LCD infos/properties
print("LCD is on I2C address {}".format(lcd.addr))
print("LCD has {} columns and {} rows".format(lcd.cols, lcd.rows))
print("LCD is used with a charsize of {}".format(lcd.charsize))
print("Cursor position is {}".format(lcd.cursor_position))

if __name__ == '__main__':
#     # create mu character for lcd.print(chr(0))
#     lcd.create_char(0,[0x00,
#       0x00,
#       0x00,
#       0x11,
#       0x11,
#       0x1B,
#       0x15,
#       0x10]
#     )

    # start LCD, not automatically called during init to be Arduino compatible
    lcd.begin()
