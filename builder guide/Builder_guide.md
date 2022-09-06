# Builder guide

## 1.  Bill of materials

In this part we will focus on what components were used and why they were used. Please find the [BOM](https://github.com/Open-2-Photon-Microscope/3-axis-controller/tree/main/BOM) as table format on the repository.

### a.  Delta stage

The [OpenFlexure Delta Stage](https://openflexure.org/projects/deltastage/) is an acknowledged open source device initially designed as a microscope stage. Papers about it were published, which means data such as drift, resolution and stability are available. The stage 3-axis translations are controlled via three 28BYJ-48 -- 5V unipolar stepper motors. This is why the code was specifically developed for coil sequences activation of this kind of motors. Openflexure's program is aimed for Arduino, but in order to broaden our target audience, we wrote a Python program, which runs an esp32 microcontroller.

![28BYJ-48 stepper motor](https://github.com/Open-2-Photon-Microscope/3-axis-controller/blob/main/illustrations/stepper_motor.png)

### b.  Electronics
- To connect the Delta Stage to our manipulator, we are using a [BeeHive](https://github.com/amchagas/BeeHive) board. It's a platform using esp32 as microcontroller, which requires a 12 V power input and presents many 5 V outputs to connect devices. Beware about the common connection mistakes you can make using the BeeHive (check [Common errors](https://github.com/Open-2-Photon-Microscope/3-axis-controller/blob/main/common%20errors/Common_errors.md) doc part 1. a.).
- The rotary encoders are connected to the BeeHive board through a PCB custom made for this project. It contains pull-up resistors and filter capacitors, which are recommended in the component data sheet for proper operation. There's also a bridge divider reducing the encoder channel signal voltage from 5 V to 3 V for the esp32 power supply.
- Here is a connection scheme from one rotary encoder to one motor.

![Electrical connection scheme](https://github.com/Open-2-Photon-Microscope/3-axis-controller/blob/main/illustrations/electrical_connections.png)

### c.  Box

The electrical connections above-mentioned are contained in a box. This box is also the concrete outcome users are going to interact with to control the delta stage. It can be 3D printed (FFF) with PLA, and requires about 350 g of material. To assemble the PCBs in it, you will need :
- x 56 M3 nuts
- x 28 M3 screws, 6 mm below head length, Ø5 mm head diameter

## 2.  Bill of tools and skills

### a.  CAD

To update the design, you will need **FreeCAD** software. It's better if you're familiar with it. More details about the way the CAD was made is written in the following [3. a.](https://github.com/Open-2-Photon-Microscope/3-axis-controller/blob/main/documentation/Developer_guide.md#a--the-box-cad). If you need to modify the rotary encoder board, you'll need to use **KiCad**.

### b.  FFF 3D printer

We sliced the part via **PrusaSlicer**, setting the layer height to 0,20 mm. It is made out of three independant parts : front, below, cap and frame. You can download the four stl files from the Github repo. The only part that requires a bit of support is the cap. An infill of 15% is enough, and could even be lightly reduced.

### c.  Soldering bench

In order to assemble the BeeHive board, the custom made PCB and some electrical connections such as the rotary encoder ones, you will need to deal with soldering.

### d.  Electronic bench

In case you need to do some functionality tests, you will need some basic electronic tools, such as an oscilloscope, or a multimeter for instance.

### e.  Programming

To run the code, you'll have to use the **Jupyter Notebook IDE**.

## 3.  Assembly guide

Work in progress
