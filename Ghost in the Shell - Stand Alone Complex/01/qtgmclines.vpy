from vapoursynth import core, VideoNode, GRAY
import vapoursynth as vs
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc as hf
import mvsfunc as mvf
import gradfun_amod as gfa
import insaneAA
import HardAAp2 as HardAA
import cooldegrain as cd

core.max_cache_size = 5000


def SAC_aa(clip: vs.VideoNode) -> vs.VideoNode:
    clipY = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(clipY, descale_strength=0.9, kernel='bicubic', bicubic_b=0, bicubic_c=0.75, descale_width=None, descale_height=540)
    hard = HardAA.HardAA(desc, mask=None, nrad=2, alpha=0.15, beta=0.2)
    mask = core.std.MakeDiff(desc, hard).hist.Luma().std.Expr('x 2 *').rgvs.RemoveGrain(2).std.Expr('x 50 < 0 x 2 * ?').std.Maximum()
    maskedHard = core.std.MaskedMerge(desc, hard, mask)
    rescale = insaneAA.rescale(maskedHard, eedi3Mode='cpu', nnedi3Mode='opencl', dx=1920, dy=1080)
    return insaneAA.insaneAA(clip, externalAA=rescale, outputMode=0, inputMode=1)


episode = core.lsmas.LWLibavSource(r'01-1.avi')
maskforQTGMC = core.raws.Source(r'01losslessforfix.y4m')

episode = core.edgefixer.Continuity(episode, 2, 0, 2, 0, 2)

titles = atf.DiffRescaleMask(episode)

qtgmcclip = hf.QTGMC(SAC_aa(episode), Preset='Very Slow', NoisePreset="Slower", ThSAD1=400, ThSAD2=200, EZDenoise=0, InputType=1, opencl=True).std.Trim(890, 976)
qtgmclines = core.std.MaskedMerge(SAC_aa(episode).std.Trim(890, 976), qtgmcclip, maskforQTGMC, planes=[0,1,2], first_plane=True)

qtgmclines.set_output()