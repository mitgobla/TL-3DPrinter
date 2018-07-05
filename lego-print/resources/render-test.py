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

script_dir = os.path.dirname(os.path.realpath(__file__))

model = [
    [1, 3, 1, 1], #Front of Box
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
    [1, 11, 1, 1], #Left side of box
    [1, 9, 1, 1],
    [1, 7, 1, 1],
    [1, 5, 1, 1]
]

app = QtGui.QApplication([])
window = QtGui.QMainWindow()
area = DockArea()

window.setCentralWidget(area)
window.resize(1000, 500)
window.setWindowTitle('3D Printing Preview')

dock_one = Dock("Animated Preview", size=(500, 300))
dock_two = Dock("Finished Preview", size=(500, 300))
area.addDock(dock_one, 'left')
area.addDock(dock_two, 'right')

animated_preview_widget = gl.GLViewWidget()
animated_preview_widget.opts['distance'] = 20
animated_preview_widget.show()
preview_widget = gl.GLViewWidget()
preview_widget.opts['distance'] = 20
preview_widget.show()


dock_one.addWidget(animated_preview_widget)
dock_two.addWidget(preview_widget)

animated_preview_widget.setBackgroundColor(mkColor(155, 155, 155, 0))
preview_widget.setBackgroundColor(mkColor(155, 155, 155, 0))

grid = gl.GLGridItem(size=QtGui.QVector3D(12, 13, 1))
grid.setSpacing(spacing=QtGui.QVector3D(0.5, 0.5, 0.5))
grid.translate(6.5, 7, 0)
animated_preview_widget.addItem(grid)
preview_widget.addItem(grid)


x_verts_line = np.array([
    [0, 0, 0],
    [2, 0, 0]
])

y_verts_line = np.array([
    [0, 0, 0],
    [0, 2, 0]
])

z_verts_line = np.array([
    [0, 0, 0],
    [0, 0, 2]
])

axis_color_line = np.array([
    [1, 0, 0, 1],
    [1, 0, 0, 1]
])

x_line = gl.GLLinePlotItem(pos=x_verts_line, color=axis_color_line, width=2, antialias=True)
x_line.translate(0.5, 0.5, 0)
y_line = gl.GLLinePlotItem(pos=y_verts_line, color=axis_color_line, width=2, antialias=True)
y_line.translate(0.5, 0.5, 0)
z_line = gl.GLLinePlotItem(pos=z_verts_line, color=axis_color_line, width=2, antialias=True)
z_line.translate(0.5, 0.5, 0)
animated_preview_widget.addItem(x_line)
animated_preview_widget.addItem(y_line)
animated_preview_widget.addItem(z_line)

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
    animated_preview_widget.addItem(box)
    preview_widget.addItem(box)
    animated_preview_widget.addItem(frame)
    preview_widget.addItem(frame)

extruder = gl.GLBoxItem(size=QtGui.QVector3D(0.5, 0.5, 8), color=(55, 155, 55, 255))
extruder.translate(1.25, 1.25, 0)
animated_preview_widget.addItem(extruder)
for pos in model:
    brick(pos[0]/2, pos[1]/2, pos[2]-1, pos[3])
window.show()

index = 0
rotation = 0
updown = True
def update():
    global index, updown, rotation
    if index >= 1:
        updown = False
    elif index <= 0:
        updown = True
    
    if rotation >= 360:
        rotation = 0
    

    preview_widget.opts['center'] = QtGui.QVector3D(6.5, 6.5, 0)
    preview_widget.setCameraPosition(elevation=25, azimuth=rotation)
    rotation += 0.5

    if updown:
        extruder.translate(0, 0, 0.1)
        index += 0.1
    else:
        extruder.translate(0, 0, -0.1)
        index -= 0.1

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(30)

#timer.setInterval(100)
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
