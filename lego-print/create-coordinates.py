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
model_coordinates = [
    [0, 3, 1, 1], #Front of Box
    [3, 3, 1, 1],
    [5, 3 , 1, 1],
    [7, 3 , 1 , 1],
    [9, 3 , 1, 1],
    [11, 3, 1, 1],  #Right Side of box
    [11, 5, 1, 1],
    [11, 7, 1, 1],
    [11, 9, 1, 1],
    [11, 11, 1, 1],
    [9, 11, 1, 1], #Top Side of box
    [7, 11, 1, 1],
    [5, 11, 1, 1],
    [3, 11, 1, 1],
    [0, 11, 1, 1], #Left side of box
    [0, 9, 1, 1],
    [0, 7, 1, 1],
    [0, 5, 1, 1],
    
    #[3, 3, 2, 2],
    #[3, 3, 3, 3],
    #[3, 3, 4, 2],
    #[3, 3, 5, 1],
    #[3, 3, 7, 0]
]

coordinates = []
for pos in range(0, len(model_coordinates), 1):
    #write each number on a new line
    
    if model_coordinates[pos][3] == 1:
        coordinates.append([-10, 1, 1.2, 0]) #Red Brick Coord
        print("red")
    elif model_coordinates[pos][3] == 2:
        coordinates.append([-10, 7, 1.2, 0]) #Blue Brick Coord
        print("blue")
    elif model_coordinates[pos][3] == 3:
        coordinates.append([-10, 13, 1.2, 0]) #Yellow Brick Coord
        print("yellow")
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