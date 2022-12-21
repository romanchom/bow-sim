from OpenGL.GL import *
import sympy
import itertools

class Bow:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def relaxate(self):
        threshold = 0.1
        for i in range(1000):
            stress = sum(self.for_all(lambda c: c.apply_constraint()))
            print(stress)
            self.update()
            if stress < threshold:
                break

        if stress > threshold:
            print("not good")

    def for_all(self, cb):
        for comp in self.components:
            try:
                yield cb(comp)
            except AttributeError:
                pass

    def init(self):
        self.update()
        for _ in self.for_all(lambda c: c.init()): pass

    def update(self):
        for _ in self.for_all(lambda c: c.update()): pass

    def draw(self):
        for _ in self.for_all(lambda c: c.draw()): pass

    def solve(self):
        eqs = list(self.for_all(lambda c: c.equations()))
        symbols = list(self.for_all(lambda c: c.symbols()))
        eqs = [sum(itertools.chain.from_iterable(eq[x] for eq in eqs)) for x in range(3)]
        eqs = [sympy.Eq(exp, 0) for exp in eqs]
        symbols = list(itertools.chain.from_iterable(symbols))

        return list(sympy.linsolve(eqs, symbols))[0]
