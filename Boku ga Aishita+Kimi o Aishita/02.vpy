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

def BokugaAishitaSubetenoKimie_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='lanczos', descale_height=876, lanczos_taps = 3)
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, gamma=50)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    graydh = fd.fine_dehalo(aa, darkstr=0, brightstr=0.70, showmask=0, thlimi=40, thlima=80, thmi=40, thma=80, rx=2.2, ry=2.2, useMtEdge=True, lowsens=10, highsens=90, ss=1, edgeproc=1)
    mixyuv = core.std.ShufflePlanes([graydh, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

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
    filtered2 = core.grain.Add(filtered1, var=0.3, uvar=0.2)
    filtered3 = core.std.ShufflePlanes([filtered2, filtered1, filtered1],[0,1,2], YUV)
    denoise_deband = core.fmtc.bitdepth(filtered3, bits=10)
    return  denoise_deband

def BokugaAishitaSubetenoKimie_denoise_deband2(clip):
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    clip_y = mvf.GetPlane(clip16, 0)
    pf = core.dfttest.DFTTest(clip_y, sigma=7, tbsize=3, opt=3)
    pf2 = core.dfttest.DFTTest(clip16, sigma=7, tbsize=3, opt=3, planes=[1,2])
    den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=42, thsadc=0, bits=16, blksize=8, overlap=4, pf=pf)
    filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
    filtered = cooldegrain.CoolDegrain(filtered, tr=1, thsad=0, thsadc=28, bits=16, blksize=8, overlap=4, pf=pf2)
    db = core.placebo.Deband(filtered, planes = 1 | 2 | 4, threshold = 8.0, grain = 8, radius = 16)
    filtered2 = core.grain.Add(db, var=0.4, uvar=0.2)
    denoise_deband = core.fmtc.bitdepth(filtered2, bits=10)
    return  denoise_deband

core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'02.dgi')
insaneaa = BokugaAishitaSubetenoKimie_aa(episode)
mrgc = episode.std.Trim(0, 1657)+insaneaa.std.Trim(1658, 4667)+episode.std.Trim(4668, 5099)+insaneaa.std.Trim(5100, 128285)+episode.std.Trim(128286, 136163)+insaneaa.std.Trim(136164, 141599)+episode.std.Trim(141600, 141935)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[1875 1991]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\02.png'), "[2015 2129]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\03.png'), "[2159 2276]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\04.png'), "[2303 2420]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\05.png'), "[2526 2643]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\06.png'), "[2663 2781]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\07.png'), "[2811 2929]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[2956 3073]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\09.png'), "[3189 3323]")
denoise_deband = BokugaAishitaSubetenoKimie_denoise_deband(mrgc)
denoise_deband2 = BokugaAishitaSubetenoKimie_denoise_deband2(mrgc)
mrgc2 = denoise_deband.std.Trim(0, 599)+denoise_deband2.std.Trim(600, 1657)+denoise_deband.std.Trim(1658, 141935)
mrgc2.set_output()










