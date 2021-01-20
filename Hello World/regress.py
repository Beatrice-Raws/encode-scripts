"""
    Original module written by shane#9837 (on Discord).
"""
import vapoursynth as vs
from functools import partial
from typing import NamedTuple
core = vs.core

class RegressClips(NamedTuple):
    slope: vs.VideoNode
    intercept: vs.VideoNode
    correlation: vs.VideoNode


def Regress(x, *ys, radius=1, eps=1e-7):
    """
    Fit a line for every neighborhood of values of a given size in a clip
    with corresponding neighborhoods in one or more other clips.

    More info: https://en.wikipedia.org/wiki/Simple_linear_regression
    """

    if not radius > 0:
        raise ValueError("radius must be greater than zero")

    Expr = vs.core.std.Expr
    E = partial(vs.core.std.BoxBlur, hradius=radius, vradius=radius)

    def mul(*c):
        return Expr(c, "x y *")

    def sq(c):
        return mul(c, c)

    Ex = E(x)
    Exx = E(sq(x))
    Eys = [E(y) for y in ys]
    Exys = [E(mul(x, y)) for y in ys]
    Eyys = [E(sq(y)) for y in ys]

    var_x = Expr((Exx, Ex), "x y dup * - 0 max")
    var_ys = [Expr((Eyy, Ey), "x y dup * - 0 max") for Eyy, Ey in zip(Eyys, Eys)]
    cov_xys = [Expr((Exy, Ex, Ey), "x y z * -") for Exy, Ey in zip(Exys, Eys)]

    slopes = [Expr((cov_xy, var_x), f"x y {eps} + /") for cov_xy in cov_xys]
    intercepts = [Expr((Ey, slope, Ex), "x y z * -") for Ey, slope in zip(Eys, slopes)]
    corrs = [
        Expr((cov_xy, var_x, var_y), f"x dup * y z * {eps} + / sqrt")
        for cov_xy, var_y in zip(cov_xys, var_ys)
    ]

    return list(map(RegressClips._make, zip(slopes, intercepts, corrs)))

def ReconstructMulti(c, r, radius=2):
    weights = core.std.Expr(r.correlation, 'x 0.5 - 0.5 / 0 max')
    slope_pm = core.std.Expr((r.slope, weights), 'x y *')
    slope_pm_sum = mean(slope_pm, radius)
    recons = core.std.Expr((c, slope_pm_sum), 'x y *')
    return recons

def mean(c, radius):
    return core.std.BoxBlur(c, hradius=radius, vradius=radius)