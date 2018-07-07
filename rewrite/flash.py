"""
Title: FLASH
Description: 3D Preview software for models to be printed on
             Team Lightning 3D printers.

Author: Ben Dodd (mitgobla)
Email: ben-dodd@outlook.com
Website: http://www.team-lightning.ga
"""

import os

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
        self.window.filename = filedialog.askopenfilename(initialdir = SCRIPT_DIR, title = "Select Coordinate file", filetypes = [("Text Files", "*.txt")])
        self.file = self.window.filename
        if not self.file:
            print("No File Selected, aborting")
            exit(0)

    def load_flash(self):
        """Load a FLASH file
        """
        self.window.filename = filedialog.askopenfilename(initialdir = SCRIPT_DIR, title = "Select FLASH file", filetypes = [("FLASH Files", "*.flash")])
        self.file = self.window.filename
        if not self.file:
            print("No File Selected, aborting")
            exit(0)

LOADER = FileLoader()
LOADER.load_txt()
MODEL = generator.Model(LOADER.file)
MODEL.read()
GENERATOR = generator.Generate(MODEL)
GENERATOR.gen_model()
GENERATOR.write_model()


