import ctypes
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from ast import literal_eval

from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import Ui_MainWindow
import generator

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
APP_ID = "mitgobla.teamlightning.flash.alpha"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

class FileLoader:
    """Loads a text file of coordinates and colours
    """

    def __init__(self):
        self.window = tk.Tk()
        self.window.withdraw()
        self.window.wm_iconbitmap(SCRIPT_DIR+"\\bolt-icon.ico")
        self.file = None
        self.previous = None

    def load_txt(self):
        """Load the list of brick positions and colours
        """
        self.previous = self.file
        self.window.filename = filedialog.askopenfilename(
            initialdir=SCRIPT_DIR,
            title="Select Coordinate file",
            filetypes=[("Text Files", "*.txt")])
        self.file = self.window.filename
        if not self.file:
            self.file = self.previous
            return False
        return True

    def load_flash(self):
        """Load a FLASH file
        """
        self.previous = self.file
        self.window.filename = filedialog.askopenfilename(
            initialdir=SCRIPT_DIR,
            title="Select FLASH file",
            filetypes=[("FLASH Files", "*.flash")])
        self.file = self.window.filename
        if not self.file:
            self.file = self.previous
            return False
        return True

    @property
    def return_coordinates(self):
        """Convert FLASH to coordinates

        Returns:
            list -- Array of Lists [x, y, z, c]
        """

        return literal_eval(self.file)




class FileGenerator:

    def __init__(self):
        self.loader = FileLoader()

    def generate_flash_file(self):
        if self.loader.load_txt(): # Continue if a file was selected
            model = generator.Model(self.loader.file)
            if model.read(): # Continue if a valid model file
                generate = generator.Generate(model)
                generate.gen_model()
                generate.write_model()
                messagebox.showinfo("Completed", "FLASH file generated as model.flash")
            else:
                messagebox.showerror("Error", "Invalid model file.")

    def load_flash_file(self):
        if self.loader.load_flash():
            model_content = open(self.loader.file, "r")
            model = literal_eval(model_content.read())
            model_content.close()
            #PREVIEWER.model = model
            #PREVIEWER.generate_model(0)
            #PREVIEWER.generate_model(1)


LOADER = FileGenerator()

APP = QApplication(sys.argv)
WINDOW = QMainWindow()
UI = Ui_MainWindow()
UI.setupUi(WINDOW)

UI.actionOpen.triggered.connect(LOADER.load_flash_file)
UI.actionConvert.triggered.connect(LOADER.generate_flash_file)

WINDOW.show()
sys.exit(APP.exec_())
