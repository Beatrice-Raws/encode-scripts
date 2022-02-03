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
    clip1 = dsc.Descale(gray, 640, 360, kernel="bilinear")
    clip1 = hiaa.HardAA(clip1, mask=None, alpha=0.9, beta=0.1, gamma=15.0, mdis=30)
    clip1 = insaneAA.rescale(clip1, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, pscrn=0, alpha=0.9, beta=0.1, gamma=10.0, mdis=30)
    mixyuv = core.std.ShufflePlanes([clip1, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=22, thma=140, rx=3, ry=3)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, cplace="mpeg2", blur=60)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=22, thma=140, rx=3, ry=3)
    return mixyuv
 
def oreigaru_aa2_5(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    clip1 = dsc.Descale(gray, 640, 360, kernel="bilinear")
    clip1 = hiaa.HardAA(clip1, mask=None, alpha=0.9, beta=0.1, gamma=15.0, mdis=30)
    clip1 = insaneAA.rescale(clip1, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, pscrn=0, alpha=0.9, beta=0.1, gamma=10.0, mdis=30)
    mixyuv = core.std.ShufflePlanes([clip1, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=2, showmask=0, thmi=22, thma=140, rx=3, ry=3)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, cplace="mpeg2", blur=60)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30, useCL=False)
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

def oreigaru_aa4(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080) 
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=45, useCL=False)
    return mixyuv
     
core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'01.dgi')
op_titles = core.std.Trim(episode, 1614, 3760)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(31, 2177)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(31, 2177)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 32056, 34042)
nced = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(171, 2157)
nced_aa = core.raws.Source(r'NCED.y4m').std.Trim(171, 2157)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = oreigaru_aa(episode)
insaneaa2 = oreigaru_aa2(episode)
insaneaa3 = oreigaru_aa3(episode)
insaneaa5 = oreigaru_aa4(episode)
insaneaa4 = oreigaru_aa2_5(episode)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa5, InputType=1, SourceMatch=3)
mask_clip = core.raws.Source(r'mask.yuv').std.Trim(6, 253).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Invert()
mask_final = core.std.MaskedMerge(insaneaa2.std.Trim(22850, 23097), insaneaa.std.Trim(22850, 23097), mask_clip, planes=[0], first_plane=True)
mask_clip2 = core.raws.Source(r'mask3.yuv').std.Trim(62, 140).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final2 = core.std.MaskedMerge(insaneaa2.std.Trim(31008, 31086), insaneaa.std.Trim(31008, 31086), mask_clip2, planes=[0], first_plane=True)
mask_clip3 = core.raws.Source(r'mask3.yuv').std.Trim(160, 207).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final3 = core.std.MaskedMerge(insaneaa4.std.Trim(31106, 31153), insaneaa.std.Trim(31106, 31153), mask_clip3, planes=[0], first_plane=True)

mrgc = insaneaa.std.Trim(0, 1613)+op+insaneaa.std.Trim(3761, 3946)+stab.std.Trim(3947, 4195)+insaneaa.std.Trim(4196, 19123)+stab.std.Trim(19124, 19297)+insaneaa.std.Trim(19298, 21251)+stab2.std.Trim(21252, 21431)+insaneaa.std.Trim(21432, 22849)+mask_final+insaneaa.std.Trim(23098, 31007)+mask_final2+insaneaa.std.Trim(31087, 31105)+mask_final3+insaneaa.std.Trim(31154, 32055)+ed+insaneaa.std.Trim(34043, 34782)

mrgc2 = mrgc.std.Trim(0, 792)+insaneaa3.std.Trim(793, 828)+mrgc.std.Trim(829, 12707)+insaneaa3.std.Trim(12708, 12815)+mrgc.std.Trim(12816, 13363)+insaneaa3.std.Trim(13364, 13495)+mrgc.std.Trim(13496, 15712)+insaneaa3.std.Trim(15713, 15796)+mrgc.std.Trim(15797, 19964)+insaneaa3.std.Trim(19965, 20050)+mrgc.std.Trim(20051, 22378)+insaneaa4.std.Trim(22379, 22465)+insaneaa3.std.Trim(22466, 22568)+mrgc.std.Trim(22569, 22849)+insaneaa2.std.Trim(22850, 23097)+mrgc.std.Trim(23098, 30163)+insaneaa3.std.Trim(30164, 30316)+mrgc.std.Trim(30317, 34782)
 
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc, r'.\mask\23.png'), "[793 828]") 
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc, r'.\mask\20.png'), "[12708 12815]")
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc, r'.\mask\24.png'), "[13364 13495]")
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc, r'.\mask\21.png'), "[15713 15796]")
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc, r'.\mask\25.png'), "[22379 22465]")
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc, r'.\mask\fix1_0.png'), "[22850 22855]")
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc, r'.\mask\fix1_1.png'), "[22856 22858]")
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc, r'.\mask\fix1_2.png'), "[22859 23023]")
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc, r'.\mask\fix1_3.png'), "[23024 23097]")

insaneaa5 = oreigaru_aa2_5(mrgc2)

mrgc3 = mrgc2.std.Trim(0, 31007)+insaneaa5.std.Trim(31008, 31086)+mrgc2.std.Trim(31087, 34782)
 
mrgc3 = fvf.rfs(mrgc3, atf.ApplyImageMask(mrgc3, mrgc2, r'.\mask\22.png'), "[31008 31086]")

insaneaa6 = oreigaru_aa2_5(mrgc3)

mrgc4 = mrgc3.std.Trim(0, 31007)+insaneaa6.std.Trim(31008, 31086)+mrgc3.std.Trim(31087, 34782)

mrgc4 = fvf.rfs(mrgc4, atf.ApplyImageMask(mrgc4, mrgc3, r'.\mask\30.png'), "[31008 31086]")
 
#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc4, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=20, thsadc=16, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=16, cb=11, cr=11, grainy=18, grainc=18, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()





 







