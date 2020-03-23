from itertools import chain
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class vec:
    vector = lambda x, y, z: sp.Matrix([x, y, z])
    symbol = lambda name: vec.vector(*sp.symbols(f"{name}_x, {name}_y, {name}_z"))
    symbols = lambda names: [vec.symbol(n) for n in names.split(' ')]
    subs = lambda expr, subs: expr.subs(dict(chain(*[((f'{sym}_x', val[0]),(f'{sym}_y', val[1]),(f'{sym}_z', val[2])) for sym, val in subs.items()])))
    length = lambda v: sp.sqrt(v.dot(v))
    normalize = lambda v: v / vec.length(v)


def eval(expr, args=None, dtype=np.float, **kwargs):
    """Evaluate sympy expression into numpy array.

    Variables to substitute can be given in kwargs by name, or in args by symbol or string name.

    Values can be any iterables or scalars (converted to singular lists).

    :param expr: sympy expression
    :param args: substitution by dict
    :param kwargs: substitutions by name
    :param dtype: numpy type to convert values

    :returns: np.array with predictable shape and data type

    >>> eval(x + y + z, x=np.linspace(0, 1, 4), y=[10, 20], z=100.0)
    array([[[110.        ],
            [120.        ]],

           [[110.33333333],
            [120.33333333]],

           [[110.66666667],
            [120.66666667]],

           [[111.        ],
            [121.        ]]])

    >>> eval(x + y, x=[1, 2], y=[10, 20], dtype=np.float32)

    >>> eval(x + y, {x: [1, 2], 'y': [10, 20]})

    >>> eval(x + y + z, x=[1, 2], y=[10, 20])
    ...
    TypeError: can't convert expression to float
    """
    assert args or len(kwargs), "substitutions expected"
    if not args:
        args = kwargs
    symbols = args.keys()
    values = [(v,) if not hasattr(v, '__iter__') else v for v in args.values()]

    def iterate(indexes, vals):
        if len(vals):
            return np.array([
                iterate(indexes + (i,), vals[1:])
                for i in range(0, vals[0])
            ]).astype(dtype)
        return expr.subs({s: v[i] for s, v, i in zip(symbols, values, indexes)})

    return iterate(tuple(), [len(v) for v in values])

class curv:
    @staticmethod
    def frame(Q, t):
        Qdt = sp.simplify(sp.diff(Q, t))     # Q'
        Qddt = sp.simplify(sp.diff(Qdt, t))  # Q''
        Qdt_dt = sp.simplify(Qdt.dot(Qdt))   # Q'·Q'
        Qdt_ddt = sp.simplify(Qdt.dot(Qddt)) # Q'·Q''
        T = vec.normalize(Qdt)
        N = vec.normalize((Qdt_dt * Qddt - Qdt_ddt * Qdt) / Qdt_dt **2)
        B = T.cross(N)
        return T, N, B

    @staticmethod
    def params(Q, t):
        Qdt = sp.simplify(sp.diff(Q, t))       # Q'
        Qddt = sp.simplify(sp.diff(Qdt, t))    # Q''
        Qdddt = sp.simplify(sp.diff(Qddt, t))  # Q'''
        Qdt_dt = sp.simplify(Qdt.dot(Qdt))     # Q'·Q'
        Qdt_ddt = sp.simplify(Qdt.dot(Qddt))   # Q'·Q''
        Qdtxddt = sp.simplify(Qdt.cross(Qddt)) # Q'×Q''
        Qdtxddt_sq = sp.simplify(Qdtxddt.dot(Qdtxddt)) # Q'×Q''·Q'×Q''
        vel = vec.len(Qdt)
        kap = Qdtxddt_sq / Qdt_dt ** 3
        tau = Qdtxddt.dot(Qdddt) / Qdtxddt_sq
        return vel, kap, tau


class Plt:

    def __init__(self, ax=None):
        if ax:
            self.ax = ax
        else:
            self.ax = Axes3D(plt.figure(figsize=(6, 6)))
        self.reset()

    def clear(self):
        self.reset()

    def reset(self):
        self.ax.cla()
        self.ax.set_proj_type('ortho')
        self.ax.autoscale(False)
        self.ax.set_xlabel("X")
        self.ax.set_xlim(0, 1)
        self.ax.set_ylabel("Y")
        self.ax.set_ylim(0, 1)
        self.ax.set_zlabel("Z")
        self.ax.set_zlim(0, 1)


    def points(self, points, fmt='ko', **kwargs):
        xx, yy, zz = np.array(points).T
        self.ax.plot(xx, yy, zz, fmt, **kwargs)

    def vectors(self, pnts, vecs, **kwargs):
        xx, yy, zz = pnts.T
        uu, vv, ww = vecs.T
        self.ax.quiver(xx, yy, zz, uu, vv, ww, **kwargs)

    def curve(self, Q, t, fmt='k-', samples=128, **kwargs):
        tt = np.linspace(0, 1, samples)
        xx, yy, zz = eval(Q, {t: tt}).T
        self.ax.plot(xx, yy, zz, fmt, **kwargs)

    def arc(self, Q, t, t0, t1, fmt='k-', **kwargs):
        tt = np.linspace(t0, t1, 64)
        xx, yy, zz = eval(Q, {t: tt}).T
        self.ax.plot(xx, yy, zz, fmt, **kwargs)

    def surface(self, S, u, v, **kwargs):
        uu = np.linspace(0, 1, 32)
        vv = np.linspace(0, 1, 16)
        xx, yy, zz = eval(S, {u: uu, v: vv}).T
        self.ax.plot_surface(xx, yy, zz, **kwargs)

    def pipe(self, S, u, v, **kwargs):
        uu = np.linspace(0, 1, 32)
        vv = np.linspace(0, 0.5, 8)
        xx, yy, zz = eval(S, {u: uu, v: vv}).T
        self.ax.plot_surface(xx, yy, zz, **kwargs)