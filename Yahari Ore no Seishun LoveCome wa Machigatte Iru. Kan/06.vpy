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

def oreigaru3_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=0.78, showmask=0, thmi=24, thma=100, rx=2.4, ry=2.4)
    return mixyuv

def oreigaru3_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=0.78, showmask=0, thmi=24, thma=100, rx=2.4, ry=2.4)
    mixyuv = hiaa.HardAA(mixyuv, mask=None, useCL=False)
    return mixyuv

def oreigaru3_aa2_6(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    clip1 = dsc.Descale(gray, 1136, 640, kernel="bilinear")
    clip1 = hiaa.HardAA(clip1, mask=None, alpha=0.9, beta=0.1, gamma=15.0, mdis=30)
    clip1 = insaneAA.rescale(clip1, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, pscrn=0, alpha=0.9, beta=0.1, gamma=10.0, mdis=30)
    mixyuv = core.std.ShufflePlanes([clip1, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, cplace="mpeg2", blur=60)
    mixyuv = hiaa.HardAA(mixyuv, mask=None, useCL=False)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    return mixyuv

def oreigaru3_aa2_7(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    clip1 = dsc.Descale(gray, 1136, 640, kernel="bilinear")
    clip1 = hiaa.HardAA(clip1, mask=None, alpha=0.9, beta=0.1, gamma=15.0, mdis=30)
    clip1 = insaneAA.rescale(clip1, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, pscrn=0, alpha=0.9, beta=0.1, gamma=10.0, mdis=30)
    mixyuv = core.std.ShufflePlanes([clip1, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, cplace="mpeg2", blur=40)
    mixyuv = hiaa.HardAA(mixyuv, mask=None, useCL=False)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    return mixyuv
    
def oreigaru3_aa3(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=0.78, showmask=0, thmi=24, thma=100, rx=2.4, ry=2.4)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=40, useCL=False)
    return mixyuv     
     
core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'06.dgi')
op_titles = core.std.Trim(episode, 1366, 3524)
ncop = core.dgdecodenv.DGSource(r'NCOP3.dgi').std.Trim(0, 2158)
ncop_aa = core.raws.Source(r'NCOP3.y4m').std.Trim(0, 2158)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 31769, 33926)
nced = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(0, 2157)
nced_aa = core.raws.Source(r'NCED.y4m').std.Trim(0, 2157)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = oreigaru3_aa(episode)
insaneaa2 = oreigaru3_aa2(episode)
insaneaa4 = oreigaru3_aa2_6(episode)
insaneaa5 = oreigaru3_aa2_7(episode)
insaneaa3 = oreigaru3_aa3(episode)
stab0 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=1)
stab2 = havsfunc.QTGMC(stab, InputType=1, SourceMatch=2)
stab3 = havsfunc.QTGMC(stab2, InputType=1, SourceMatch=3)
mask_clip = core.raws.Source(r'mask.yuv').std.Trim(1007, 1049).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final = core.std.MaskedMerge(insaneaa4.std.Trim(12062, 12080), insaneaa.std.Trim(12062, 12080), mask_clip, planes=[0], first_plane=True)

mrgc = insaneaa.std.Trim(0, 1365)+op+insaneaa.std.Trim(3525, 9040)+insaneaa2.std.Trim(9041, 9122)+insaneaa.std.Trim(9123, 9179)+insaneaa3.std.Trim(9180, 9242)+insaneaa.std.Trim(9243, 12061)+mask_final+insaneaa.std.Trim(12081, 15632)+insaneaa4.std.Trim(15633, 15740)+insaneaa.std.Trim(15741, 16210)+insaneaa4.std.Trim(16211, 16531)+insaneaa.std.Trim(16532, 16596)+insaneaa2.std.Trim(16597, 16650)+insaneaa.std.Trim(16651, 17441)+insaneaa2.std.Trim(17442, 17657)+insaneaa.std.Trim(17658, 28545)+insaneaa5.std.Trim(28546, 28593)+insaneaa.std.Trim(28594, 29107)+stab0.std.Trim(29108, 29239)+insaneaa.std.Trim(29240, 31672)+episode.std.Trim(31673, 31768)+ed+insaneaa.std.Trim(33927, 33967)+stab3.std.Trim(33968, 34045)+insaneaa.std.Trim(34046, 34574)+episode.std.Trim(34575, 34671)
 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\22.png'), "[9041 9122]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\28.png'), "[15633 15740]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\23.png'), "[16211 16261]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\24.png'), "[16262 16531]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\25.png'), "[16597 16650]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\26.png'), "[17442 17657]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\27.png'), "[28546 28593]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=18, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=20, cb=10, cr=10, grainy=28, grainc=28, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()










