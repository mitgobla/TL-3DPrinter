"""
Title: Team Lightning EV3 Printer Code Generator
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
    [1, 2, 3, 0],
    [2, 3, 4, 5]
]

xfile = open('./coordinates/x.rtf', 'w')
yfile = open('./coordinates/y.rtf', 'w')
zfile = open('./coordinates/z.rtf', 'w')
cfile = open('./coordinates/c.rtf', 'w')

for [x, y, z, c] in coordinates:
    #write each number on a new line
    xfile.write("{:.4f}".format(x)+chr(13))
    yfile.write("{:.4f}".format(y)+chr(13))
    zfile.write("{:.4f}".format(z)+chr(13))
    cfile.write("{:.4f}".format(c)+chr(13))

xfile.close()
yfile.close()
zfile.close()
cfile.close()