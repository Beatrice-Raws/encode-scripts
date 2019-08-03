from vapoursynth import core, VideoNode, GRAY, GRAY8, GRAYS, YUV
import vapoursynth as vs
import atomchtools as at
import cooldegrain as cd
from insaneAA import insaneAA, EEDI3Mode, NNEDI3Mode

def MainAA(clip):
    return insaneAA(clip, eedi3_mode=EEDI3Mode.OPENCL, nnedi3_mode=NNEDI3Mode.NNEDI3CL, pscrn=0, descale_strength=0.85, kernel='spline36', descale_height=848)

def DealWithFades(clip):
	Y = clip.std.ShufflePlanes(0, GRAY).resize.Point(format=GRAYS)
	Y = Y.ftf.FixFades(mode=0, threshold=0.002, color=0.0, opt=True)
	Y = Y.resize.Point(format=GRAY8)
	return core.std.ShufflePlanes([Y,clip], [0,1,2], YUV)

def DenoiseDebandMain(clip, expr_multiplier=4.5, thsad=80, thsadc=48, d_range=8, y=48, cb=32, cr=32, grainy=48, grainc=32):
    src = core.fmtc.bitdepth(clip, bits=16)
    mask = at.retinex_edgemask(src, sigma=1).std.Expr(f'x {expr_multiplier} *')
    den = cd.CoolDegrain(src, tr=1, thsad=thsad, thsadc=thsadc, bits=16, blksize=8, overlap=4)
    deb = core.f3kdb.Deband(den, range=d_range, y=y, cb=cb, cr=cr, grainy=grainy, grainc=grainc, output_depth=16)
    clip = core.std.MaskedMerge(deb, src, mask, [0,1,2], first_plane=True)
    return clip

def DenoiseDebandFades(clip):
    return DenoiseDebandMain(clip, thsadc=56, y=56, cb=42, cr=42, grainy=56, grainc=40)

def DenoiseDebandStronger(clip):
    return DenoiseDebandMain(clip, thsad=112, thsadc=56, y=80, cb=48, cr=48, grainy=80, grainc=48)

def DenoiseDebandPV2_TOHO(clip):
    return DenoiseDebandMain(clip, thsad=112, thsadc=56, d_range=15, y=112, cb=112, cr=112, grainy=64, grainc=48)

def DenoiseDebandPV2(clip):
    return DenoiseDebandMain(clip, expr_multiplier=7.5, thsad=112, thsadc=56, d_range=15, y=112, cb=56, cr=56, grainy=64, grainc=48)
