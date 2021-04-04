from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8
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
p_handle = psutil.Process()
p_handle.cpu_affinity([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46])
core.num_threads = 24

def fate_stay_night_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bilinear', descale_height=853) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv 

def fate_stay_night_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bilinear', descale_height=853) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30, useCL=True)
    return mixyuv  

def fate_stay_night_aa3(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bilinear', descale_height=853) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=60, useCL=True)
    return mixyuv 
     
def fate_stay_night_aa4(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bilinear', descale_height=853) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(clip, 1, GRAY)
    v = core.std.ShufflePlanes(clip, 2, GRAY)
    u = hiaa.HardAA(u, mask='simple', mthr=30, useCL=True)
    v = hiaa.HardAA(v, mask='simple', mthr=30, useCL=True)
    mixyuv = hiaa.HardAA(aa, mask='simple', mthr=30, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], clip.format.color_family)
    return mixyuv  
 
core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'02.dgi')
mask_clip = core.raws.Source(r'01.yuv').std.Trim(16, 136).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Prewitt().std.Maximum().std.Maximum().std.Deflate()
op_titles = core.std.Trim(episode, 3933, 6089)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(24, 2180)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(24, 2180)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 66078, 68233)
nced = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(25, 2180)
nced_aa = core.raws.Source(r'NCED.y4m').std.Trim(25, 2180)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = fate_stay_night_aa(episode)
insaneaa2 = fate_stay_night_aa2(episode)
insaneaa3 = fate_stay_night_aa3(episode)
insaneaa4 = fate_stay_night_aa4(episode)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa2, InputType=1, SourceMatch=3)
stab3 = havsfunc.QTGMC(insaneaa3, InputType=1, SourceMatch=3)
stab4 = havsfunc.QTGMC(insaneaa4, InputType=1, SourceMatch=3)
mask_final = core.std.MaskedMerge(insaneaa.std.Trim(6102, 6222), episode.std.Trim(6102, 6222), mask_clip, planes=[0], first_plane=True)

mrgc = insaneaa.std.Trim(0, 1394)+stab.std.Trim(1395, 1845)+insaneaa.std.Trim(1846, 3932)+op+insaneaa.std.Trim(6090, 6101)+mask_final+insaneaa.std.Trim(6223, 6232)+insaneaa2.std.Trim(6233, 6328)+insaneaa.std.Trim(6329, 6691)+stab.std.Trim(6692, 6823)+insaneaa.std.Trim(6824, 10206)+stab.std.Trim(10207, 10410)+insaneaa.std.Trim(10411, 13529)+stab.std.Trim(13530, 13613)+insaneaa.std.Trim(13614, 17687)+stab.std.Trim(17688, 17885)+insaneaa.std.Trim(17886, 18599)+insaneaa2.std.Trim(18600, 18700)+insaneaa.std.Trim(18701, 19779)+stab.std.Trim(19780, 19947)+insaneaa.std.Trim(19948, 21938)+stab.std.Trim(21939, 22019)+insaneaa.std.Trim(22020, 26479)+insaneaa2.std.Trim(26480, 26527)+insaneaa.std.Trim(26528, 28885)+stab.std.Trim(28886, 28941)+insaneaa.std.Trim(28942, 29109)+insaneaa2.std.Trim(29110, 29499)+insaneaa.std.Trim(29500, 30323)+insaneaa2.std.Trim(30324, 30594)+insaneaa.std.Trim(30595, 31646)+insaneaa2.std.Trim(31647, 31760)+insaneaa.std.Trim(31761, 34444)+stab.std.Trim(34445, 34522)+insaneaa.std.Trim(34523, 37369)+stab.std.Trim(37370, 37453)+insaneaa.std.Trim(37454, 55131)+insaneaa2.std.Trim(55132, 55203)+insaneaa.std.Trim(55204, 55999)+stab.std.Trim(56000, 56125)+insaneaa.std.Trim(56126, 63754)+stab.std.Trim(63755, 63934)+insaneaa.std.Trim(63935, 66077)+ed+stab3.std.Trim(68234, 68593)+episode.std.Trim(68594, 68617) 
 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\03.png'), "[18600 18700]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\15.png'), "[26480 26527]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\16.png'), "[29110 29499]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\17.png'), "[30324 30594]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\18.png'), "[31647 31760]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\19.png'), "[55132 55203]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\04.png'), "[68498 68593]") 

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=14, thsadc=12, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=12, cb=10, cr=10, grainy=12, grainc=12, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()









