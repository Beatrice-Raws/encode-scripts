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
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=855, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv 

def fate_stay_night_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=855, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30, useCL=True)
    return mixyuv  

def fate_stay_night_aa3(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=855, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=80, useCL=True)
    return mixyuv 
     
def fate_stay_night_aa4(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=855, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(clip, 1, GRAY)
    v = core.std.ShufflePlanes(clip, 2, GRAY)
    u = hiaa.HardAA(u, mask='simple', mthr=30, useCL=True)
    v = hiaa.HardAA(v, mask='simple', mthr=30, useCL=True)
    mixyuv = hiaa.HardAA(aa, mask='simple', mthr=30, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], clip.format.color_family)
    return mixyuv

def fate_stay_night_aa5(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=855, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=60, useCL=True)
    return mixyuv    
  
core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'13.dgi')
mask_clip = core.raws.Source(r'13.yuv').std.Trim(4, 124).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Prewitt().std.Maximum().std.Maximum().std.Deflate()
ed_titles = core.std.Trim(episode, 31042, 32617)
nced = core.dgdecodenv.DGSource(r'NCED_EP14.dgi').std.Trim(726, 2301)
nced_aa = core.raws.Source(r'NCED_EP13.y4m').std.Trim(726, 2301)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = fate_stay_night_aa(episode)
insaneaa2 = fate_stay_night_aa2(episode)
insaneaa3 = fate_stay_night_aa3(episode)
insaneaa4 = fate_stay_night_aa4(episode)
insaneaa5 = fate_stay_night_aa5(episode)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa2, InputType=1, SourceMatch=3)
stab3 = havsfunc.QTGMC(insaneaa3, InputType=1, SourceMatch=3)
stab4 = havsfunc.QTGMC(insaneaa4, InputType=1, SourceMatch=3)
stab5 = havsfunc.QTGMC(insaneaa5, InputType=1, SourceMatch=3)
mask_final = core.std.MaskedMerge(insaneaa.std.Trim(1690, 1810), episode.std.Trim(1690, 1810), mask_clip, planes=[0], first_plane=True)

mrgc = insaneaa.std.Trim(0, 1389)+stab.std.Trim(1390, 1545)+episode.std.Trim(1546, 1677)+insaneaa.std.Trim(1678, 1689)+mask_final+insaneaa.std.Trim(1811, 2556)+stab.std.Trim(2557, 2625)+insaneaa.std.Trim(2626, 2676)+stab.std.Trim(2677, 2769)+insaneaa.std.Trim(2770, 3273)+stab.std.Trim(3274, 3333)+insaneaa.std.Trim(3334, 4053)+stab.std.Trim(4054, 4497)+insaneaa.std.Trim(4498, 4797)+stab.std.Trim(4798, 5115)+insaneaa.std.Trim(5116, 6783)+stab.std.Trim(6784, 6966)+insaneaa.std.Trim(6967, 9005)+stab5.std.Trim(9006, 9221)+insaneaa.std.Trim(9222, 11749)+stab.std.Trim(11750, 11821)+insaneaa.std.Trim(11822, 16953)+stab.std.Trim(16954, 17109)+insaneaa.std.Trim(17110, 17478)+stab.std.Trim(17479, 17543)+insaneaa.std.Trim(17544, 22849)+stab.std.Trim(22850, 23245)+insaneaa.std.Trim(23246, 25463)+stab5.std.Trim(25464, 25685)+insaneaa.std.Trim(25686, 26180)+insaneaa2.std.Trim(26181, 26246)+stab.std.Trim(26247, 26360)+insaneaa.std.Trim(26361, 26948)+insaneaa2.std.Trim(26949, 27260)+insaneaa.std.Trim(27261, 27995)+stab5.std.Trim(27996, 28205)+insaneaa2.std.Trim(28206, 28421)+stab.std.Trim(28422, 28678)+insaneaa.std.Trim(28679, 28951)+stab.std.Trim(28952, 29158)+insaneaa.std.Trim(29159, 31041)+ed+insaneaa.std.Trim(32618, 34003)+episode.std.Trim(34004, 34094)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\40.png'), "[26181 26246]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\41.png'), "[26949 27260]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\42.png'), "[28206 28421]")

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







