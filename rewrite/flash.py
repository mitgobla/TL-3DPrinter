"""
Title: FLASH
Description: 3D Preview software for models to be printed on
             Team Lightning 3D printers.

Author: Ben Dodd (mitgobla)
Email: ben-dodd@outlook.com
Website: http://www.team-lightning.ga
"""

import os

from ast import literal_eval
import numpy as np
import pyqtgraph.dockarea as qtdk
import pyqtgraph.opengl as gl
from pyqtgraph import mkColor
from pyqtgraph.Qt import QtCore, QtGui
import tkinter as tk
from tkinter import filedialog
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
            initialdir=SCRIPT_DIR, title="Select Coordinate file", filetypes=[("Text Files", "*.txt")])
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

        self.current_position = (0,0,0)
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




LOADER = FileLoader()
LOADER.load_txt()
MODEL = generator.Model(LOADER.file)
MODEL.read()
GENERATOR = generator.Generate(MODEL)
GENERATOR.gen_model()
GENERATOR.write_model()
