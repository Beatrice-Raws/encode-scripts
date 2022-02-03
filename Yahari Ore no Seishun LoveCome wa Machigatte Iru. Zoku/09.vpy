from vapoursynth import core, VideoNode, GRAY8, YUV, GRAY
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

def oreigaru2_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.35, kernel='bicubic', descale_height=720, bicubic_b=0, bicubic_c=0.75) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.68, showmask=0, thmi=42, thma=100, rx=2.3, ry=2.3)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

def oreigaru2_aa2_5(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    clip1 = dsc.Descale(gray, 1136, 640, kernel="bilinear")
    clip1 = hiaa.HardAA(clip1, mask=None, alpha=0.9, beta=0.1, gamma=15.0, mdis=30)
    clip1 = insaneAA.rescale(clip1, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, pscrn=0, alpha=0.9, beta=0.1, gamma=10.0, mdis=30)
    mixyuv = core.std.ShufflePlanes([clip1, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=2, showmask=0, thmi=22, thma=140, rx=3, ry=3)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, cplace="mpeg2", blur=60)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30, useCL=False)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=22, thma=140, rx=3, ry=3)
    return mixyuv  
     
core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'09.dgi')
op_titles = core.std.Trim(episode, 2518, 4670)
ncop = core.raws.Source(r'NCOP_ep9_no_aa.y4m').std.Trim(72, 2224)
ncop_aa = core.raws.Source(r'NCOP_ep9_aa.y4m').std.Trim(72, 2224)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 31885, 34040)
nced = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(74, 2229)
nced_aa = core.raws.Source(r'NCED.y4m').std.Trim(74, 2229)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = oreigaru2_aa(episode)
insaneaa2 = oreigaru2_aa2_5(episode)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 2517)+op+insaneaa.std.Trim(4671, 8073)+insaneaa2.std.Trim(8074, 8145)+insaneaa.std.Trim(8146, 19648)+stab.std.Trim(19649, 19828)+insaneaa.std.Trim(19829, 31786)+episode.std.Trim(31787, 31884)+ed+insaneaa.std.Trim(34041, 34756)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\07.png'), "[8074 8145]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08\01.png'), "[34041 34756]")
 
#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=26, thsadc=16, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=30, cb=11, cr=11, grainy=41, grainc=41, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()

