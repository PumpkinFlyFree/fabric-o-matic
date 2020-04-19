from itertools import chain
import numpy as np
import sympy as sp
from myutils import *

t, u = sp.symbols("t, u")

Circle = lambda t, r: vector(r * sp.cos(t * 2 * sp.pi), r * sp.sin(t * 2 * sp.pi), 0)
Ellipse = lambda t, a, b: vector(a * sp.cos(t * 2 * sp.pi), b * sp.sin(t * 2 * sp.pi), 0)
Bezier2 = lambda t, p0, p1, p2: (1-t)**2 * p0 + 2 * t * (1-t) * p1 + t**2 * p2
Bezier3 = lambda t, p0, p1, p2, p3: (1-t)**3 * p0 + 3 * t * (1-t)**2 * p1 + 3 * t**2 * (1-t) * p2 + t**3 * p3


def eval_curve(Q, u, urange=(0,1,6)):
    uu = np.linspace(*urange)
    points = eval(Q, {u: uu}, dtype=np.float)
    return points


B2 = [
    t**2 / 2,
    -t**2 + 3*t - sp.Rational(3,2),
    t**2 / 2 - 3*t + sp.Rational(9,2)
]

B3 = [
     t**3 / 6, 
    -t**3 / 2 + 2*t**2 -  2*t + sp.Rational(2,3),
     t**3 / 2 - 4*t**2 + 10*t - sp.Rational(22,3),
    -t**3 / 6 + 2*t**2 -  8*t + sp.Rational(32,3)
]

def Spline(u, B, points):
    """Creates expression for single spline segment, with arg replacement
    
    B: list of basis functions B2 or B3
    points: list of points from j-k to j
    """
    deg = len(B)
    assert len(points) == deg, f"{len(points)} != {deg}"
    parts = [B[i].subs({t: u+i}) * vector(*points[-i-1]) for i in range(0, deg)]
    return sp.add.Add(*parts)

def make_splines(t, B, points):
    deg = len(B)
    return [Spline(t, B, points[ids]) for ids in iter_slices(deg, len(points))]

def eval_splines(B, points, urange=(0, 1, 6)):
#     deg = len(B)
#     return list(chain(*[eval_curve(Spline(t, B, points[ids]), t, urange) for ids in iter_slices(deg, len(points))]))
     return list(chain(*[eval_curve(spl, t, urange) for spl in make_splines(t, B, points)]))

def spine_frame(u, Q):
    # Verically-aligned spine frame: X axis parallel to world XY, Y axis approximately "up"
    Z = vec.normalize(sp.diff(Q, u))         # spine tangent direction
    X = vec.normalize(Z.cross(vector(0, 0, 1)))
    Y = X.cross(Z)
    return X, Y, Z

def Pipe(uv, Qa, Qc, XYZ=None):
    u, v = uv
    if XYZ is None:
        X, Y, Z = spine_frame(u, Qa)
    else:
        X, Y, Z = XYZ
    return Qa + X * Qc[0] + Y * Qc[1]

def pipe_frame(uv, S):
    u, v = uv    
    U = vec.normalize(sp.diff(S, u))
    V = vec.normalize(sp.diff(S, v))
    N = U.cross(V)    
    return U, V, N
      
def eval_pipe(S, vrs, segs):
    u, v = vrs
    usegs, vsegs = segs
    nu = usegs+1
    nv = vsegs
    uu = np.linspace(0, 1, nu)
    vv = np.linspace(0, 1, nv)
    points = eval(S, {u: uu, v: vv}).reshape(nu*nv, 3)
    tris = np.array(tuple(triangulate_pipe(nu, nv)), np.int)
    coords = np.array(np.meshgrid(uu, vv)).T.reshape(-1,2)
    return points, tris, coords
