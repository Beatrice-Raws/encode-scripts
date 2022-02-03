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

def oreigaru_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080) 
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv
  
def oreigaru_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080) 
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=45, useCL=True)
    return mixyuv

def oreigaru_aa2_5(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    clip1 = dsc.Descale(gray, 640, 360, kernel="bilinear")
    clip1 = hiaa.HardAA(clip1, mask=None, alpha=0.9, beta=0.1, gamma=15.0, mdis=30)
    clip1 = insaneAA.rescale(clip1, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, pscrn=0, alpha=0.9, beta=0.1, gamma=10.0, mdis=30)
    mixyuv = core.std.ShufflePlanes([clip1, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=22, thma=140, rx=3, ry=3)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, cplace="mpeg2", blur=60)
    mixyuv = hiaa.HardAA(mixyuv, mask=None, useCL=False)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, cplace="mpeg2", blur=60)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=22, thma=140, rx=3, ry=3)
    return mixyuv  
	
def oreigaru_aa3(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080) 
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30, useCL=False)
    return mixyuv
     
core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'10.dgi')
op_titles = core.std.Trim(episode, 1039, 3184)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(31, 2176)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(31, 2176)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 32056, 34042)
nced = core.dgdecodenv.DGSource(r'00057.dgi').std.Trim(195, 2181)
nced_aa = core.raws.Source(r'NCED4.y4m').std.Trim(195, 2181)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = oreigaru_aa(episode)
insaneaa2 = oreigaru_aa2(episode)
insaneaa3 = oreigaru_aa3(episode)
insaneaa4 = oreigaru_aa2_5(episode)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa3, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 173)+insaneaa3.std.Trim(174, 251)+insaneaa.std.Trim(252, 1038)+op+insaneaa.std.Trim(3185, 21443)+stab.std.Trim(21444, 21509)+insaneaa.std.Trim(21510, 27271)+stab.std.Trim(27272, 27421)+insaneaa.std.Trim(27422, 29155)+stab.std.Trim(29156, 29281)+insaneaa.std.Trim(29282, 30841)+stab2.std.Trim(30842, 30931)+insaneaa4.std.Trim(30932, 30979)+insaneaa.std.Trim(30980, 32055)+ed+insaneaa.std.Trim(34043, 34783)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\32.png'), "[30932 30979]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=20, thsadc=16, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=16, cb=11, cr=11, grainy=18, grainc=18, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()










