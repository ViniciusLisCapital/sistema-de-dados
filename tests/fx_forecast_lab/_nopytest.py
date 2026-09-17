"""The three pytest features the integrity controls use, for when pytest isn't
installed — it is not a declared dependency of this project.

Deliberately tiny: `approx`, `fixture` (a no-op here, since the standalone
runner injects fixtures by parameter name) and `mark.parametrize` (which just
records the cases on the function for that runner to expand). Anything richer
would be a second test framework to maintain.
"""

from __future__ import annotations

import math


class _Approx:
    def __init__(self, expected, rel=None, abs=None):
        self.expected = expected
        self.rel = rel if rel is not None else 1e-6
        self.abs = abs if abs is not None else 1e-12

    def __eq__(self, other):
        try:
            return math.isclose(float(other), float(self.expected),
                                rel_tol=self.rel, abs_tol=self.abs)
        except (TypeError, ValueError):
            return NotImplemented

    def __repr__(self):
        return f"approx({self.expected!r}, rel={self.rel})"


class _Mark:
    @staticmethod
    def parametrize(argnames, argvalues):
        names = [a.strip() for a in argnames.split(",")]

        def deco(fn):
            cases = []
            for v in argvalues:
                vals = v if isinstance(v, (tuple, list)) else (v,)
                cases.append(dict(zip(names, vals)))
            fn._params = cases
            return fn

        return deco

    def __getattr__(self, _name):
        def deco(fn):
            return fn

        return deco


class _Pytest:
    mark = _Mark()

    @staticmethod
    def approx(expected, rel=None, abs=None):
        return _Approx(expected, rel=rel, abs=abs)

    @staticmethod
    def fixture(*args, **kwargs):
        if args and callable(args[0]):
            return args[0]

        def deco(fn):
            return fn

        return deco

    @staticmethod
    def raises(*_a, **_k):  # not used by the controls, kept so an import can't fail
        raise NotImplementedError("pytest.raises is not shimmed")


pytest = _Pytest()
