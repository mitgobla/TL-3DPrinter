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

    def __init__(self):
        self.app = QtGui.QApplication([])
        self.window = QtGui.QMainWindow()
        self.area = qtdk.DockArea()

        self.window.setCentralWidget(self.area)
        self.window.resize(1000, 500)
        self.window.setWindowTitle('FLASH - LEGO 3D Printer Software')

        self.docks = []
        self.widgets = []

    def add_dock(self, title, x, y, position):
        """Add a dock to the window

        Arguments:
            title {string} -- Title of the dock
            x {int} -- Width
            y {int} -- Height
            position {string} -- Grid position
        """

        self.docks.append(qtdk.Dock(title, size=(x, y)))
        self.area.addDock(self.docks[-1], position)

    def add_gl_widget(self):
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


LOADER = FileLoader()
LOADER.load_txt()
MODEL = generator.Model(LOADER.file)
MODEL.read()
GENERATOR = generator.Generate(MODEL)
GENERATOR.gen_model()
GENERATOR.write_model()
