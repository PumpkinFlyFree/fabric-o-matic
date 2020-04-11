from itertools import chain, cycle
import re
import sympy as sp
import numpy as np

rt = sp.Rational
half = rt(1,2)

vector = lambda x, y, z: sp.Matrix([sp.sympify(x), sp.sympify(y), sp.sympify(z)])

class vec:
    symbol = lambda name: vector(*sp.symbols(f"{name}_x, {name}_y, {name}_z"))
    symbols = lambda names: [vec.symbol(n) for n in re.split(r",? +",names)]   
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

    lambdexpr = sp.lambdify(symbols, expr)
        
    def iterate(indexes, vals):
        if len(vals):
            return np.array([
                iterate(indexes + (i,), vals[1:])
                for i in range(0, vals[0])
            ],dtype=dtype)
        return lambdexpr(*[v[i] for v, i in zip(values, indexes)])

    return iterate(tuple(), [len(v) for v in values])
    

def triangulate_grid(nu, nv):
    for u in range(nu-1):
        for v in range(nv-1):
            idx = u * nv + v
            yield (idx, idx+nv, idx+nv+1)
            yield (idx, idx+nv+1, idx+1)           
            

def triangulate_pipe(nu, nv):
    for u in range(nu-1):
        for v in range(nv-1):
            idx = u * nv + v
            yield (idx, idx+nv, idx+nv+1)
            yield (idx, idx+nv+1, idx+1)
        idx = u * nv + nv - 1
        yield (idx, idx+nv, idx+1)
        yield (idx, idx+1, idx-nv+1)
        

def iter_slices(length, total):
    """generates slices of points indexes"""
    for j in range(0, total-length+1):
        yield slice(j, j+length) 

def hexcolor(c): 
    return int(c[0] * 0xff0000 + c[1] * 0x00ff00 + c[2] * 0xff)

def hexpalette(cmap): 
    return [hexcolor(cmap(t)) for t in np.linspace(0, 1, cmap.N)]