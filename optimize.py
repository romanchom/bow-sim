from optimizer import Optimizer
import csv
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def load_force_curve(file_name):
    with open(file_name) as f:
        r = csv.reader(f)
        return {float(dl): float(f) for dl, f in r}


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


def showScreen():
    coordAxes()
    optimizer.draw()

    glutSwapBuffers()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-950.0, 50, -50.0, 950, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

target_curve = load_force_curve('target_curve.csv')

optimizer = Optimizer()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL Coding Practice")

for i in range(1000):
    optimizer.analyze_bow(showScreen if i % 20 == 19 else None)
    optimizer.optimize(target_curve, 0.5 + i * 0.02)
    showScreen()

