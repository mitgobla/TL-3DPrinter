from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

app = QtGui.QApplication([])
widget = gl.GLViewWidget()
widget.show()
widget.setWindowTitle('Team Lightning Lego Model Preview')
widget.setCameraPosition(distance=40)

grid = gl.GLGridItem()
grid.scale(1,1,1)
widget.addItem(grid)

verts = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],

    [0, 0, 0],
    [0, 1, 0],
    [1, 1, 0],
])
faces = np.array([
    [0, 1, 2],
    [0, 1, 3],
    [0, 2, 3],
    [1, 2, 3]
])
colors = np.array([
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 1, 0, 1]
])

## Mesh item will automatically compute face normals.
m1 = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False)
m1.translate(5, 5, 0)
#m1.setGLOptions('additive')
widget.addItem(m1)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
