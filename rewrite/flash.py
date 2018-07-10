"""
Title: FLASH
Description: 3D Preview software for models to be printed on
             Team Lightning 3D printers.

Author: Ben Dodd (mitgobla)
Email: ben-dodd@outlook.com
Website: http://www.team-lightning.ga
"""

import os
import tkinter as tk
from tkinter import filedialog
from ast import literal_eval

import numpy as np
import pyqtgraph.dockarea as qtdk
import pyqtgraph.opengl as gl
from pyqtgraph import mkColor, LayoutWidget, SpinBox
from pyqtgraph.Qt import QtCore, QtGui

import generator

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class FileLoader:
    """Loads a text file of coordinates and colours
    """

    def __init__(self):
        self.window = tk.Tk()
        self.window.withdraw()
        self.file = None

    def load_txt(self):
        """Load the list of brick positions and colours
        """
        self.window.filename = filedialog.askopenfilename(
            initialdir=SCRIPT_DIR,
            title="Select Coordinate file",
            filetypes=[("Text Files", "*.txt")])
        self.file = self.window.filename
        if not self.file:
            print("No File Selected, aborting")
            exit(0)

    def load_flash(self):
        """Load a FLASH file
        """
        self.window.filename = filedialog.askopenfilename(
            initialdir=SCRIPT_DIR,
            title="Select FLASH file",
            filetypes=[("FLASH Files", "*.flash")])
        self.file = self.window.filename
        if not self.file:
            print("No File Selected, aborting")
            exit(0)

    @property
    def return_coordinates(self):
        """Convert FLASH to coordinates

        Returns:
            list -- Array of Lists [x, y, z, c]
        """

        return literal_eval(self.file)


class Display:
    """Core functions for display
    """

    def __init__(self):
        """Core functions for display
        """
        self.app = QtGui.QApplication([])
        self.window = QtGui.QMainWindow()
        self.area = qtdk.DockArea()

        self.window.setCentralWidget(self.area)
        self.window.resize(1000, 500)
        self.window.setWindowTitle('FLASH - LEGO 3D Printer Software')

        self.docks = []
        self.widgets = []
        self.premade_widgets = {}

        self.extruders = []

    def add_dock(self, title, x_pos, y_pos, position):
        """Add a dock to the window

        Arguments:
            title {string} -- Title of the dock
            x {int} -- Width
            y {int} -- Height
            position {string} -- Grid position
        """

        self.docks.append(qtdk.Dock(title, size=(x_pos, y_pos)))
        self.area.addDock(self.docks[-1], position)

    def add_gl_widget(self):
        """Adds an OpenGL View Widget
        """

        self.widgets.append(gl.GLViewWidget())
        self.widgets[-1].opts['distance'] = 20
        self.widgets[-1].show()
        self.widgets[-1].setBackgroundColor(mkColor(155, 155, 155, 0))

    def add_to_dock(self, index, widget):
        """Add a widget to a dock

        Arguments:
            index {int} -- Dock index in self.docks
            widget {object} -- Widget from self.widgets
        """

        self.docks[index].addWidget(widget)

    def initialize_widgets(self):
        """Creates predefined objects for OpenGL displays
        """

        self.premade_widgets["grid"] = gl.GLGridItem(
            size=QtGui.QVector3D(8, 9, 1))
        self.premade_widgets["grid"].setSpacing(
            spacing=QtGui.QVector3D(0.5, 0.5, 0.5))
        self.premade_widgets["grid"].translate(4.5, 5, 0)

        self.premade_widgets["x_line"] = np.array([
            [0, 0, 0],
            [2, 0, 0]
        ])

        self.premade_widgets["y_line"] = np.array([
            [0, 0, 0],
            [0, 2, 0]
        ])

        self.premade_widgets["z_line"] = np.array([
            [0, 0, 0],
            [0, 0, 2]
        ])

        self.premade_widgets["axis_line_colour"] = np.array([
            [1, 0, 0, 1],
            [1, 0, 0, 1]
        ])

        self.premade_widgets["block_verts"] = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 1, 1]],
                                                       dtype=float)

        self.premade_widgets["block_faces"] = np.array([
            [0, 1, 2],
            [0, 2, 3],
            [0, 1, 4],
            [1, 5, 4],
            [1, 2, 5],
            [2, 5, 6],
            [2, 3, 6],
            [3, 6, 7],
            [0, 3, 7],
            [0, 4, 7],
            [4, 5, 7],
            [5, 6, 7],
        ])

    def add_axis_line(self, linename, widget):
        """Add an axis line to a OpenGL Widget

        Arguments:
            lineName {str} -- Axis name
            widget {int} -- Widget to draw line on
        """
        line = gl.GLLinePlotItem(pos=self.premade_widgets[linename],
                                 color=self.premade_widgets["axis_line_colour"],
                                 width=2,
                                 antialias=True)
        line.translate(0.5, 0.5, 0)
        self.widgets[widget].addItem(line)

    def add_extruder(self, widget, x_pos, y_pos, z_pos):
        """Add the extruder object to a OpenGL Widget

        Arguments:
            widget {int} -- Widget to draw extruder on
            x_pos {float} -- Extruder x position
            y_pos {float} -- Extruder y position
            z_pos {float} -- Extruder z position
        """

        extruder_gl = gl.GLBoxItem(size=QtGui.QVector3D(
            0.5, 0.5, 8), color=(55, 155, 55, 255))
        extruder_gl.translate(x_pos, y_pos, z_pos)
        self.extruders.append(extruder_gl)
        self.widgets[widget].addItem(self.extruders[-1])


