"""
Title: Team Lightning EV3 Printer Code Previewer
Author: Ben Dodd (mitgobla)
Email: ben-dodd@outlook.com
Website: http://www.team-lightning.ga
"""
import os

import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.dockarea import *
from pyqtgraph import mkColor
from pyqtgraph.Qt import QtCore, QtGui

app = QtGui.QApplication([])
window = QtGui.QMainWindow()
area = DockArea()

window.setCentralWidget(area)
window.resize(1000, 500)
window.setWindowTitle('3D Printing Preview')

dock_one = Dock("Printing Preview", size=(500, 300))
area.addDock(dock_one, 'left')

widget = gl.GLViewWidget()
widget.opts['distance'] = 20
widget.show()
widget.setWindowTitle('Lil Timmy 3D Printing Preview')
dock_one.addWidget(widget)
widget.setBackgroundColor(mkColor(155, 155, 155, 0))
script_dir = os.path.dirname(os.path.realpath(__file__))

grid = gl.GLGridItem(size=QtGui.QVector3D(12, 13, 1))
grid.translate(6, 6.5, 0)
widget.addItem(grid)


def brick(x, y, z, blocktype):
    """Add a brick to the scene

    Arguments:
        x {int} -- Block x from home
        y {int} -- Block y from home
        z {int} -- Block z from home
        blocktype {int} -- Block colour
            0 -- movement
            1 -- red
            2 -- blue
            3 -- yellow
    """
    verts_box = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1]],
                         dtype=float)

    faces_box = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [0, 1, 4],
        [1, 5, 4],
        [1, 2, 5],
        [2, 5, 6],
        [2, 3, 6],
        [3, 6, 7],
        [0, 3, 7],
        [0, 4, 7],
        [4, 5, 7],
        [5, 6, 7],
    ])

    color_list = ()
    if blocktype == 1:
        color_list = (1, 0, 0, 0.8)
    elif blocktype == 2:
        color_list = (0, 0, 1, 0.8)
    elif blocktype == 3:
        color_list = (1, 1, 0, 0.8)

    # probably not needed
    #colors_box = np.array([
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #    [1, 1, 1, 0.5],
    #])
    # faceColors=colors_box
    box = gl.GLMeshItem(vertexes=verts_box, faces=faces_box,
                        color=color_list, glOptions='opaque', smooth=True)
    frame = gl.GLBoxItem(color=(0, 0, 0, 255))
    box.translate(x, y, z)
    frame.translate(x, y, z)
    widget.addItem(box)
    widget.addItem(frame)

extruder = gl.GLBoxItem(size=QtGui.QVector3D(0.5, 0.5, 8), color=(55, 155, 55, 255))
extruder.translate(1.25, 1.25, 0)
widget.addItem(extruder)
for blocks in range(4):
    brick(blocks, 0, 0, 3)
window.show()

index = 0
updown = True
def update():
    global index, updown
    if index >= 1:
        updown = False
    elif index <= 0:
        updown = True
    
    if updown:
        extruder.translate(0, 0, 0.1)
        index += 0.1
    else:
        extruder.translate(0, 0, -0.1)
        index -= 0.1

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(30)

timer.setInterval(100)
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
