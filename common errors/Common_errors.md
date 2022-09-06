# Common errors

## 1.  Builder

### a.  BeeHive / esp32

- Don’t power the Beehive with the micro usb cable only. Always use simultaneously the 12 V power supply and the 5 V micro usb power supply.
- Don’t use the analog pins called “A1”, “A2” and “A3”.
- Don’t use the pins 0 and 4 when you are connected to the computer via usb connection.

### b.  Electrical connections

If you notice that a circuit isn’t working, although each electrical connection was double checked, try to remove and solder its components to the board again.


## 2.  User

### a.  Running the code

- If the error “pin can only be input” appears, make sure that rotary encoders and motors aren’t connected to any analog pin. The analog pins are located in the “A1”, “A2” and “A3” BeeHive connectors. 

![](https://github.com/Open-2-Photon-Microscope/3-axis-controller/blob/main/illustrations/common_errors_1.PNG)

- If you’re having trouble connecting the esp32, try to close the jupyter notebook and the command prompt windows and start all over again.
If it persists, you can erase and flash again the esp32. 

![](https://github.com/Open-2-Photon-Microscope/3-axis-controller/blob/main/illustrations/common_errors_2.PNG)
