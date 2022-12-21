import numpy as np
from OpenGL.GL import *
import sympy

def angle_to(a, p):
    diff = p - a
    angle = np.arctan2(diff[1], diff[0])
    return angle

class CableAttachment:
    def __init__(self, position):
        self.position = np.array(position)

class CablePiece:
    def __init__(self, attachment, cam):
        self.attachment = attachment
        self.cam = cam
        self.cam_anchor = np.array((0, 0))
        self.update()

    @property
    def total_length(self):
        return self.wrapped_length + self.straight_length

    def update(self):
        self.wrapped_index, self.cam_anchor = max(enumerate(self.cam.points), key=lambda p: self.cam.direction * angle_to(self.attachment.position, p[1]))
        self.cable_direction = self.cam_anchor - self.attachment.position
        self.straight_length = np.linalg.norm(self.cable_direction)
        self.cable_direction /= self.straight_length
        lever_arm = self.cam_anchor - self.cam.axis.position
        self.lever = np.cross(lever_arm, self.cable_direction)
        self.wrapped_length = 0.0
        for p0, p1 in zip(self.cam.points[:self.wrapped_index], self.cam.points[1:]):
            self.wrapped_length += np.linalg.norm(p0 - p1)

    def apply_error(self, error):
        self.cam.axis.angle_adjustment += error / self.lever * 0.5
        self.cam.axis.position_adjustment += error * self.cable_direction * 0.5


class Cable:
    def __init__(self, name, pieces):
        self.target_length = 0
        self.pieces = pieces
        self.tension = sympy.symbols(name)

    @property
    def total_length(self):
        return sum(map(lambda p: p.total_length, self.pieces))

    def init(self):
        self.target_length = self.total_length

    def apply_constraint(self):
        error = (self.target_length - self.total_length)
        for p in self.pieces:
            p.apply_error(error / len(self.pieces))
        return abs(error)

    def draw(self):
        for piece in self.pieces:
            glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_LINE_STRIP)
            for p in piece.cam.points[:piece.wrapped_index + 1]:
                glVertex2f(*p)
            glVertex2f(*piece.attachment.position)
            glEnd()

    def equations(self):
        force_x = sum(map(lambda p: self.tension * p.cable_direction[0], self.pieces))
        force_y = sum(map(lambda p: self.tension * p.cable_direction[1], self.pieces))
        torque = sum(map(lambda p: self.tension * p.lever, self.pieces))
        return (
            (force_x,),
            (force_y,),
            (torque,),
        )

    def symbols(self):
        return (self.tension,)
