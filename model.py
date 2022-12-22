from OpenGL.GL import *
import sympy
import itertools

class ConvergenceError:
    def __init__(self, num_iters, stress):
        self.num_iter = num_iters
        self.stress = stress

    def __repr__(self):
        return f'Relaxation did not converge after {self.num_iter} with finall stress of {self.stress}'

class Model:
    def __init__(self, components):
        self.components = components
        self.update()
        for _ in self.for_all(lambda c: c.init()): pass

    def relaxate(self):
        threshold = 0.1
        iterations = 1000
        for i in range(iterations):
            stress = sum(self.for_all(lambda c: c.apply_constraint()))
            self.update()
            if stress < threshold:
                break

        # if stress > threshold:
        #     raise ConvergenceError(iterations, stress)

    def for_all(self, cb):
        for comp in self.components:
            try:
                yield cb(comp)
            except AttributeError:
                pass

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

        return list(map(float, list(sympy.linsolve(eqs, symbols))[0]))
