from model import Model
from cam import Cam, Axis
from cable import Cable, CablePiece, CableAttachment
from spring import Spring
import numpy as np
import math
from OpenGL.GL import *
import csv
import matplotlib.pyplot as plt

def elipse(sides, minor, ecc, start = 0):
    def radius(angle):
        return minor * (1 - ecc * ecc) / (1 + ecc * math.cos(angle))
    return [radius(angle - start) for angle in np.linspace(0, math.tau, num=sides, endpoint=False)]

def adjust_cam_radii(radii, center_index, adjustment):
    l = len(radii)
    adjustment_range = l // 2
    for i in range(1, adjustment_range):
        index = center_index - adjustment_range // 2 + i
        strength = (1 - math.cos(i / adjustment_range * math.tau)) / 2
        if not 0 <= index < l:
            continue
        radii[index] += adjustment * strength / l * 10.0

def normalize_cam(radii, target_circumference, alpha):
    avg = sum(radii) / len(radii)
    t = 0.99
    for i in range(len(radii)):
        radii[i] = radii[i] * t + avg * (1.0 - t)

    circ = 0
    ps = [np.array((math.cos(a), math.sin(a))) * r for r, a in zip(radii, np.linspace(0.0, math.tau, len(radii), endpoint=False))]
    for p0, p1 in zip(ps, ps[1:]):
        circ += np.linalg.norm(p0 - p1)
    error = target_circumference / circ

    for i in range(len(radii)):
        radii[i] *= error# - 1) * alpha)


def adjust_cam_radii2(radii, center_index, adjustment):
    radii[center_index] *= (1 + adjustment)

class Optimizer:
    def __init__(self):
        sides = 40
        main_geometry = elipse(sides, 50., 0.0, -math.pi * 0.7)
        aux_geometry = elipse(sides, 30., 0.0, -math.pi * 0.8)
        self.axle_to_center = 500.0
        self.max_draw = 600
        self.spring_stroke = 100
        self.make_model(main_geometry, aux_geometry)
        self.force_curve = {}
        self.draw_process = {}

    def make_model(self, main_geometry, aux_geometry):
        cam_axis = Axis((-120., self.axle_to_center))

        self.main_cam = Cam(cam_axis, math.pi * -0.6, main_geometry, 1.)

        self.aux_cam = Cam(cam_axis, math.pi * 0.25, aux_geometry, -1.)

        self.nock = CableAttachment((-200., 0.))
        self.main_string_piece = CablePiece(self.nock, self.main_cam)

        main_string = Cable('string', (self.main_string_piece,))

        self.aux_cable_piece = CablePiece(CableAttachment((-100., 0.)), self.aux_cam)

        aux_cable = Cable('cable', (self.aux_cable_piece,))

        spring = Spring('spring', self.main_cam, 3., (-120., self.axle_to_center + 150), (0.0, 1.0))

        components = [
            cam_axis,
            self.main_cam,
            self.aux_cam,
            self.main_string_piece,
            main_string,
            self.aux_cable_piece,
            aux_cable,
            spring,
        ]
        self.model = Model(components)

    def analyze_bow(self, cb):
        draw_lengths = np.linspace(0., self.max_draw, 31)

        for dl in draw_lengths:
            self.nock.position[0] = -(200 + dl)
            self.model.relaxate()
            string_force = self.model.solve()[0]
            arrow_force = self.main_string_piece.cable_direction[0] * string_force
            self.force_curve[dl] = arrow_force
            self.draw_process[dl] = {
                'm': self.main_string_piece.wrapped_index,
                'a': self.aux_cable_piece.wrapped_index,
            }
            if cb:
                cb()

    def export_force_curve(self):
        with open('force_curve.csv', 'w') as f:
            w = csv.writer(f)
            for i in self.force_curve.items():
                w.writerow(i)

    def plot_force_curve(self):
        plt.plot(self.force_curve.keys(), self.force_curve.values())
        plt.show()

    def optimize(self, target_curve, alpha):
        alpha = alpha / len(self.force_curve)
        for dl, actual_force in self.force_curve.items():
            target_force = target_curve[dl]
            process = self.draw_process[dl]
            error = target_force - actual_force
            main_contact_point = process['m']
            aux_contact_point = process['a']

            adjust_cam_radii(self.main_cam.radii, main_contact_point, -alpha * error)
            adjust_cam_radii(self.aux_cam.radii, aux_contact_point, alpha * error)

        main_t_circ = (math.sqrt(self.axle_to_center ** 2 + self.max_draw ** 2) - self.axle_to_center) * 1.5
        aux_t_circ = self.spring_stroke * 1.5

        # normalize_cam(self.main_cam.radii, main_t_circ, alpha)
        # normalize_cam(self.aux_cam.radii, aux_t_circ, alpha)

        main_geometry = self.main_cam.radii
        aux_geometry = self.aux_cam.radii
        self.make_model(main_geometry, aux_geometry)

        glColor3f(0.5, 1.0, 1.0)
        glBegin(GL_LINE_STRIP)
        for dl, f in target_curve.items():
            glVertex2f(-dl, f)
        glEnd()

    def draw(self):
        self.model.draw()
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_STRIP)
        for dl, f in self.force_curve.items():
            glVertex2f(-dl, f)
        glEnd()
