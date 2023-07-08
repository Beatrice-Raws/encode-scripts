from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import GradFun3 as gfa
import insaneAA 

import cooldegrain
import finedehalo as fd
import HardAAp2 as hiaa
import descale as dsc
import psutil
import regress

p_handle = psutil.Process()
p_handle.cpu_affinity([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46])
core.num_threads = 24

def BokugaAishitaSubetenoKimie_denoise_deband(clip):
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    clip_y = mvf.GetPlane(clip16, 0)
    pf = core.dfttest.DFTTest(clip_y, sigma=2, tbsize=3, opt=3)
    pf2 = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[1,2])
    den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=22, thsadc=0, bits=16, blksize=8, overlap=4, pf=pf)
    filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
    filtered = cooldegrain.CoolDegrain(filtered, tr=1, thsad=0, thsadc=18, bits=16, blksize=8, overlap=4, pf=pf2)
    db = core.placebo.Deband(filtered, planes = 1, threshold = 3.0, grain = 6, radius = 16)
    Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False)
    Mask2 = core.std.Binarize(Mask, 9828,0)
    filtered1 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
    filtered2 = core.grain.Add(filtered1, var=0.2, uvar=0.2)
    filtered3 = core.std.ShufflePlanes([filtered2, filtered1, filtered1],[0,1,2], YUV)
    denoise_deband = core.fmtc.bitdepth(filtered3, bits=10)
    return  denoise_deband

core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'00019.dgi')
denoise_deband = BokugaAishitaSubetenoKimie_denoise_deband(episode)
denoise_deband.set_output()










