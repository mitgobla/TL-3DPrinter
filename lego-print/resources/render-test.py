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
    [-4, 1, 1.2, 0],
    [1, 1, 1, 1],
    [-4, 1, 1.2, 0],
    [3, 1, 1, 1],
    [-4, 1, 1.2, 0],
    [5, 1, 1, 1],
    [-4, 1, 1.2, 0],
    [7, 1, 1, 1],
    [-4, 1, 1.2, 0],
    [9, 1, 1, 1],
    [-4, 1, 1.2, 0],
    [11, 1, 1, 1],
    [-4, 1, 1.2, 0],
    [11, 3, 1, 1],
    [-4, 1, 1.2, 0],
    [11, 5, 1, 1],
    [-4, 1, 1.2, 0],
    [11, 7, 1,1],
    [-4, 1, 1.2, 0],
    [11, 9, 1, 1],
    [-4, 1, 1.2, 0],
    [9, 9, 1, 1],
    [-4, 1, 1.2, 0],
    [7, 9, 1, 1],
    [-4, 1, 1.2, 0],
    [5, 9, 1, 1],
    [-4, 1, 1.2, 0],
    [3, 9, 1, 1],
    [-4, 1, 1.2, 0],
    [1, 9, 1, 1],
    [-4, 1, 1.2, 0],
    [1, 7, 1, 1],
    [-4, 1, 1.2, 0],
    [1, 5, 1, 1],
    [-4, 1, 1.2, 0],
    [1, 3, 1, 1]
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

grid = gl.GLGridItem(size=QtGui.QVector3D(8, 9, 1))
grid.setSpacing(spacing=QtGui.QVector3D(0.5, 0.5, 0.5))
grid.translate(4.5, 5, 0)
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

x_line = gl.GLLinePlotItem(
    pos=x_verts_line, color=axis_color_line, width=2, antialias=True)
x_line.translate(0.5, 0.5, 0)
y_line = gl.GLLinePlotItem(
    pos=y_verts_line, color=axis_color_line, width=2, antialias=True)
y_line.translate(0.5, 0.5, 0)
z_line = gl.GLLinePlotItem(
    pos=z_verts_line, color=axis_color_line, width=2, antialias=True)
z_line.translate(0.5, 0.5, 0)
animated_preview_widget.addItem(x_line)
animated_preview_widget.addItem(y_line)
animated_preview_widget.addItem(z_line)
preview_widget.addItem(x_line)
preview_widget.addItem(y_line)
preview_widget.addItem(z_line)

extruder = gl.GLBoxItem(size=QtGui.QVector3D(
    0.5, 0.5, 8), color=(55, 155, 55, 255))
extruder.translate(0.25, 0.25, 0)
animated_preview_widget.addItem(extruder)

def brick(x, y, z, blocktype, screen):
    global extruder
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
        screen {int} -- Screen
            0 -- both
            1 -- preview
            2 -- animated
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
    no_skip_block = True
    if blocktype == 0:
        no_skip_block = False
    elif blocktype == 1:
        color_list = (1, 0, 0, 0.8)
    elif blocktype == 2:
        color_list = (0, 0, 1, 0.8)
    elif blocktype == 3:
        color_list = (1, 1, 0, 0.8)

    if no_skip_block:
        box = gl.GLMeshItem(vertexes=verts_box, faces=faces_box,
        color=color_list, glOptions='translucent', smooth=True)
        frame = gl.GLBoxItem(color=(0, 0, 0, 255))
        box.translate(x, y, z)
        frame.translate(x, y, z)

    if screen == 0:
        if no_skip_block:
            animated_preview_widget.addItem(box)
            preview_widget.addItem(box)
            animated_preview_widget.addItem(frame)
            preview_widget.addItem(frame)

        if extruder in animated_preview_widget.items:
            animated_preview_widget.removeItem(extruder)
        extruder = gl.GLBoxItem(size=QtGui.QVector3D(
        0.5, 0.5, 8), color=(55, 155, 55, 255))
        extruder.translate(x+0.25, y+0.25, z+1)
        animated_preview_widget.addItem(extruder)
    elif screen == 1:
        if no_skip_block:
            preview_widget.addItem(box)
            preview_widget.addItem(frame)
        else:
            pass
    elif screen == 2:
        if no_skip_block:
            animated_preview_widget.addItem(box)
            animated_preview_widget.addItem(frame)

        if extruder in animated_preview_widget.items:
            animated_preview_widget.removeItem(extruder)
        extruder = gl.GLBoxItem(size=QtGui.QVector3D(
                                0.5, 0.5, 8), color=(55, 155, 55, 255))
        extruder.translate(x+0.25, y+0.25, z+1)
        animated_preview_widget.addItem(extruder)






brick(-2, 0.5, 0.2, 1, 0)
brick(-2, 3.5, 0.2, 2, 0)
brick(-2, 6.5, 0.2, 3, 0)

for pos in model:
    brick(pos[0]/2, pos[1]/2, pos[2]-1, pos[3], 1)
window.show()

index = 1
rotation = 0

current_x, current_y, current_z = 0, 0, 0
def update_animated():
    global index, model, current_x, current_y, current_z, grid
    if index == len(model):
        index = 1
        for item in animated_preview_widget.items:
            animated_preview_widget.items.remove(item)
            item._setView(None)
        
        animated_preview_widget.items = []
        animated_preview_widget.update()
        brick(-2, 0.5, 0.2, 1, 2)
        brick(-2, 3.5, 0.2, 2, 2)
        brick(-2, 6.5, 0.2, 3, 2)
        animated_preview_widget.addItem(grid)


    #if index == 1:
    #    current_x = 0
    #    current_y = 0
    #    current_z = 0
    #else:
    #    current_x = model[index-1][0]/2
    #    current_y = model[index-1][1]/2 
    #    current_z = model[index-1][2]/2

    #x_dif = model[index][0]/2 - current_x/2

    #y_dif = model[index][1]/2 - current_y/2

    #z_dif = model[index][2]/2 - current_z/2

    #extruder.translate((x_dif)+0.75, (y_dif)+0.75, z_dif)
    #extruder["position"] = QtGui.QVector3D((model[index][0]/2)+0.5, (model[index][1]/2)+0.5, model[index][2])
    if model[index][3] == 0:
        brick(model[index][0]/2, model[index][1]/2, model[index][2]-1, 0, 2)
    elif model[index][3] == 1:
        brick(model[index][0]/2, model[index][1]/2, model[index][2]-1, 1, 2)
    elif model[index][3] == 2:
        brick(model[index][0]/2, model[index][1]/2, model[index][2]-1, 2, 2)
    elif model[index][3] == 3:
        brick(model[index][0]/2, model[index][1]/2, model[index][2]-1, 3, 2)

    index += 1

gl
def update_preview():
    global rotation
    if rotation >= 360:
        rotation = 0

    preview_widget.opts['center'] = QtGui.QVector3D(6.5, 6.5, 0)
    preview_widget.setCameraPosition(elevation=25, azimuth=rotation)
    rotation += 1


preview_timer = QtCore.QTimer()
preview_timer.timeout.connect(update_preview)
preview_timer.start(100)

animated_timer = QtCore.QTimer()
animated_timer.timeout.connect(update_animated)
animated_timer.start(300)

# timer.setInterval(100)
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
