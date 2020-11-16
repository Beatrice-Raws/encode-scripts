from vapoursynth import core, VideoNode, GRAY
import vapoursynth as vs
import atomchtools as at
import xvs

core.max_cache_size = 40000


def hard_deband(clip: vs.VideoNode) -> vs.VideoNode:
    linemask = at.retinex_edgemask(clip, sigma=0.1, opencl=True, draft=False)
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    deb1 = core.placebo.Deband(clip16, iterations=10, threshold=4)
    deb2 = xvs.SAdeband(deb1)
    debanded = core.std.MaskedMerge(deb2, clip16, linemask, planes=[0,1,2], first_plane=True)
    return debanded


clip = core.dgdecodenv.DGSource(r'00009.dgi')

DD_clip = hard_deband(clip)

clip.fmtc.bitdepth(bits=10).set_output()