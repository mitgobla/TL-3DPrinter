import pyglet
from pyglet.gl import *

win = pyglet.window.Window()
glClearColor(0.2, 0.1, 0, 1)
@win.event
def on_draw():
    #Clear Buffers
    glClear(GL_COLOR_BUFFER_BIT)
    
    #Draw stuff
    #Vertex2 is a 2d coordinate system
    #   i: integer
    #   f: float
    #Vertex3 is a 3d coordinate system
    #
    #glBegin:
    #   GL_POINTS creates dots at coordinates
    #   GL_LINES joines these coordinates together in pairs (first two join)
    #   GL_LINES_STRIP joines these coordiantes in dot-to-dot
    #   GL_LINE_LOOP does the same as above, and draws line from first to last vertex
    #   GL_TRIANGLES to be used with glPolygonMode
    #

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glBegin(GL_TRIANGLES)
    glVertex2i(50, 50)
    glVertex2i(75, 100)
    glVertex2i(200, 200)
    glEnd()

pyglet.app.run()
