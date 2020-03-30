from itertools import chain
import sympy as sp
import numpy as np
import plotly.graph_objects as go

vector = lambda x, y, z: sp.Matrix([sp.sympify(x), sp.sympify(y), sp.sympify(z)])

class vec:
    symbol = lambda name: vector(*sp.symbols(f"{name}_x, {name}_y, {name}_z"))
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


def Arrows(x, y, z, u, v, w, color='black', scale=1.0, **kwargs):
    return go.Cone(x=x, y=y, z=z, u=u, v=v, w=w, anchor='tail', showscale=False, colorscale=[[0, color], [1, color]], sizemode='scaled', sizeref=scale, **kwargs)


def Surface(x, y, z, color='gray', **kwargs):
    return go.Surface(x=x, y=y, z=z, showscale=False, colorscale=[[0, color], [1, color]], **kwargs)



def plot_spline(bspl, points, names=None, **kwargs):
    deg = len(bspl)
    traces = []
    uu = np.linspace(0, 1, 10)
    for j in range(deg-1, len(points)):
        if names:
            kwargs['name'] = "-".join(names[j-deg+1:j+1]) 
        q = Spline(bspl, points[j-deg+1:j+1])
        xx, yy, zz = eval(q, u=uu).T
        traces.append(go.Scatter3d(x=xx, y=yy, z=zz, mode='lines', **kwargs))
    return traces
