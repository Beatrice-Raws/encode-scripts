import vapoursynth as vs
import atomchtools as at
import cooldegrain as cd
import finedehalo as fd
import HardAAp2 as HardAA
from vapoursynth import core
from beatricetools import ExprStr
from insaneAA import insaneAA, EEDI3Mode, NNEDI3Mode

core.augment(locals())

"""
NekoCoder's library for anime encode
"""

def clip_aa(clip: vs.VideoNode, descale_strength: float, kernel: str, descale_height: int, bicubic_b: float = 1/3, bicubic_c: float = 1/3, taps: int = 3) -> vs.VideoNode:
    return insaneAA(clip=clip, eedi3_mode=EEDI3Mode.OPENCL, nnedi3_mode=NNEDI3Mode.NNEDI3CL, eedi3_device=0, nnedi3_device=0, pscrn=0, descale_strength=descale_strength, kernel=kernel, descale_height=descale_height, bicubic_b=bicubic_b, bicubic_c=bicubic_c, lanczos_taps=taps)

def main_aa(clip: vs.VideoNode) -> vs.VideoNode:
    return clip_aa(clip=clip, descale_strength=0.8, kernel='bicubic', descale_height=720, bicubic_b=0, bicubic_c=1)

def hard_aa(clip: vs.VideoNode, mthr: int = 40, useCL: bool = True) -> vs.VideoNode:
    return HardAA.HardAA(clip, mthr=mthr, useCL=useCL)

def main_dehalo(clip: vs.VideoNode) -> vs.VideoNode:
    return fd.fine_dehalo(clip=clip, darkstr=0, brightstr=0.8, showmask=0, rx=1.7, ry=1.7, thmi=65, thma=120, useMtEdge=True)

def denoise_deband(clip: vs.VideoNode, expr_multiplier: float = 4,
    thsad: int = 64, thsadc: int = 48, blksize: int = 8, overlap: int = 4,
    d_range: int = 8, y: int = 56, cb: int = 48, cr: int = 48, grainy: int = 48, grainc: int = 32) -> vs.VideoNode:

    src  = core.fmtc.bitdepth(clip, bits=16)
    mask = at.retinex_edgemask(src, sigma=1).ExprStr(f'x * {expr_multiplier}')
    den  = cd.CoolDegrain(src, tr=1, thsad=thsad, thsadc=thsadc, bits=16, blksize=blksize, overlap=overlap)
    deb  = core.f3kdb.Deband(den, range=d_range, y=y, cb=cb, cr=cr, grainy=grainy, grainc=grainc, output_depth=16)
    clip = core.std.MaskedMerge(deb, src, mask, first_plane=True)
    return clip

def replace_by_mask(clip_a: vs.VideoNode, clip_b: vs.VideoNode, mask: str, frames: list) -> vs.VideoNode:
    return at.rfs(clip_a, at.ApplyImageMask(clip_a, clip_b, mask, preview=False), [frames])


### development block. unnecessary for production ###

def histogramm(clip: vs.VideoNode) -> vs.VideoNode:
    return clip.fmtc.bitdepth(bits=8).hist.Luma()

def sobel_mask(clip: vs.VideoNode, thr: int = 40) -> vs.VideoNode:
    sob = core.std.ShufflePlanes(clip, 0, vs.GRAY).std.Sobel()
    cleanup = sob.ExprStr(f'0 if x < {thr} else x')
    return cleanup

def credits_mask(clip: vs.VideoNode, b: float = 0, c: float = 1) -> vs.VideoNode:
    mask1 = core.std.Prewitt(clip.std.ShufflePlanes(0, vs.GRAY))
    mask2 = at.DiffRescaleMask(clip, kernel="bicubic", descale_h=720, b=b, c=c, mthr=25).ExprStr('0 if x < 10 else 255').std.Maximum().std.Maximum().std.Deflate()
    mask3 = ExprStr([mask1, mask2], 'min(x, y)').ExprStr('0 if x < 30 else x').std.Maximum().std.Maximum().std.Deflate()
    return mask3

def rescale_credit_mask(clip: vs.VideoNode) -> vs.VideoNode:
    return clip.at.DiffRescaleMask(descale_h=720, kernel='bicubic', b=0, c=1, mthr=30).std.Maximum().std.Inflate()
