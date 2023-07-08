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

core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'01.dgi')
insaneaa = BokugaAishitaSubetenoKimie_aa(episode)
mrgc = episode.std.Trim(0, 983)+insaneaa.std.Trim(984, 7883)+episode.std.Trim(7884, 8096)+insaneaa.std.Trim(8097, 139468)+episode.std.Trim(139469, 147191)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10.png'), "[8244 8362]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11.png'), "[8436 8554]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\12.png'), "[8676 8794]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\13.png'), "[8868 8986]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\14.png'), "[9036 9154]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\15.png'), "[9324 9441]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\16.png'), "[9612 9729]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\17.png'), "[10284 10402]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\18.png'), "[10548 10664]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\19.png'), "[10920 11038]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\20.png'), "[11358 11488]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\21.png'), "[11784 11903]")
denoise_deband = BokugaAishitaSubetenoKimie_denoise_deband(mrgc)
denoise_deband.set_output()




















