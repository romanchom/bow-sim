from model import Model
from cam import Cam, Axis
from cable import Cable, CablePiece, CableAttachment
from spring import Spring
import numpy as np
import math
from OpenGL.GL import *


def elipse(sides, minor, ecc, start = 0):
    def radius(angle):
        return minor * (1 - ecc * ecc) / (1 + ecc * math.cos(angle))
    return [radius(angle - start) for angle in np.linspace(0, math.tau, num=sides, endpoint=False)]

class Optimizer:
    def __init__(self):
        cam_axis = Axis((-120., 400.))

        sides = 40

        main_cam = Cam(cam_axis, math.pi * -0.6, elipse(sides, 70., 0.7, -math.pi * 0.7), 1.)

        aux_cam = Cam(cam_axis, 0.3, elipse(sides, 25., 0.6, -math.pi * 0.8), -1.)

        self.nock = CableAttachment((-200., 0.))
        self.main_string_piece = CablePiece(self.nock, main_cam)

        main_string = Cable('string', (self.main_string_piece,))

        aux_cable_piece = CablePiece(CableAttachment((-100., 0.)), aux_cam)

        aux_cable = Cable('cable', (aux_cable_piece,))

        spring = Spring('spring', main_cam, 3., (-120., 450.0), (0.0, 1.0))

        components = [
            cam_axis,
            main_cam,
            aux_cam,
            self.main_string_piece,
            main_string,
            aux_cable_piece,
            aux_cable,
            spring,
        ]
        self.model = Model(components)
        self.i = 0
        self.force_curve = {}

    def do_stuff(self):
        draw_length = (self.i % 120) * 5
        self.i += 1
        self.nock.position[0] = -(200 + draw_length)
        self.model.relaxate()
        string_force = self.model.solve()[0]
        arrow_force = self.main_string_piece.cable_direction[0] * string_force
        self.force_curve[draw_length] = arrow_force

    def draw(self):
        self.model.draw()
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_STRIP)
        for dl, f in self.force_curve.items():
            glVertex2f(-dl, f)
        glEnd()
