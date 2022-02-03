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
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30, useCL=False)
    return mixyuv
    
def oreigaru_aa2_6(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    clip1 = dsc.Descale(gray, 1136, 640, kernel="bilinear")
    clip1 = hiaa.HardAA(clip1, mask=None, alpha=0.9, beta=0.1, gamma=15.0, mdis=30)
    clip1 = insaneAA.rescale(clip1, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, pscrn=0, alpha=0.9, beta=0.1, gamma=10.0, mdis=30)
    mixyuv = core.std.ShufflePlanes([clip1, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=22, thma=140, rx=3, ry=3)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, cplace="mpeg2", planes=[0], blur=10)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=22, thma=140, rx=3, ry=3)
    return mixyuv
    
def oreigaru_aa2_7(clip):
    clip = clip
    clip = hiaa.HardAA(clip, mask='simple', mthr=40, useCL=False)
    return clip     
     
core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'11.dgi')
op_titles = core.std.Trim(episode, 1830, 3976)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(31, 2177)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(31, 2177)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 32056, 34042)
nced = core.dgdecodenv.DGSource(r'00057.dgi').std.Trim(195, 2181)
nced_aa = core.raws.Source(r'NCED4.y4m').std.Trim(195, 2181)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = oreigaru_aa(episode)
insaneaa2 = oreigaru_aa2(episode)
insaneaa4 = oreigaru_aa2_6(episode)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa2, InputType=1, SourceMatch=3)
mask_clip = core.raws.Source(r'mask4.yuv').std.Trim(13, 84).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final = core.std.MaskedMerge(insaneaa4.std.Trim(10530, 10601), insaneaa.std.Trim(10530, 10601), mask_clip, planes=[0], first_plane=True)
mask_clip2 = core.raws.Source(r'mask4.yuv').std.Trim(151, 332).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final2 = core.std.MaskedMerge(insaneaa4.std.Trim(13152, 13333), insaneaa.std.Trim(13152, 13333), mask_clip2, planes=[0], first_plane=True)

mrgc = insaneaa.std.Trim(0, 1829)+op+insaneaa.std.Trim(3977, 10529)+mask_final+insaneaa.std.Trim(10602, 12256)+insaneaa2.std.Trim(12257, 12415)+insaneaa.std.Trim(12416, 13151)+mask_final2+insaneaa.std.Trim(13334, 16048)+insaneaa2.std.Trim(16049, 16210)+insaneaa.std.Trim(16211, 18352)+insaneaa2.std.Trim(18353, 18427)+insaneaa.std.Trim(18428, 19518)+insaneaa4.std.Trim(19519, 19554)+insaneaa.std.Trim(19555, 20292)+stab.std.Trim(20293, 20631)+insaneaa.std.Trim(20632, 32055)+ed+insaneaa.std.Trim(34043, 34099)+stab2.std.Trim(34100, 34213)+insaneaa.std.Trim(34214, 34503)+stab2.std.Trim(34504, 34561)+insaneaa.std.Trim(34562, 34782)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\33.png'), "[19519 19554]")
insaneaa5 = oreigaru_aa2_7(mrgc)
mrgc2 = mrgc.std.Trim(0, 10529)+insaneaa5.std.Trim(10530, 10601)+mrgc.std.Trim(10602, 34782)

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc2, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=20, thsadc=16, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=16, cb=11, cr=11, grainy=18, grainc=18, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()









