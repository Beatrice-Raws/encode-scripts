from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import GradFun3 as gfa
import insaneAA 
import finesharp
import cooldegrain
import finedehalo as fd
import HardAAp2 as hiaa
import descale as dsc
import psutil
import regress
p_handle = psutil.Process()
p_handle.cpu_affinity([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46])
core.num_threads = 24

def Vivy_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='lanczos', descale_height=864, lanczos_taps = 1)
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=10, thma=60, thlimi=10, thlima=60, rx=2.3, ry=2.3, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

def Vivy_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='lanczos', descale_height=864, lanczos_taps = 1)
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=10, thma=60, thlimi=10, thlima=60, rx=2.3, ry=2.3, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask=None, useCL=False)
    return mixyuv

core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'07.dgi')
op_titles = core.std.Trim(episode, 418, 2828)
ncop = core.dgdecodenv.DGSource(r'NCOP5.dgi').std.Trim(24, 2434)
ncop_aa = core.raws.Source(r'NCOP5.y4m').std.Trim(24, 2434)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 31528, 33685)
nced = core.dgdecodenv.DGSource(r'NCED3.dgi').std.Trim(24, 2181)
nced_aa = core.raws.Source(r'NCED3.y4m').std.Trim(24, 2181)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Vivy_aa(episode)
insaneaa2 = Vivy_aa2(episode)
stab0 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=1)
stab2 = havsfunc.QTGMC(stab, InputType=1, SourceMatch=2)
stab3 = havsfunc.QTGMC(stab2, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 417)+op+insaneaa.std.Trim(2829, 4133)+stab3.std.Trim(4134, 4183)+insaneaa.std.Trim(4184, 5610)+stab3.std.Trim(5611, 5687)+insaneaa.std.Trim(5688, 5843)+stab3.std.Trim(5844, 5987)+insaneaa.std.Trim(5988, 6107)+stab3.std.Trim(6108, 6356)+insaneaa.std.Trim(6357, 12278)+stab3.std.Trim(12279, 12512)+insaneaa.std.Trim(12513, 12679)+stab3.std.Trim(12680, 12872)+insaneaa.std.Trim(12873, 13015)+stab3.std.Trim(13016, 13255)+insaneaa.std.Trim(13256, 21132)+stab3.std.Trim(21133, 21276)+insaneaa.std.Trim(21277, 23243)+insaneaa2.std.Trim(23244, 23398)+insaneaa.std.Trim(23399, 24525)+stab3.std.Trim(24526, 24645)+insaneaa.std.Trim(24646, 31527)+ed+insaneaa.std.Trim(33686, 34045)+episode.std.Trim(34046, 34071)
 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\95.png'), "[2835 2941]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\110.png'), "[23244 23398]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\96.png'), "[33951 34045]")

#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()
#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
pf2 = core.dfttest.DFTTest(clip16, sigma=7, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=14, thsadc=10, bits=16, blksize=8, overlap=4, pf=pf)
den2 = cooldegrain.CoolDegrain(clip16, tr=1, thsad=28, thsadc=22, bits=16, blksize=8, overlap=4, pf=pf2)
db = core.placebo.Deband(den, planes = 1, threshold = 0.8, grain = 6.2, radius = 10)
db2 = core.placebo.Deband(den2, planes = 1 | 2 | 4, threshold = 4.0, grain = 6.2, radius = 16)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
filtered3 = core.std.MaskedMerge(db2, clip16, Mask, planes=[0,1,2], first_plane=True)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
mrgc2 = episode3.std.Trim(0, 33872)+episode4.std.Trim(33873, 33904)+episode3.std.Trim(33905, 34071)
mrgc2.set_output()







