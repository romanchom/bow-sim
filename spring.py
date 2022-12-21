from OpenGL.GL import *
import numpy as np
import sympy

class Spring:
    def __init__(self, name, cam, stiffness, position, direction):
        self.cam = cam
        self.stiffness = stiffness
        self.position = position
        d = np.array(direction)
        self.direction = d / np.linalg.norm(d)

        self.balancing_force = sympy.symbols(name)


    def apply_constraint(self):
        diff = self.cam.axis.position - self.position
        dot = np.dot(diff, self.direction)
        wanted_pos = self.position + dot * self.direction
        pos_fixup = wanted_pos - self.cam.axis.position
        self.cam.axis.position_adjustment += pos_fixup
        return np.linalg.norm(pos_fixup)

    def draw(self):
        glColor3f(1.0, 1.0, 0.0)
        glBegin(GL_LINE_STRIP)
        glVertex2f(*self.position)
        glVertex2f(*self.cam.axis.position)
        glEnd()

    def force(self):
        spring_force = self.stiffness * np.dot(self.cam.axis.position - self.position, self.direction) * self.direction
        tangent = (-self.direction[1], self.direction[0])
        return (
            self.balancing_force * tangent[0] + spring_force[0],
            self.balancing_force * tangent[1] + spring_force[1],
        )


