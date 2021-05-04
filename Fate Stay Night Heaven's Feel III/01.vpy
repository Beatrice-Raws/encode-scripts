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

def rotate_clockwise(clip: VideoNode) -> VideoNode:
    return clip.std.Transpose().std.FlipHorizontal()

def rotate_counterclockwise(clip: VideoNode) -> VideoNode:
    return clip.std.Transpose().std.FlipVertical()
 
def mangle_luma(clip: VideoNode) -> VideoNode:
    luma = mvf.GetPlane(clip,0)
    luma_mangled = luma.resize.Point(960,1080, src_left=-1).resize.Bicubic(960,540, filter_param_a=0.33, filter_param_b=0.33)
    return luma_mangled    
  
def demangle_plane(clip: VideoNode) -> VideoNode:
    descaled = mvf.GetPlane(clip,0)
    descaled = descaled.resize.Bicubic(960,1080, filter_param_a=0.33, filter_param_b=0.33, format=GRAYS)
    rotated = rotate_clockwise(descaled)
    interpolated = rotated.eedi3m.EEDI3(field=1, dh=True, alpha=0.4,beta=0.25,gamma=20.0,nrad=2,mdis=20, hp=False,ucubic=True,cost3=True,vcheck=3,vthresh0=32,vthresh1=64,vthresh2=4, sclip=rotated.nnedi3.nnedi3(field=1, dh=True, nsize=0, nns=4, pscrn=1, qual=2), opt=4)
    interpolated = rotate_counterclockwise(interpolated)
    return interpolated

def do_chroma_aa(clip: VideoNode) -> VideoNode:
    luma_descaled = mvf.GetPlane(clip,0)
    luma_mangled = mangle_luma(luma_descaled)
    reconstructed = regress.Reconstruct(luma_descaled.resize.Bicubic(format=GRAYS),
                                        demangle_plane(luma_mangled),
                                        demangle_plane(mvf.GetPlane(clip, 1)),
                                        demangle_plane(mvf.GetPlane(clip, 2)),  use_binary=True)
    reconstructed = core.fmtc.resample(reconstructed, css='420')                                    
    return core.std.ShufflePlanes([clip, reconstructed],[0,1,2], YUV)

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
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30)
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
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=50)
    return mixyuv
    
core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'Film.dgi')
episode = core.fmtc.bitdepth(episode, bits=16)
insaneaa = fate_stay_night_aa(episode)
insaneaa2 = fate_stay_night_aa2(episode)
insaneaa3 = fate_stay_night_aa3(episode)
insaneaa4 = fate_stay_night_aa4(episode)
insaneaa5 = fate_stay_night_aa5(episode)
insaneaa6 = do_chroma_aa(insaneaa2)
insaneaa7 = do_chroma_aa(insaneaa)
insaneaa8 = do_chroma_aa(insaneaa5)
stab0 = havsfunc.QTGMC(episode, InputType=1, SourceMatch=3)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa2, InputType=1, SourceMatch=3)
stab3 = havsfunc.QTGMC(insaneaa3, InputType=1, SourceMatch=3)
stab4 = havsfunc.QTGMC(insaneaa4, InputType=1, SourceMatch=3)
stab5 = havsfunc.QTGMC(insaneaa5, InputType=1, SourceMatch=3)

