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
episode = core.dgdecodenv.DGSource(r'03.dgi')
mask_clip = core.raws.Source(r'03.yuv').std.Trim(1, 121).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Prewitt().std.Maximum().std.Maximum().std.Deflate()
op_titles = core.std.Trim(episode, 656, 2813)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(24, 2181)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(24, 2181)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
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
mask_final = core.std.MaskedMerge(insaneaa.std.Trim(2838, 2958), episode.std.Trim(2838, 2958), mask_clip, planes=[0], first_plane=True)

mrgc = insaneaa.std.Trim(0, 655)+op+insaneaa.std.Trim(2814, 2837)+mask_final+insaneaa.std.Trim(2959, 3295)+stab.std.Trim(3296, 3399)+insaneaa.std.Trim(3400, 4815)+stab.std.Trim(4816, 5023)+insaneaa.std.Trim(5024, 6075)+stab.std.Trim(6076, 6155)+insaneaa.std.Trim(6156, 18313)+stab.std.Trim(18314, 18475)+insaneaa.std.Trim(18476, 26868)+stab2.std.Trim(26869, 26900)+insaneaa.std.Trim(26901, 28183)+insaneaa3.std.Trim(28184, 28289)+insaneaa.std.Trim(28290, 32058)+episode.std.Trim(32059, 34280)+stab4.std.Trim(34281, 34640)+episode.std.Trim(34641, 34664)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\03.png'), "[34575 34640]")

stab0 = havsfunc.QTGMC(mrgc, InputType=1, SourceMatch=3)
insaneaa22 = hiaa.HardAA(mrgc, mask='simple', mthr=30, useCL=True)
mrgc2 = mrgc.std.Trim(0, 2813)+insaneaa22.std.Trim(2814, 2867)+stab0.std.Trim(2868, 2997)+mrgc.std.Trim(2998, 34664)
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc, r'.\mask\28.png'), "[2814 2867]") 

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc2, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=14, thsadc=12, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=12, cb=10, cr=10, grainy=12, grainc=12, output_depth=16, keep_tv_range=True)
db2 = core.f3kdb.Deband(den, range=31, y=36, cb=10, cr=10, grainy=28, grainc=28, output_depth=16, keep_tv_range=True)
db3 = core.f3kdb.Deband(den, range=31, y=46, cb=10, cr=10, grainy=36, grainc=36, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(db2, clip16, Mask, planes=[0,1,2], first_plane=True)
filtered4 = core.std.MaskedMerge(db3, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
episode5 = core.fmtc.bitdepth(filtered4, bits=10)
mrgc3 = episode3.std.Trim(0, 11856)+episode4.std.Trim(11857, 12168)+episode3.std.Trim(12169, 12842)+episode4.std.Trim(12843, 12956)+episode3.std.Trim(12957, 13202)+episode4.std.Trim(13203, 13748)+episode3.std.Trim(13749, 14314)+episode4.std.Trim(14315, 14689)+episode3.std.Trim(14690, 32058)+episode5.std.Trim(32059, 34280)+episode3.std.Trim(34281, 34664)
mrgc3.set_output()




