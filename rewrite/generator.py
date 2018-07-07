"""
Title: FLASH Model Generator
Description: Converts coordinates into FLASH code.

Author: Ben Dodd (mitgobla)
Email: ben-dodd@outlook.com
Website: http://www.team-lightning.ga


Each position has 4 values:
    x: the x coordinate
    y: the y coordinate
    z: the z coordinate
    c: the block colour
    c = 0 - 3; 0 being none
        1: red
        2: blue
        3: yellow
"""

import os
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class Model:
    """Convert file to FLASH model format

    Arguments:
        path {file} -- File of model coordinates and colours
    """
    def __init__(self, path):
        """Convert file to FLASH model format

        Arguments:
            path {file} -- File of model coordinates and colours
        """
        self.file = None
        self.file_list = []
        self.coordinates = []
        self.model_path = path

    def read(self):
        """Read the given file.
        """
        self.file = open(self.model_path, "r")
        self.file_list = self.file.read().split('\n')
        self.file.close()
        for line in self.file_list:
            next_coords = line.split(', ')
            for pos in range(len(next_coords)):
                next_coords[pos] = float(next_coords[pos])
            self.coordinates.append(next_coords)

    @property
    def get_model(self):
        """Return the model coordinates
        """
        return self.coordinates



class Generate:
    """Generate print instructions from model coordinates

    Arguments:
        model {generator.Model} -- Model object
    """

    def __init__(self, model):
        """Generate print instructions from model coordinates

        Arguments:
            model {generator.Model} -- Model object
        """

        self.model_coordinates = []
        self.coordinates = []
        self.model = model

    def gen_model(self):
        """Generate the FLASH model
        """
        self.model_coordinates = self.model.get_model

        self.coordinates = []
        for pos in range(len(self.model_coordinates)):
            if self.model_coordinates[pos][3] == 1:
                self.coordinates.append([-4, 1, 1.2, 0]) #Red Brick Coord
            elif self.model_coordinates[pos][3] == 2:
                self.coordinates.append([-4, 7, 1.2, 0]) #Blue Brick Coord
            elif self.model_coordinates[pos][3] == 3:
                self.coordinates.append([-4, 13, 1.2, 0]) #Yellow Brick Coord
            self.coordinates.append(self.model_coordinates[pos])

    def write_model(self):
        """Write the FLASH file and the EV3 .rtf file
        """
        if not os.path.exists(SCRIPT_DIR+'\\coordinates'):
            os.makedirs(SCRIPT_DIR+'\\coordinates')

        flash_file = open(SCRIPT_DIR+'\\coordinates\\model.flash', 'w')
        flash_file.write(str(self.coordinates))
        flash_file.close()

        model_file = open(SCRIPT_DIR+'\\coordinates\\model.rtf', 'w')
        model_file.write("{:.4f}".format(len(self.coordinates))+chr(13))
        for axes in range(4):
            for pos in self.coordinates:
                #write each number on a new line
                model_file.write("{:.4f}".format(pos[axes])+chr(13))
        model_file.close()
