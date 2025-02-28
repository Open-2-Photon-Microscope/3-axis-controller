# 3-axis-controller

A manipulator device to operate microscope stage XYZ translations. This project was specifically designed for the OpenFlexure Delta Stage.
  
## Assembly

### Assembling the Board
1. Order the (2 layer) board from a PCB manufacturer (e.g. JLCPCB) by uploading [this file](electronics/integrated_board/Fabrication files/integrated_board_gerbers.zip).
1. Using the [BOM](BOM.xlsx), solder together the integrated board from [electronics/integrated_board](electronics/integrated_board). The board is labeled with the locations and values of resistors, capacitors etc.
    * _Make sure to solder socket headers to the board and slot in the esp32 and pcf8575 modules rather than soldering them directly to the board. Sometimes things go wrong and they will be very hard to remove..._  

### Assembling the controller
1. Assemble the JST-HX cables mentioned in the BOM
1. For each button and flip switch, cut one crimped wire in half and solder before attaching to the JST-XH head  
    ![All switches in the panel use one crimped cable cut in half](illustrations/switch%20JST.jpg)

## Software
### Setting up MicroPython with Thonny IDE
1. Follow the tutorial on [this page](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/) if you haven't already done so when assembling the board.   
### Upload the Code
1. Download our code [here](https://github.com/Open-2-Photon-Microscope/3-axis-controller/tree/main/micropython/V2)
1. Open them all in Thonny.
    * *Connect your board to your PC via micro USB.*
1. In Thonny, in the files panel (`view > files`) navigate to the location of the code to be installed
1. Highlight all files and folders, including `lib`
1. Right click and select __Upload to /__
1. __CHECK:__ Does the file layout in the esp32 look like that on this GitHub?  


### Installing the I2C library
#### You may need to install the `lib` portion of the I2C code another way - the above method __should__ work, so only follow these instructions if something is not behaving as expected.
1. Download [micropython-i2c-lcd-0.1.1.tar.gz](https://pypi.org/project/micropython-i2c-lcd/#files)
1. In Thonny go to `Tools > Manage Packages`
    * _make sure the esp32 is still plugged in to your computer_
1. Click the __Install from local file__ link and select the `.tar.gz` file you downloaded
1. __CHECK:__ Does the file layout in the esp32 look like that on this GitHub? You should not need to but you may have to rename the folder to ensure all the code is looking in the right place...  
