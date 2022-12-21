import math
import numpy as np
from OpenGL.GL import *

def sincos(a):
    return np.array((math.cos(a), math.sin(a)))

class Axis:
    def __init__(self, position):
        self.position = np.array(position)
        self.angle = 0.0
        self.position_adjustment = np.array((0., 0.))
        self.angle_adjustment = 0

    def update(self):
        alpha = 0.5
        self.position += self.position_adjustment * alpha
        self.angle += self.angle_adjustment * alpha
        self.position_adjustment = np.array((0., 0.))
        self.angle_adjustment = 0

class Cam:
    def __init__(self, axis, angleOffset, radii, direction):
        self.axis = axis
        self.radii = radii
        self.angleOffset = angleOffset
        self.direction = direction
        self.points = []
        self.update()

    def update(self):
        self.points.clear()
        angle = self.axis.angle + self.angleOffset
        for i, r in enumerate(self.radii):
            a = self.direction * i * math.tau / len(self.radii) + angle
            normal = sincos(a)
            self.points.append(self.axis.position + normal * r)

    def draw(self):
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_STRIP)
        glVertex2f(*self.axis.position)
        for p in self.points:
            glVertex2f(*p)
        glEnd()