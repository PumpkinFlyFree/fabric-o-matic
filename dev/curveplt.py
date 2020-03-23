import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def eval(expr, var, vals): # evaluate sympy -> numpy
    return np.array([expr.subs({var: val}).evalf() for val in vals]).astype(np.float)




class Plt:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = Axes3D(fig, proj_type='ortho')
        self.ax.autoscale(False)
        self.ax.set_xlabel("X")
        self.ax.set_xlim(0, 1)
        self.ax.set_ylabel("Y")
        self.ax.set_ylim(0, 1)
        self.ax.set_zlabel("Z")
        self.ax.set_zlim(0, 1)

    def plot_curve(self, Q, fmt='k-', samples=10, **kwargs):
        tt = np.linspace(0, 1, samples)
        pnts = eval(Q, 't', tt)
        self.ax.plot(pnts[:,0], pnts[:,1], pnts[:,2], fmt, **kwargs)

    def plot_arc(self, Q, t0, t1, fmt='k-', **kwargs):
        tt = np.linspace(t0, t1, 10)
        pnts = eval(Q, 't', tt)
        self.ax.plot(pnts[:,0], pnts[:,1], pnts[:,2], fmt, **kwargs)

    def plot_points(self, points, fmt='ro', **kwargs):
        pnts = np.array(points)
        self.ax.plot(pnts[:,0], pnts[:,1], pnts[:,2], fmt, **kwargs)

    def plot_vectors(self, pnts, vecs, **kwargs):
        self.ax.quiver(pnts[:,0], pnts[:,1], pnts[:,2], vecs[:,0], vecs[:,1], vecs[:,2], **kwargs)

    # def plot_pipe(self.ax, S, samples=10, color='c'):
    #     Sl = sp.lambdify((t, s), S)
    #     tt, ss = np.meshgrid(np.linspace(0, 1, samples*2), np.linspace(0, 0.5, samples))
    #     xx, yy, zz = Sl(tt, ss)
    #     self.ax.plot_surface(xx[0], yy[0], zz[0], alpha=0.5, edgecolors=('k',), linewidths=(0.1), color=color)

    # def plot_pipe_full(self.ax, S, samples=10, color='c'):
    #     Sl = sp.lambdify((t, s), S)
    #     tt, ss = np.meshgrid(np.linspace(0, 1, samples*2), np.linspace(0, 1.0, samples))
    #     xx, yy, zz = Sl(tt, ss)
    #     self.ax.plot_surface(xx[0], yy[0], zz[0], alpha=0.5, edgecolors=('k',), linewidths=(0.1), color=color)

    # def plot_pipe_uv(self.ax, S, u, v):
    #     Sl = sp.lambdify((t, s), S)
    #     xx, yy, zz = Sl(u, v)
    #     self.ax.plot(xx, yy, zz, 'ko')

    #     tt, ss = np.linspace(0, 1.0, 10), np.linspace(v, v, 10)
    #     xx, yy, zz = Sl(tt, ss)
    #     self.ax.plot(xx[0], yy[0], zz[0], 'k-', dashes=(1, 1))

    #     tt, ss = np.linspace(u, u, 10), np.linspace(0, 0.5, 10)
    #     xx, yy, zz = Sl(tt, ss)
    #     self.ax.plot(xx[0], yy[0], zz[0], 'k-', dashes=(1, 1))


    def plot_dot(self, pnt, txt, fmt='ko'):
        pnts = np.array(pnt)
        self.ax.plot(*pnt, fmt)
        if txt:
            self.ax.text(pnt[0], pnt[1], pnt[2]+0.05, txt)


    def plot_line(self, pnt0, pnt1, dashes=(1, 1)):
        xx = (pnt0[0][0], pnt1[0][0])
        yy = (pnt0[1][0], pnt1[1][0])
        zz = (pnt0[2][0], pnt1[2][0])
        self.ax.plot(xx, yy, zz, 'k-', dashes=dashes)