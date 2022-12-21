from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
from bow import Bow

def coordAxes():
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINE_STRIP)
    glVertex2f(0, 0)
    glVertex2f(500, 0)
    glEnd()
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINE_STRIP)
    glVertex2f(0, 0)
    glVertex2f(0, 500)
    glEnd()


i = 0
def update():
    t = time.time() - start_time
    global i
    model.draw_length = (i % 120) * 5
    model.relaxate(0.5)
    model.solve()

    i += 1
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-950.0, 50, -50.0, 950, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    coordAxes()
    model.draw()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(update)

start_time = time.time()
model = Bow()

glutMainLoop()