class Graphics:
    """Class for updating display
    """

    def __init__(self):
        self.root = Display()
        self.root.initialize_widgets()

        self.current_position = (0, 0, 0)
        self.coordinate_index = 0

    def add_box(self, position, colour, widget):
        """Create a brick on the display

        Arguments:
            position {tuple} -- XYZ Tuple position of the brick
            colour {tuple} -- RGBW of the brick
            widget {int} -- Widget to draw brick to
        """
        box = gl.GLMeshItem(vertexes=self.root.premade_widgets["block_verts"],
                            faces=self.root.premade_widgets["block_faces"],
                            color=colour,
                            glOptions='translucent',
                            smooth=True)
        box.translate(position[0], position[1], position[2])
        frame = gl.GLBoxItem(color=(0, 0, 0, 255))
        frame.translate(position[0], position[1], position[2])

        self.root.widgets[widget].addItem(box)
        self.root.widgets[widget].addItem(frame)

    def update_extruder(self, position, widget):
        """Update extruder position

        Arguments:
            position {tuple} -- XYZ tuple of position
            widget {int} -- Widget to draw extruder to
        """

        for extruder_objects in self.root.extruders:
            if extruder_objects in self.root.widgets[widget].items:
                self.root.widgets[widget].removeItem(extruder_objects)
        self.root.add_extruder(widget, position[0], position[1], position[2])


class Preview:
    """Class for updating previews
    """

    def __init__(self):
        self.graphic_engine = Graphics()
        self.rotation = 0
        self.model = []
        self.index = len(self.model)
        self.pos = []

        self.red = (1, 0, 0, 0.8)
        self.blue = (0, 0, 1, 0.8)
        self.yellow = (1, 1, 0, 0.8)
        self.next_colour = ()

    def add_widget(self, title, pos):
        """Add a widget for displaying objects

        Arguments:
            title {string} -- Title of the display
            pos {string} -- Position of the display
        """

        self.graphic_engine.root.add_dock(title, 500, 300, pos)
        self.graphic_engine.root.add_gl_widget()
        self.graphic_engine.root.add_to_dock(-1,
                                             self.graphic_engine.root.widgets[-1])
        self.graphic_engine.root.add_axis_line("x_line", -1)
        self.graphic_engine.root.add_axis_line("y_line", -1)
        self.graphic_engine.root.add_axis_line("z_line", -1)
        self.graphic_engine.root.widgets[-1].addItem(
            self.graphic_engine.root.premade_widgets["grid"])

    def generate_model(self, widget):
        """Generate the model on the widget

        Arguments:
            widget {int} -- Widget to generate model on
        """
        self.index = len(self.model)

        for item in self.graphic_engine.root.widgets[widget].items:
            self.graphic_engine.root.widgets[widget].items.remove(item)

        self.graphic_engine.root.widgets[widget].items = []
        self.graphic_engine.root.widgets[widget].update()

        self.graphic_engine.add_box((-2, 0.5, 0.2), self.red, widget)
        self.graphic_engine.add_box((-2, 3.5, 0.2), self.blue, widget)
        self.graphic_engine.add_box((-2, 6.5, 0.2), self.yellow, widget)
        self.graphic_engine.root.widgets[widget].addItem(
            self.graphic_engine.root.premade_widgets["grid"])

        for pos in self.model:
            self.next_colour = ()
            if pos[3] == 1:
                self.next_colour = self.red
            elif pos[3] == 2:
                self.next_colour = self.blue
            elif pos[3] == 3:
                self.next_colour = self.yellow

            if pos[3] != 0:
                self.graphic_engine.add_box(
                    (pos[0]/2, pos[1]/2, pos[2]-1), self.next_colour, widget)

    def update_animated(self, widget=0):
        """Update an animated widget

        Arguments:
            widget {int} -- Widget to update
        """
        if self.model == []:
            return

        if self.index == len(self.model):
            self.index = 0
            for item in self.graphic_engine.root.widgets[widget].items:
                self.graphic_engine.root.widgets[widget].items.remove(item)

            self.graphic_engine.root.widgets[widget].items = []
            self.graphic_engine.root.widgets[widget].update()

        self.graphic_engine.add_box((-2, 0.5, 0.2), self.red, widget)
        self.graphic_engine.add_box((-2, 3.5, 0.2), self.blue, widget)
        self.graphic_engine.add_box((-2, 6.5, 0.2), self.yellow, widget)

        self.graphic_engine.root.widgets[widget].addItem(
            self.graphic_engine.root.premade_widgets["grid"])
        self.graphic_engine.update_extruder(((self.model[self.index][0]/2)+0.25,
                                             (self.model[self.index]
                                              [1]/2)+0.25,
                                             self.model[self.index][2]),
                                            widget)
        if self.model[self.index][3] == 1:
            self.graphic_engine.add_box((self.model[self.index][0]/2,
                                         self.model[self.index][1]/2,
                                         self.model[self.index][2]-1), self.red,
                                        widget)
        elif self.model[self.index][3] == 2:
            self.graphic_engine.add_box((self.model[self.index][0]/2,
                                         self.model[self.index][1]/2,
                                         self.model[self.index][2]-1), self.blue,
                                        widget)
        elif self.model[self.index][3] == 3:
            self.graphic_engine.add_box((self.model[self.index][0]/2,
                                         self.model[self.index][1]/2,
                                         self.model[self.index][2]-1), self.yellow,
                                        widget)
        self.index += 1

    def update_frozen(self, widget=1):
        """Update the frozen display

        Keyword Arguments:
            widget {int} -- Widget to update (default: {1})
        """

        if self.rotation >= 360:
            self.rotation = 0

        self.graphic_engine.root.widgets[widget].opts['center'] = QtGui.QVector3D(
            6.5, 6.5, 0)
        self.graphic_engine.root.widgets[widget].setCameraPosition(
            elevation=25, azimuth=self.rotation)
        self.rotation += 1


