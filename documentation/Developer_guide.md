# Developer guide

## 1.  Bill of materials

In this part we will focus on what components were used and why they were used. Please find the BOM as table format on the repository.

### a.  Delta stage

The [OpenFlexure Delta Stage](https://openflexure.org/projects/deltastage/) is an acknowledged open source device initially designed as a microscope stage. Papers about it were published, which means data such as drift, resolution and stability are available. The stage 3-axis translations are controlled via three 28BYJ-48 -- 5V unipolar stepper motors. This is why the code was specifically developed for coil sequences activation of this kind of motors. Openflexure's program is aimed for Arduino, but in order to broaden our target audience, we wrote a Python program, which runs an esp32 microcontroller.
![test](pictures/stepper_motor.png)

### b.  Electronics

    i.  To connect the Delta Stage to our manipulator, we are using a [[BeeHive]{.underline}][3] board. It's a platform using esp32 as microcontroller, which requires a 12 V power input and presents many 5 V outputs to connect devices. Beware about the common connection mistakes you can make using the BeeHive (check "Common mistakes" doc part 1. a.).

    ii. The rotary encoders are connected to the BeeHive board through a PCB custom made for this project. It contains pull-up resistors and filter capacitors, which are recommended in the component data sheet for proper operation. There's also a bridge divider reducing the encoder channel signal voltage from 5 V to 3 V for the esp32 power supply.

    iii. Here is a connection scheme from one rotary encoder to one motor.\
         ![][4]

### c.  Box

The electrical connections above-mentioned are contained in a box. This box is also the concrete outcome users are going to interact with to control the delta stage. It can be 3D printed (FFF) with PLA, and requires about 350 g of material. To assemble the PCBs in it, you will need :

i.  x 56 M3 nuts

ii. x 28 M3 screws, 6 mm below head length, Ø5 mm head diameter

## 2.  Bill of tools and skills

### a.  CAD

To update the design, you will need **FreeCAD** software. It's better if you're familiar with it. More details about the way the CAD was made is written in the following 3. a. If you need to modify the rotary encoder board, you'll need to use **KiCad**.

### b.  FFF 3D printer

We sliced the part via **PrusaSlicer**, setting the layer height to 0,20 mm. It is made out of three independant parts : front, below, cap and frame. You can download the four stl files from the Github repo. The only part that requires a bit of support is the cap. An infill of 15% is enough, and could even be lightly reduced.

### c.  Soldering bench

In order to assemble the BeeHive board, the custom made PCB and some electrical connections such as the rotary encoder ones, you will need to deal with soldering.

### d.  Electronic bench

In case you need to do some functionality tests, you will need some basic electronic tools, such as an oscilloscope, or a multimeter for instance.

### e.  Programming

To upgrade the code, or understand its structure, you'll need some knowledge in **Python**. We used the **Jupyter Notebook IDE** to develop and run the code on the manipulator.

## 3.  How has the project been developed ?

### a.  The box CAD

It is parametrized, so if you want to customise it, you can open the source file in FreeCAD and directly change the wanted parameter in the Spreadsheet. Here is a table which identifies the different parameter spreadsheets :

  ----------------------- ---------------------------- -------------------------------------------------------------------------------------------------------------------------------------
  Table name              Parameter                    Explanation

  Spreadsheet.front       length                       box length without taking into account the 2 sides thickness

                          height                       box height without taking into account the top and below sides thickness

                          fastening thickness          thread length

                          thickness                    Pocket depth minus slack

                          notch length                 \-

                          slack                        Assembly slack for pocket depth

                          frame thickness              \-

                          nut thickness                rotary encoder nut thickness

                          centre distance              distance between to rotary encoder rod center

                          encoder width                \-

                          rod diameter                 rotary encoder rod diameter

                          nut edge                     rotary encoder nut edge

                          hole                         rotary encoder rod hole

                          encoder height               \-

                          encoder height below shaft   \-

                          part thickness               front part thickness,\
                                                       = fastening thickness + thickness + slack.

  Spreadsheet.below       below side thickness         \-

                          screw head diameter          assembly screw head diameter

                          screw head thickness         assembly screw head thickness

                          screw length                 assembly screw length

                          hole diameter                mounting hole diameter

                          PCB center distance 1        biggest distance between 2 PCB (rotary encoder board) mounting hole centers

                          PCB center distance 2        smallest distance between 2 PCB (rotary encoder board) mounting hole centers

                          PCB dimension 1              biggest PCB (rotary encoder board) dimension

                          PCB dimension 2              smallest PCB (rotary encoder board) dimension

                          BeeHive center distance 1    biggest distance between 2 BeeHive board mounting hole centers

                          BeeHive center distance 2    smallest distance between 2 BeeHive board mounting hole centers

                          BeeHive dimension 1          biggest BeeHive board dimension

                          BeeHive dimension 2          smallest BeeHive board dimension

                          PCB gap                      distance between 2 boards

                          rotary encoder thickness     \-

                          RE wire connection depth     volume dedicated to rotary encoder connection wires

                          box depth                    inside box depth,\
                                                       = rotary encoder thickness + RE wire connection depth + PCB dimension 1 + BeeHive dimension 2 + ULN board dimension2 + 3 \* PCB gap

                          mounting hole diameter       \-

                          below part thickness         \-

                          assembly gap                 gap dedicated to counter 3D printed imprecision and allow by hand assembly

  Spreadsheet.cap         motor cables hole height     rectangle side dimension for motor cables

                          motor cables hole length     rectangle side dimension for motor cables

                          power supply hole            square side dimension for power supply cables
  ----------------------- ---------------------------- -------------------------------------------------------------------------------------------------------------------------------------

If you are curious about a specific box feature, please find its design brief on the repository.

b.  Electronics

To allow a proper operation of each rotary encoder, and reduce channel voltage to 3V for esp32 power supply, we had to design a custom made board. We used KiCad to draw the schematics and then design the board. The schematics and the board source files are available in the Github repo. If you only aime to manufacture it again, please find the gerber file in the same place.

c.  Code

The code has been developed on a Jupyter Notebook. It has been implemented in several modules :

-   Pin assignment

You can find here two functions: one that assigns channels A and B of each rotary encoder to pins and another that assigns motors to pins.

-   Motor functions

    -   The first function defines the motor sequence depending on the command : clockwise, counter clockwise or freeze.

    -   The second one runs the required amount of steps. If the required number is negative, let's say "-n", it will run "n" counter clockwise sequences.

    -   The third one assigns the required motor rotation combination to each translation axis. For example, if the Y-axis rotary encoder sends a clockwise command, motors a and b are going to run -4 steps and motor c 8 steps. This conversion from cartesian to delta movement is explained in d. Kinematics.

-   Rotary encoder function\
    ![][5]

(Rotary optical encoder from Bourns datasheet)

This function translates the rotary encoder signal into motor rotations. Channels A and B have square signals, with high (=1) and low (=0) output values. However the signals are slightly delayed one another. The first channel to reach the high output value indicates if the encoder is turned either clockwise or counterclockwise. In order to know which signal is ahead, the code implements two data: the channel value and the channel state. The channel state is the current output value minus the previous one. When this state is equal to 1, it means that the output has changed from high to low. So, if channel A state is 1 and channel B output value is 0, then channel A is the first one to reach high output. This means that the rotary encoder is being turned clockwise. On the contrary, if channel B state is 1 and channel A output value is 0, the rotary encoder is being turned anticlockwise.

-   Program

The program is an open loop. Its first step is to assign the rotary encoder channels pins and the motor pins as well. In the open loop, each rotary encoder is assigned to a translation axis, and runs motor rotation if the appropriate output voltage is detected.

a.  Kinematics

The 28byj-48 stepper motor has four coils that can be activated by sequences. Depending on the sequence pattern, the motor will turn clockwise or counterclockwise. Here is the clockwise sequence pattern: \[1,0,0,0\], \[0,1,0,0\], \[0,0,1,0\], \[0,0,0,1\]. Each sequence activates one motor step. So, every complete sequence pattern activates four motor steps. The original motor step is 0,18°. So the motor has to do 2038 steps to complete a rotation.

To reach the sub micron step size, you would have to upgrade the program. We have been focusing on steps (sub micron steps would be called "microsteps"). In order to translate in one axis translation, the Delta Stage requires a specific motor combination. According to the matrix below, one positive unit in the x direction requires -cos30 (= - 0,87) motor a step and one 0,87 motor b step. In order to command a decimal step value you would require PWM. As it lowers the device stability and consumes a lot of energy, we wanted to first test the device with whole steps.

![][6]

![][7]

The littlest multiple that would allow a complete whole number step value combination is 8. This way, the new motor step is 1,44°, 250 steps would complete a whole motor shaft rotation.

  --------------------------------- -------------------------------------
                                    **8 steps**

  1                                 8 steps

                                    1,44°

  0,5 = cos60                       4 steps

                                    0,72°

  0,87 = cos30                      6,96 ≈ 7 steps

                                    1,25°
  --------------------------------- -------------------------------------

4.  Current state of development

    a.  tasks currently worked on

Have a look at the [[github projects]{.underline}][8], to check the current state of development.

b.  open task priorities

-   Acceptance tests\
    [[https://github.com/Open-2-Photon-Microscope/3-axis-controller/projects/6#card-85028599]{.underline}][9] :

    -   check how well it moves in X,Y,Z (as the code we are implementing converts delta stage movement to cartesian)

    -   see what is the minimum amount we can move

    -   see how fast things are moving

    -   see how stable the system is without moving (drifts over 30min/hour? or even longer)

-   Programming

    -   Refine the open loop program. OpenFlexure uses a specific algorithm to overcome open loop backlashes.

    -   The user has to be able to command the stage to translate to a specific location.

    -   Allow the device to do microstepping. The minimal step size has to be sub-micron.

5.  Documentation/references

    a.  Delta Stage

-   McDermott, S., Ayazi, F., Collins, J., Knapper, J., Stirling, J., Bowman, R., & Cicuta, P. «Multimodal microscopy imaging with the OpenFlexure Delta Stage.» *Optics Express*, 2022.

-   James P. Sharkey, Darryl C. W. Foo, Alexandre Kabla, et al. «A one-piece 3D printed flexure translation stage for open-source microscopy.» *Review of Scientific Instruments*, 2016

  [1]: https://openflexure.org/projects/deltastage/
  [2]: media/image1.png {width="2.46875in" height="1.1068722659667543in"}
  [3]: https://github.com/amchagas/BeeHive
  [4]: media/image2.png {width="4.566637139107612in" height="7.740676946631671in"}
  [5]: media/image3.png {width="4.546875546806649in" height="1.4502963692038495in"}
  [6]: media/image4.png {width="6.270833333333333in" height="2.1039074803149607in"}
  [7]: media/image5.png {width="3.3020833333333335in" height="0.9583333333333334in"}
  [8]: https://github.com/Open-2-Photon-Microscope/3-axis-controller/projects?type=classic
  [9]: https://github.com/Open-2-Photon-Microscope/3-axis-controller/projects/6#card-85028599
