from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from optimizer import Optimizer

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


force_curve = {}
def update():
    optimizer.do_stuff()
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
    optimizer.draw()

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(update)

optimizer = Optimizer()

update()

glutMainLoop()
