"""
Title: Team Lig)htning EV3 Printer Code Generator
Author: Ben Dodd (mitgobla)
Co-Author: Thomas Woodthorpe (lonewolfdesign)
Email: ben-dodd@outlook.com
Website: http://www.team-lightning.ga


Each position has 4 values:
    x: the x coordinate
    y: the y coordinate
    z: the z coordinate
    c: z hop
        4: hop
        anything else: nothing
"""
model_coordinates = [
    [0, 0, 0, 0], #Letter: T
    [5, 0, 0, 0],
    [2.5, 0 , 1, 0],
    [2.5, 0 , 0 , 0],
    [2.5, -7, 0, 1],
    
    [12, -7, 1, 0], #E
    [12, -7 ,0 ,0],
    [7, -7 , 0, 0],
    [7, -3.5, 0, 0],
    [12, -3.5, 0, 0],
    [7, -3.5, 1, 0],
    [7, -3.5, 0, 0],
    [7, 0, 0, 0],
    [12, 0, 0, 2],

    [19, 0, 1, 0], #C
    [19, 0, 0, 0],
    [14, 0, 0, 0],
    [14, -7, 0, 0],
    [19, -7, 0, 0],
    [21, -7, 1, 3],

    [21, -7, 0, 0], #H
    [21, 0, 0, 0],
    [21, -3.5, 1, 0],
    [21, -3.5, 0, 0],
    [26, -3.5, 0, 0],
    [26, 0, 1, 0],
    [26, 0, 0, 0],
    [26, -7, 0, 4],

    [28, -7, 1, 0], #N
    [28, -7, 0, 0],
    [28, 0, 0, 0],
    [33, 0, 0, 0],
    [33, -7, 0, 5],

    [35, -7, 1, 0], #O
    [35, -7, 0, 0],
    [35, 0, 0, 0],
    [40, 0, 0, 0],
    [40, -7, 0, 0],
    [32, -7, 0, 6]
]

coordinates = []
for pos in range(0, len(model_coordinates), 1):
    #write each number on a new line
    
#    if model_coordinates[pos][3] == 1:
#        coordinates.append([-10, 1, 1.2, 0]) #Red Brick Coord
#        print("red")
#    elif model_coordinates[pos][3] == 2:
#        coordinates.append([-10, 7, 1.2, 0]) #Blue Brick Coord
#        print("blue")
#    elif model_coordinates[pos][3] == 3:
#        coordinates.append([-10, 13, 1.2, 0]) #Yellow Brick Coord
#        print("yellow")
    coordinates.append(model_coordinates[pos])

#coordinates.reverse()
print(coordinates)
model = open('./coordinates/model.rtf', 'w')

model.write("{:.4f}".format(len(coordinates))+chr(13))
for axes in range(4):
    for pos in coordinates:
        #write each number on a new line
        model.write("{:.4f}".format(pos[axes])+chr(13))

model.close()