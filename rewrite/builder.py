"""
Title: FLASH Model Builder
Description: Converts a user built model into FLASH code.

Author: Ben Dodd (mitgobla)
Email: ben-dodd@outlook.com
Website: http://www.team-lightning.ga
"""

import ctypes
import os
import tkinter as tk
from tkinter import filedialog, messagebox

import numpy as np
import pyqtgraph.dockarea as qtdk
import pyqtgraph.opengl as gl
from pyqtgraph import mkColor, LayoutWidget, ColorButton
from pyqtgraph.Qt import QtCore, QtGui

import flash
import generator

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
APP_ID = "mitgobla.teamlightning.flashbuilder.alpha"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

class Preview:
    """Class for updating previews
    """

    def __init__(self):
        self.graphic_engine = flash.Graphics()

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



PREVIEWER = Preview()
PREVIEWER.add_widget("Preview Window", "left")

CONTROL_LAYOUT = LayoutWidget()


PREVIEWER.graphic_engine.root.add_dock("Controls", 150, 300, "left")
PREVIEWER.graphic_engine.root.add_to_dock(-1, None) #CHANGE NONE TO A LAYOUT ASAP!!!!

PREVIEWER.graphic_engine.root.window.show()

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
