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
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa2, InputType=1, SourceMatch=3)
stab3 = havsfunc.QTGMC(insaneaa3, InputType=1, SourceMatch=3)
stab4 = havsfunc.QTGMC(insaneaa4, InputType=1, SourceMatch=3)
stab5 = havsfunc.QTGMC(insaneaa5, InputType=1, SourceMatch=3)

mrgc = episode.std.Trim(0, 599)+insaneaa.std.Trim(600, 6230)+episode.std.Trim(6231, 6500)+insaneaa.std.Trim(6501, 21834)+insaneaa2.std.Trim(21835, 21894)+insaneaa.std.Trim(21895, 24801)+insaneaa2.std.Trim(24802, 24879)+insaneaa.std.Trim(24880, 25113)+insaneaa2.std.Trim(25114, 25229)+insaneaa.std.Trim(25230, 30303)+insaneaa2.std.Trim(30304, 30349)+insaneaa.std.Trim(30350, 32385)+insaneaa5.std.Trim(32386, 32623)+insaneaa.std.Trim(32624, 34497)+insaneaa7.std.Trim(34498, 34557)+insaneaa.std.Trim(34558, 34956)+insaneaa2.std.Trim(34957, 35040)+insaneaa.std.Trim(35041, 37580)+insaneaa5.std.Trim(37581, 37682)+insaneaa.std.Trim(37683, 37862)+insaneaa5.std.Trim(37863, 38130)+insaneaa.std.Trim(38131, 38258)+stab.std.Trim(38259, 38378)+insaneaa.std.Trim(38379, 41478)+stab2.std.Trim(41479, 41559)+insaneaa.std.Trim(41560, 41671)+stab5.std.Trim(41672, 41846)+insaneaa.std.Trim(41847, 42123)+stab.std.Trim(42124, 42305)+insaneaa.std.Trim(42306, 42583)+episode.std.Trim(42584, 42691)+insaneaa.std.Trim(42692, 42973)+episode.std.Trim(42974, 43108)+insaneaa.std.Trim(43109, 43704)+stab.std.Trim(43705, 44144)+insaneaa.std.Trim(44145, 45991)+stab.std.Trim(45992, 46165)+insaneaa.std.Trim(46166, 57805)+stab.std.Trim(57806, 57901)+insaneaa.std.Trim(57902, 58129)+stab2.std.Trim(58130, 58369)+insaneaa.std.Trim(58370, 59729)+stab.std.Trim(59730, 59851)+insaneaa.std.Trim(59852, 60997)+stab.std.Trim(60998, 61201)+insaneaa.std.Trim(61202, 61857)+stab.std.Trim(61858, 62315)+insaneaa.std.Trim(62316, 63722)+stab.std.Trim(63723, 63928)+insaneaa.std.Trim(63929, 70164)+stab.std.Trim(70165, 70256)+insaneaa.std.Trim(70257, 74970)+stab.std.Trim(74971, 75072)+insaneaa.std.Trim(75073, 81424)+stab.std.Trim(81425, 81559)+insaneaa.std.Trim(81560, 93574)+stab.std.Trim(93575, 93756)+insaneaa.std.Trim(93757, 98969)+stab.std.Trim(98970, 99351)+insaneaa.std.Trim(99352, 109533)+stab2.std.Trim(109534, 109615)+insaneaa.std.Trim(109616, 109765)+stab.std.Trim(109766, 110165)+insaneaa.std.Trim(110166, 110733)+stab.std.Trim(110734, 110949)+insaneaa.std.Trim(110950, 111525)+insaneaa5.std.Trim(111526, 111617)+insaneaa.std.Trim(111618, 111945)+stab5.std.Trim(111946, 112060)+insaneaa.std.Trim(112061, 127289)+insaneaa6.std.Trim(127290, 127422)+insaneaa.std.Trim(127423, 132353)+stab.std.Trim(132354, 133001)+insaneaa.std.Trim(133002, 139232)+stab.std.Trim(139233, 139452)+insaneaa.std.Trim(139453, 153979)+insaneaa7.std.Trim(153980, 154219)+insaneaa.std.Trim(154220, 154311)+insaneaa7.std.Trim(154312, 154395)+insaneaa.std.Trim(154396, 155645)+insaneaa2.std.Trim(155646, 155705)+insaneaa.std.Trim(155706, 160685)+stab.std.Trim(160686, 160757)+insaneaa.std.Trim(160758, 163460)+episode.std.Trim(163461, 171777)+insaneaa.std.Trim(171778, 172971)+episode.std.Trim(172972, 173476)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[600 645]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\02.png'), "[9763 9849]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\03.png'), "[11417 11529]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\04.png'), "[13408 13527]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\05.png'), "[15594 15735]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\06.png'), "[18494 18644]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa , r'.\mask\18.png'), "[21835 21894]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa , r'.\mask\19.png'), "[24802 24879]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa , r'.\mask\19.png'), "[25114 25229]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\07.png'), "[28592 28710]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa , r'.\mask\20.png'), "[30304 30349]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa , r'.\mask\21.png'), "[34957 35040]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10.png'), "[39021 39160]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11.png'), "[39232 39379]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\12.png'), "[39750 39883]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\13.png'), "[39983 40118]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\14.png'), "[41268 41438]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\15.png'), "[41496 41650]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\16.png'), "[41705 41838]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\17.png'), "[41999 42114]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[42145 42273]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\088.png'), "[42330 42454]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\09.png'), "[42490 42583]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa , r'.\mask\22.png'), "[155646 155705]") 

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
mrgc3 = episode3.std.Trim(0, 54531)+episode5.std.Trim(54532, 54795)+episode3.std.Trim(54796, 126108)+episode4.std.Trim(126109, 126276)+episode3.std.Trim(126277, 127422)+episode4.std.Trim(127423, 127518)+episode3.std.Trim(127519, 173476)
mrgc3.set_output()














