from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS, YUV420P16, YUV444P16
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc as hf
import mvsfunc as mvf
import GradFun3 as gfa
import insaneAA 
import cooldegrain
import finedehalo as fd
import HardAAp2 as hiaa
import descale as dsc
import functools
import math
import psutil
import regress
core.max_cache_size = 120000

def Natsu_Eno_Tunnel_Sayonara_No_Deguchi_denoise_deband(clip):
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    clip_y = mvf.GetPlane(clip16, 0)
    pf = core.dfttest.DFTTest(clip_y, sigma=1, tbsize=3, opt=3)
    pf2 = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[1,2])
    den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=20, thsadc=0, bits=16, blksize=8, overlap=4, pf=pf)
    filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
    filtered = cooldegrain.CoolDegrain(filtered, tr=1, thsad=0, thsadc=18, bits=16, blksize=8, overlap=4, pf=pf2)
    db = core.placebo.Deband(filtered, planes = 1, threshold = 0.8, grain = 8, radius = 10)
    Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
    Mask2 = core.std.Binarize(Mask, 9828,0)
    filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
    denoise_deband = core.fmtc.bitdepth(filtered2, bits=10)
    return  denoise_deband

def Natsu_Eno_Tunnel_Sayonara_No_Deguchi_denoise_deband_scene(clip):
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    pf = core.dfttest.DFTTest(clip16, sigma=7, tbsize=3, opt=3)
    den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=64, thsadc=64, bits=16, blksize=8, overlap=4, pf=pf)
    db = core.placebo.Deband(den, planes = 1, threshold = 16, grain = 16, radius = 16, iterations = 4)
    db = core.grain.Add(db, var=1.5, uvar=1.5, opt=2)
    denoise_deband = core.fmtc.bitdepth(db, bits=10)
    return  denoise_deband

episode = core.dgdecodenv.DGSource(r'00001.dgi')
episode = core.std.Crop(episode, top=138, bottom=138)
episode_db = Natsu_Eno_Tunnel_Sayonara_No_Deguchi_denoise_deband(episode)
episode_db_scene = Natsu_Eno_Tunnel_Sayonara_No_Deguchi_denoise_deband_scene(episode)
mrgc = episode_db.std.Trim(0, 243)+episode_db_scene.std.Trim(244, 291)+episode_db.std.Trim(292, 420)+episode_db_scene.std.Trim(421, 466)+episode_db.std.Trim(467, 1463)
mrgc.set_output()














