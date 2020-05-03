# by shane#9837 (Discord)

import vapoursynth as vs
from collections import namedtuple
from functools import partial
from typing import Callable

RegressParams = namedtuple('RegressParams', 'slope intercept correlation')


def Regress(x, *ys, radius=1, eps=1e-7):
    Expr = vs.core.std.Expr
    mul = lambda *c: Expr(c, 'x y *')
    sq = lambda c: mul(c, c)
    E = partial(vs.core.std.BoxBlur, hradius=radius, vradius=radius)

    Ex = E(x)
    Exx = E(sq(x))
    Eys = [E(y) for y in ys]
    Exys = [E(mul(x, y)) for y in ys]
    Eyys = [E(sq(y)) for y in ys]

    var_x = Expr((Exx, Ex), 'x y dup * -')
    var_ys = [Expr((Eyy, Ey), 'x y dup * -') for Eyy, Ey in zip(Eyys, Eys)]
    cov_xys = [Expr((Exy, Ex, Ey), 'x y z * -')  for Exy, Ey in zip(Exys, Eys)]

    slopes = [Expr((cov_xy, var_x), f'x y {eps} + /') 
              for cov_xy in cov_xys]
    intercepts = [Expr((Ey, slope, Ex), 'x y z * -') 
                  for Ey, slope in zip(Eys, slopes)]
    corrs = [Expr((cov_xy, var_x, var_y), f'x dup * y z * {eps} + / sqrt')
             for cov_xy, var_y in zip(cov_xys, var_ys)]

    return list(map(RegressParams._make, zip(slopes, intercepts, corrs)))


def Reconstruct(original_luma: vs.VideoNode, demangled_luma: vs.VideoNode,
                demangled_chroma_u: vs.VideoNode, demangled_chroma_v: vs.VideoNode,
                radius: int = 3, use_binary: bool = False) -> vs.VideoNode:

    yu, yv = Regress(demangled_luma, demangled_chroma_u, demangled_chroma_v, radius=radius)

    y_fixup = vs.core.std.MakeDiff(original_luma, demangled_luma)

    if use_binary:
        u_fixup = vs.core.dpriv.Reconstruct(y_fixup, yu.slope, yu.correlation, radius=radius)
        v_fixup = vs.core.dpriv.Reconstruct(y_fixup, yv.slope, yv.correlation, radius=radius)
        u_r = vs.core.std.MergeDiff(demangled_chroma_u, u_fixup)
        v_r = vs.core.std.MergeDiff(demangled_chroma_v, v_fixup)
    else:
        u_fixup = vs.core.std.Expr((y_fixup, yu.slope), 'x y *')
        u_r = vs.core.std.MergeDiff(demangled_chroma_u, u_fixup)
        mask_u = vs.core.std.Expr(yu.correlation, 'x 0.3 - 0.7 / dup 0 > swap 0 ?')
        u_r = vs.core.std.MaskedMerge(demangled_chroma_u, u_r, mask_u)
        v_fixup = vs.core.std.Expr((y_fixup, yv.slope), 'x y *')
        v_r = vs.core.std.MergeDiff(demangled_chroma_v, v_fixup)
        mask_v = vs.core.std.Expr(yv.correlation, 'x 0.3 - 0.7 / dup 0 > swap 0 ?')
        v_r = vs.core.std.MaskedMerge(demangled_chroma_v, v_r, mask_v)

    return vs.core.std.ShufflePlanes([original_luma.resize.Bicubic(format=vs.GRAY8), u_r.resize.Bicubic(format=vs.GRAY8), v_r.resize.Bicubic(format=vs.GRAY8)], [0,0,0], vs.YUV)
