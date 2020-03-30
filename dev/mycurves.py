import sympy as sp

from myutils import vec, vector

u, v = sp.symbols("u, v")

B2 = [
    u**2 / 2,  # * P[j-2]
    - (u+1)**2 + 3*(u+1) - 3/2, # * P[j-1]
    (u+2)**2 / 2 - 3*(u+2) + 9/2 # * P[j]
]

B3 = [
    u**3 / 6,  # * P[j-3]
    -(u+1)**3 / 2 + 2*(u+1)**2 - 2*(u+1) + sp.Rational(2,3),  # * P[j-2]
    (u+2)**3 / 2 - 4*(u+2)**2 + 10*(u+2) - sp.Rational(22,3),  # * P[j-1]
    -(u+3)**3 / 6 + 2*(u+3)**2 - 8*(u+3) + sp.Rational(32,3)  # * P[j]
]

def Spline(bspl, points):
    deg = len(bspl)
    assert len(points) == deg, f"{len(points)} != {deg}"

    return sp.add.Add(*[bspl[i] * points[i] for i in range(0, deg)])

Circle = lambda t, r: vector(r * sp.cos(t * 2 * sp.pi), r * sp.sin(t * 2 * sp.pi), 0)

Ellipse = lambda t, a, b: vector(a * sp.cos(t * 2 * sp.pi), b * sp.sin(t * 2 * sp.pi), 0)

# Verically-aligned spine frame: X axis parallel to world XY, Y axis approximately "up"
def spine_frame(Aa, u):
    Z = vec.normalize(sp.diff(Aa, u))         # spine tangent direction
    X = vec.normalize(Z.cross(vector(0, 0, 1)))
    Y = X.cross(Z)
    return X, Y, Z

def Pipe(Qa, Qc):
    X, Y, Z = spine_frame(Qa, u)
    return Qa + X * Qc[0] + Y * Qc[1]

def pipe_frame(S, u, v):
    U = vec.normalize(sp.diff(S, u))
    V = vec.normalize(sp.diff(S, v))
    N = U.cross(V)    
    return U, V, N