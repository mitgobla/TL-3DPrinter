<p align="center">

<img src="https://github.com/mitgobla/TL-3DPrinter/blob/master/docs/bolt-128.png?raw=true">

</p>

# Team Lightning LEGO 3D Builder

LEGO Model generator and preview software written in Python.

## Backstory

Team Lightning is a robotics and programming club based in Ysgol Gyfun Emlyn School in Wales.
Visit [Team Lightning's Website](http://www.team-lightning.ga)

Team Lightning participated in the annual [Technocamps](http://www.technocamps.com/en) competition on the 5th of July, 2018. The brief was to create a robot from LEGO Mindstorms or Arduino that could produce art or music. The team decided to create a 3-axis printer that could place 2x2 LEGO bricks on to a plate.

This repo stores all the code we produced.

## This Repository

There are three main folders to this repo:

- `ev3-code` This has the code used on the LEGO Mindstorms EV3.
- `lego-print` This is the original python code used for the competition.
- `rewrite` This is the improvement of the Python code _after_ the competition.

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

### `rewrite`

As previously mentioned, this folder contains the code for the working and improved version of the preview and generation software. It is being updated to add more features.
