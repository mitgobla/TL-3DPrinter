from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import pywavefront
import os

app = QtGui.QApplication([])
widget = gl.GLViewWidget()
widget.opts['distance'] = 20
widget.show()
widget.setWindowTitle('Lil Timmy 3D Printing Preview')


script_dir = os.path.dirname(os.path.realpath(__file__))

grid = gl.GLGridItem()
widget.addItem(grid)
objfile = "C:\\Users\\mitgobla\\Documents\\Python\\Team Lightning\\Technocamps 2018\\TL-3DPrinter\\lego-print\\resources\\LegoBrick.obj"
mesh = pywavefront.Wavefront(objfile)

#box = gl.GLBoxItem(size=None, color=(255,0,255,155), glOptions='opaque')
#box.translate(0, 0, 0)
brickvertexes = mesh.mesh_list[0].materials[0].vertices
brickmesh = gl.MeshData(vertexes=brickvertexes)
brick = gl.GLMeshItem(meshdata=mesh, color=(255, 0, 0, 80), drawEdges=True)
widget.addItem(brick)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
