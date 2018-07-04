"""
Title: Team Lig)htning EV3 Printer Code Generator
Author: Ben Dodd (mitgobla)
Email: ben-dodd@outlook.com
Website: http://www.team-lightning.ga
Each position has 4 values:
    x: the x coordinate
    y: the y coordinate
    z: the z coordinate
    c: the block colour
    c = 0 - 3; 0 being none
"""
model_coordinates = [
    [3, 3, 1, 1],
    [3, 3, 2, 2],
    [3, 3, 3, 3],
    [3, 3, 4, 2],
    [3, 3, 5, 1],
    [3, 3, 7, 0]
]

coordinates = []
for pos in range(0, len(model_coordinates), 1):
    #write each number on a new line

    if model_coordinates[pos][3] == 1:
        coordinates.append([-10, 1, 1.2, 0])
        print("red")
    elif model_coordinates[pos][3] == 2:
        coordinates.append([-10, 7, 1.2, 0])
        print("blue")
    elif model_coordinates[pos][3] == 3:
        coordinates.append([-10, 13, 1.2, 0])
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