PREVIEWER = Preview()


def generate_flash_file():
    """Generate a flash file for preview
    """

    loader = FileLoader()
    loader.load_txt()
    model = generator.Model(loader.file)
    model.read()
    generate = generator.Generate(model)
    generate.gen_model()
    generate.write_model()


def load_flash_file():
    """Load a FLASH file for preview
    """

    loader = FileLoader()
    loader.load_flash()
    model_content = open(loader.file, "r")
    model = literal_eval(model_content.read())
    model_content.close()
    PREVIEWER.model = model
    PREVIEWER.generate_model(0)
    PREVIEWER.generate_model(1)

PREVIEWER.graphic_engine.root.add_dock("Options", 300, 300, "left")
OPT_LAYOUT = LayoutWidget()
OPT_GEN_BUTTON = QtGui.QPushButton('Generate FLASH Model')
OPT_LOAD_BUTTON = QtGui.QPushButton('Load FLASH Model')

OPT_GEN_BUTTON.clicked.connect(generate_flash_file)
OPT_LOAD_BUTTON.clicked.connect(load_flash_file)

OPT_LAYOUT.addWidget(OPT_GEN_BUTTON, row=0, col=0)
OPT_LAYOUT.addWidget(OPT_LOAD_BUTTON, row=1, col=0)

PREVIEWER.graphic_engine.root.add_to_dock(-1, OPT_LAYOUT)

PREVIEWER.add_widget("Animated Preview", "left")  # Widget 0
PREVIEWER.add_widget("Finished Preview", "right")  # Widget 1

A_TIMER = QtCore.QTimer()
A_TIMER.timeout.connect(PREVIEWER.update_animated)
A_TIMER.start(1000)


F_TIMER = QtCore.QTimer()
F_TIMER.timeout.connect(PREVIEWER.update_frozen)
F_TIMER.start(50)

def change_animated_speed(sb):
    """Change the update speed of the animated display

    Arguments:
        sb {float} -- Interval in seconds
    """

    A_TIMER.setInterval(sb.value()*1000)

OPT_LABEL = QtGui.QLabel('Change animation speed')
OPT_LAYOUT.addWidget(OPT_LABEL, row=2, col=0)
OPT_SPEED_SPINNER = SpinBox(value=1, step=0.1, bounds=[0.1, 5])
OPT_SPEED_SPINNER.sigValueChanging.connect(change_animated_speed)
OPT_LAYOUT.addWidget(OPT_SPEED_SPINNER, row=2, col=1)


PREVIEWER.graphic_engine.root.window.show()

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
