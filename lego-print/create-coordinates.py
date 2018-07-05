"""
Title: Team Lightning EV3 Printer Code Generator
Author: Ben Dodd (mitgobla)
Co-Author: Thomas Woodthorpe (lonewolfdesign)
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
script_dir = os.path.dirname(os.path.realpath(__file__))

model_coordinates = [
    [1, 1, 1, 1], #Front of Box
    [3, 1, 1, 1],
    [5, 1, 1, 1],
    [7, 1, 1 , 1],
    [9, 1, 1, 1],
    [11, 1, 1, 1],  #Right Side of box
    [11, 3, 1, 1],
    [11, 5, 1, 1],
    [11, 7, 1, 1],
    [11, 9, 1, 1],
    [9, 9, 1, 1], #Top Side of box
    [7, 9, 1, 1],
    [5, 9, 1, 1],
    [3, 9, 1, 1],
    [1, 9, 1, 1], #Left side of box
    [1, 7, 1, 1],
    [1, 5, 1, 1],
    [1, 3, 1, 1]
]

coordinates = []
for pos in range(0, len(model_coordinates), 1):
    #write each number on a new line
    
    if model_coordinates[pos][3] == 1:
        coordinates.append([-4, 1, 1.2, 0]) #Red Brick Coord
    elif model_coordinates[pos][3] == 2:
        coordinates.append([-4, 7, 1.2, 0]) #Blue Brick Coord
    elif model_coordinates[pos][3] == 3:
        coordinates.append([-4, 13, 1.2, 0]) #Yellow Brick Coord
    coordinates.append(model_coordinates[pos])

#coordinates.reverse()
coord_file = open(script_dir+'\\coordinates\\coord.rtf', 'w')
coord_file.write(str(coordinates))
coord_file.close()
model = open(script_dir+'\\coordinates\\model.rtf', 'w')

model.write("{:.4f}".format(len(coordinates))+chr(13))
for axes in range(4):
    for pos in coordinates:
        #write each number on a new line
        model.write("{:.4f}".format(pos[axes])+chr(13))

model.close()
