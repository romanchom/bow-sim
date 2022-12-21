from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from model import Model
from cam import Cam, Axis
from cable import Cable, CablePiece, CableAttachment
from spring import Spring
from collections import deque
import numpy as np

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
force_curve = deque()
def update():
    global i
    draw_length = (i % 120) * 5
    i += 1
    nock.position[0] = -(200 + draw_length)
    model.relaxate()
    string_force = model.solve()[0]
    arrow_force = main_string_piece.cable_direction[0] * string_force
    force_curve.append((draw_length, arrow_force))
    if len(force_curve) > 150:
        force_curve.popleft()

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

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_STRIP)
    for dl, f in force_curve:
        glVertex2f(-dl, f)
    glEnd()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(update)

model = Model()

cam_axis = Axis((-120., 400.))
model.add_component(cam_axis)

def elipse(sides, minor, ecc, start = 0):
    def radius(angle):
        return minor * (1 - ecc * ecc) / (1 + ecc * math.cos(angle))
    return [radius(angle + start) for angle in np.linspace(0, math.tau, num=sides, endpoint=False)]

sides = 40

main_cam = Cam(cam_axis, math.pi * -0.8, elipse(sides, 60., 0.5, math.pi * 0.9), 1.)
model.add_component(main_cam)

aux_cam = Cam(cam_axis, 0.3, elipse(sides, 20., 0.5, math.pi * 0.8), -1.)
model.add_component(aux_cam)

nock = CableAttachment((-200., 0.))
main_string_piece = CablePiece(nock, main_cam)
model.add_component(main_string_piece)

main_string = Cable('string', (main_string_piece,))
model.add_component(main_string)

aux_cable_piece = CablePiece(CableAttachment((-100., 0.)), aux_cam)
model.add_component(aux_cable_piece)

aux_cable = Cable('cable', (aux_cable_piece,))
model.add_component(aux_cable)

spring = Spring('spring', main_cam, 10., (-120., 600.0), (0.0, 1.0))
model.add_component(spring)

model.init()

update()

glutMainLoop()
