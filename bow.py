from OpenGL.GL import *
from cam import Cam, Axis
from cable import Cable
from spring import Spring
import sympy
from collections import deque
import time

class Bow:
    def __init__(self):
        self.cam_axis = Axis((-120., 400.))
        self.main_cam = Cam(self.cam_axis, -2., 20, 60., 1.)
        self.aux_cam = Cam(self.cam_axis, 2., 20, 20., -1.)
        self.main_string = Cable('string', (-200., 0.), self.main_cam, 800.)
        self.aux_cable = Cable('cable', (-100., 0.), self.aux_cam, 400.)
        self.spring = Spring('spring', self.main_cam, 10., (-120., 600.0), (0.0, 1.0))
        self.draw_length = 0
        self.force_curve = deque()
        self.update()
        self.main_string.target_length = self.main_string.total_cable_length
        self.aux_cable.target_length = self.aux_cable.total_cable_length

    def relaxate(self, alpha):
        self.main_string.anchor[0] = -(200 + self.draw_length)
        threshold = 0.1
        for i in range(1000):
            stress = 0
            stress += self.spring.apply_constraint()
            stress += self.main_string.apply_constraint()
            stress += self.aux_cable.apply_constraint()
            self.cam_axis.adjust(alpha)
            self.update()
            if stress < threshold:
                break


    def update(self):
        self.main_cam.update()
        self.aux_cam.update()
        self.main_string.update()
        self.aux_cable.update()

    def draw(self):
        self.main_cam.draw()
        self.aux_cam.draw()
        self.main_string.draw()
        self.aux_cable.draw()
        self.spring.draw()
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_STRIP)
        for dw, f in self.force_curve:
            glVertex2f(-dw, f)
        glEnd()

    def solve(self):
        forces = [self.spring.force(), self.main_string.force(), self.aux_cable.force()]
        torques = [self.main_string.torque(), self.aux_cable.torque()]
        symbols = [self.spring.balancing_force, self.main_string.tension, self.aux_cable.tension]
        eqs = [
            sympy.Eq(sum(map(lambda f: f[0], forces)), 0),
            sympy.Eq(sum(map(lambda f: f[1], forces)), 0),
            sympy.Eq(sum(torques), 0)
        ]
        solution = list(sympy.linsolve(eqs, symbols))[0]
        force = solution[1] * self.main_string.cable_direction[0]
        self.force_curve.append((self.draw_length, force))
        if len(self.force_curve) > 200:
            self.force_curve.popleft()

