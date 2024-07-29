# 3-axis-controller

A manipulator device to operate microscope stage XYZ translations. This project was specifically designed for the OpenFlexure Delta Stage.
  
## Assembly

Using the BOM, assemble the board in the __electronics__ folder. The board is labelled with the locations and values of resistors, capacitors etc.

## Software
### Setting up MicroPython with Thonny IDE
1. Follow the tutorial on [this page](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/) if you haven't already done so when assembling the board.  
### Upload the Code
1. Download our code [here](https://github.com/Open-2-Photon-Microscope/3-axis-controller/tree/main/micropython/V2)
1. Open them all in Thonny.
    * *Connect your board to your PC via micro USB.*
1. Save each file to the board.
1. You may need to install the `lib` portion of the I2C code another way.

### Installing the I2C library
1. Download [micropython-i2c-lcd-0.1.1.tar.gz](https://pypi.org/project/micropython-i2c-lcd/#files)
1. In Thonny go to `Tools > Manage Packages`
    * _make sure the esp32 is still plugged in to your computer_
1. Click the __Install from local file__ link and select the `.tar.gz` file you downloaded
1. __CHECK:__ Does the file layout in the esp32 look like that on this GitHub? You should not need to but you may have to rename the folder to ensure all the code is looking in the right place...