import numpy as np
from OpenGL.GL import *
import sympy

def angle_to(a, p):
    diff = p - a
    angle = np.arctan2(diff[1], diff[0])
    return angle

class Cable:
    def __init__(self, name, anchor, cam, target_length):
        self.anchor = np.array(anchor)
        self.cam = cam
        self.target_length = target_length
        self.cam_anchor = np.array((0, 0))

        self.tension = sympy.symbols(name)

        self.update()

    def update(self):
        self.wrapped_index, self.cam_anchor = max(enumerate(self.cam.points), key=lambda p: self.cam.direction * angle_to(self.anchor, p[1]))
        self.cable_direction = self.cam_anchor - self.anchor
        self.straight_length = np.linalg.norm(self.cable_direction)
        self.cable_direction /= self.straight_length
        lever_arm = self.cam_anchor - self.cam.axis.position
        self.lever = np.cross(lever_arm, self.cable_direction)
        self.wrapped_length = 0.0
        for p0, p1 in zip(self.cam.points[:self.wrapped_index], self.cam.points[1:]):
            self.wrapped_length += np.linalg.norm(p0 - p1)
        self.total_cable_length = self.wrapped_length + self.straight_length


    def apply_constraint(self):
        error = self.target_length - self.total_cable_length
        self.cam.axis.angle_adjustment += error / self.lever * 0.5
        self.cam.axis.position_adjustment += error * self.cable_direction * 0.5
        return abs(error)

    def draw(self):
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
        for p in self.cam.points[:self.wrapped_index + 1]:
            glVertex2f(*p)
        glVertex2f(*self.anchor)
        glEnd()

    def force(self):
        return (
            self.tension * self.cable_direction[0],
            self.tension * self.cable_direction[1],
        )

    def torque(self):
        return self.tension * self.lever


