<p align="center">

<img src="https://github.com/mitgobla/TL-3DPrinter/blob/master/docs/bolt-128.png?raw=true">

</p>

# Team Lightning LEGO 3D Builder

LEGO Model generator and preview software written in Python.

## Backstory

Team Lightning is a robotics and programming club based in Ysgol Gyfun Emlyn School in Wales.
_Visit [Team Lightning's Website](http://www.team-lightning.ga) to find out more._

Team Lightning participated in the annual [Technocamps](http://www.technocamps.com/en) competition on the 5th of July, 2018. The brief was to create a robot from LEGO Mindstorms or Arduino that could produce art or music. The team decided to create a 3-axis printer that could place 2x2 LEGO bricks onto a plate.

This repo stores all the code we produced.

## This Repository

There are three main folders to this repo:

- `ev3-code` This has the code used on the LEGO Mindstorms EV3.
- `lego-print` This is the original python code used for the competition.
- `rewrite` This is the improvement of the Python code _after_ the competition.

## FLASH 3D Printer Preview software a.k.a `rewrite`

As previously mentioned, this folder contains the code for the working and improved version of the preview and generation software. It is being updated to add more features.

### How to use

Look in the `examples` folder to see how model files should be written. It is in this format:

`x, y, z, c` where `c` can be `1` for red, `2` for blue, and `3` for yellow.

Next, you need to generate this model into a FLASH file. Run `flash.py` and you will see a generate button. This saves the FLASH file as `model.FLASH` in the `models` folder. This folder also has the file to be uploaded to the EV3.

Then all you have to do is press the load button and select the `model.FLASH` file. The animated display and final display will update automatically.

To change the speed of the animation, change the spinbox value. Values range from 0.1 to 5 seconds.

#### Requirements

```none
Python 3.4+
numpy
PyQt5
PyQTGraph
Tkinter
```

## Other Folders

### `ev3-code`

There are four parts to this code that make up the entire process of the printer.

#### Blocks

Firstly, `ReadModel` reads the number of coordinates from the first line of the `.rtf` file and then loops through each axis and `c` (colour), adding each to their respective array.

Next, `DisplayCurrentXYZ` updates the EV3 display with the next coordinates in the list, the block colour, and a neat progress bar and our logo.

Then `ResetCoordinates` simply sets the motor rotations to 0 and the current position of the print head to `0, 0, 0`

All these blocks are used in `Program`. This file has a list of variables that can be changed for calibration at the start, such as the number of rotations for 1 stud of movement.

#### The printing program

The printer first performs a `z-hop` (z is the up-down direction of the head) 3 blocks above the next coordinate to prevent it colliding with bricks on the plate.

Next, it synchronously moves the x-axis and y-axis motors for faster print time. It waits until both motors have completed their movement.

Finally, it moves the head to the z-coordinate at high power, and then performs a z-press which basically squashes the brick on to the plate/brick below.

### `lego-print`

This folder contains all the original code for generating models and testing previews. Creating a model that could be used by the EV3 was successful - creating a 3D display to show the model beforehand was not. However, `mitgobla` continued to create a working version called `rewrite` after the competition.