mrgc = episode.std.Trim(0, 527)+insaneaa.std.Trim(528, 5335)+stab.std.Trim(5336, 5473)+insaneaa.std.Trim(5474, 5617)+stab.std.Trim(5618, 6235)+insaneaa.std.Trim(6236, 7545)+stab.std.Trim(7546, 7743)+insaneaa.std.Trim(7744, 8167)+insaneaa7.std.Trim(8168, 8239)+stab.std.Trim(8240, 8329)+insaneaa.std.Trim(8330, 8490)+insaneaa7.std.Trim(8491, 8553)+stab.std.Trim(8554, 8661)+insaneaa.std.Trim(8662, 9905)+insaneaa8.std.Trim(9906, 10076)+insaneaa.std.Trim(10077, 10494)+insaneaa6.std.Trim(10495, 10563)+insaneaa.std.Trim(10564, 12869)+stab.std.Trim(12870, 13175)+insaneaa.std.Trim(13176, 18017)+stab.std.Trim(18018, 18544)+stab0.std.Trim(18545, 18857)+insaneaa.std.Trim(18858, 24687)+insaneaa5.std.Trim(24688, 25117)+stab5.std.Trim(25118, 25285)+insaneaa.std.Trim(25286, 25423)+stab.std.Trim(25424, 25705)+insaneaa.std.Trim(25706, 26183)+insaneaa5.std.Trim(26184, 26361)+insaneaa.std.Trim(26362, 27994)+stab5.std.Trim(27995, 28070)+insaneaa.std.Trim(28071, 28700)+stab.std.Trim(28701, 28782)+insaneaa.std.Trim(28783, 36701)+stab5.std.Trim(36702, 36753)+insaneaa.std.Trim(36754, 37075)+stab.std.Trim(37076, 37240)+insaneaa.std.Trim(37241, 40192)+stab2.std.Trim(40193, 40278)+insaneaa.std.Trim(40279, 58476)+stab.std.Trim(58477, 58772)+insaneaa.std.Trim(58773, 66034)+stab2.std.Trim(66035, 66400)+insaneaa.std.Trim(66401, 70467)+stab.std.Trim(70468, 70773)+insaneaa.std.Trim(70774, 80848)+stab.std.Trim(80849, 81012)+insaneaa.std.Trim(81013, 83384)+stab.std.Trim(83385, 83666)+insaneaa.std.Trim(83667, 86837)+stab.std.Trim(86838, 86911)+insaneaa.std.Trim(86912, 98643)+insaneaa2.std.Trim(98644, 98742)+insaneaa.std.Trim(98743, 101744)+insaneaa7.std.Trim(101745, 101921)+insaneaa.std.Trim(101922, 103401)+insaneaa7.std.Trim(103402, 103658)+insaneaa.std.Trim(103659, 118409)+stab.std.Trim(118410, 118731)+insaneaa.std.Trim(118732, 120082)+stab.std.Trim(120083, 120204)+insaneaa.std.Trim(120205, 122006)+insaneaa7.std.Trim(122007, 122222)+insaneaa.std.Trim(122223, 124786)+stab.std.Trim(124787, 125125)+insaneaa.std.Trim(125126, 127170)+stab.std.Trim(127171, 127290)+insaneaa.std.Trim(127291, 137984)+insaneaa7.std.Trim(137985, 138068)+insaneaa.std.Trim(138069, 142363)+stab.std.Trim(142364, 142765)+insaneaa.std.Trim(142766, 154849)+stab2.std.Trim(154850, 154993)+insaneaa.std.Trim(154994, 162734)+stab.std.Trim(162735, 163613)+insaneaa.std.Trim(163614, 165753)+stab.std.Trim(165754, 165921)+insaneaa.std.Trim(165922, 166540)+stab.std.Trim(166541, 166628)+insaneaa.std.Trim(166629, 168066)+stab.std.Trim(168067, 168152)+insaneaa.std.Trim(168153, 169752)+stab.std.Trim(169753, 169872)+insaneaa.std.Trim(169873, 170740)+episode.std.Trim(170741, 175631)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[16299 16403]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\02.png'), "[16441 16547]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\03.png'), "[16585 16681]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\04.png'), "[16694 16765]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\05.png'), "[16786 16857]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\06.png'), "[16869 16942]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\07.png'), "[16963 17039]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[17062 17140]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\09.png'), "[17167 17248]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10.png'), "[17270 17343]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11.png'), "[17369 17435]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\12.png'), "[17730 17818]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\13.png'), "[18117 18250]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\14.png'), "[98644 98742]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = mrgc
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=24, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=30, y=12, cb=10, cr=10, grainy=14, grainc=14, output_depth=16, keep_tv_range=True)
db2 = core.f3kdb.Deband(den, range=31, y=36, cb=10, cr=10, grainy=28, grainc=28, output_depth=16, keep_tv_range=True)
db3 = core.f3kdb.Deband(den, range=31, y=56, cb=20, cr=20, grainy=48, grainc=48, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(db2, clip16, Mask, planes=[0,1,2], first_plane=True)
filtered4 = core.std.MaskedMerge(db3, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
episode5 = core.fmtc.bitdepth(filtered4, bits=10)
mrgc3 = episode3.std.Trim(0, 18338)+episode4.std.Trim(18339, 18544)+episode3.std.Trim(18545, 104296)+episode4.std.Trim(104297, 104523)+episode3.std.Trim(104524, 114724)+episode4.std.Trim(114725, 114904)+episode3.std.Trim(114905, 175631)
mrgc3.set_output()

















