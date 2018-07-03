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
coordinates = [
    [3, 3, 1, 1],
    [10, 10, 5, 0],
    [0, 0, 1, 0]
]

for pos in range(len(coordinates)):
    #write each number on a new line
    if coordinates[pos][3] == 1:
        coordinates.insert(pos, [-9, 1, 15, 0])
        coordinates.insert(pos, [-9, 1, 15, 0])
        coordinates.insert(pos, [-9, 1, 15, 4])
    elif coordinates[pos][3] == 2:
        coordinates.insert(pos, [-9, 6, 15, 0])
        coordinates.insert(pos, [-9, 6, 15, 0])
        coordinates.insert(pos, [-9, 6, 15, 4])
    elif coordinates[pos][3] == 3:
        coordinates.insert(pos, [-9, 12, 15, 0])
        coordinates.insert(pos, [-9, 12, 15, 0])
        coordinates.insert(pos, [-9, 12, 15, 4])
        

model = open('./coordinates/model.rtf', 'w')

model.write("{:.4f}".format(len(coordinates))+chr(13))
for axes in range(4):
    for pos in coordinates:
        #write each number on a new line
        model.write("{:.4f}".format(pos[axes])+chr(13))

model.close()