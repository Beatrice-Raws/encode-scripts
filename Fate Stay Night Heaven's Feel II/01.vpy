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
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa2, InputType=1, SourceMatch=3)
stab3 = havsfunc.QTGMC(insaneaa3, InputType=1, SourceMatch=3)
stab4 = havsfunc.QTGMC(insaneaa4, InputType=1, SourceMatch=3)
stab5 = havsfunc.QTGMC(insaneaa5, InputType=1, SourceMatch=3)

mrgc = episode.std.Trim(0, 527)+insaneaa.std.Trim(528, 1504)+insaneaa5.std.Trim(1505, 1576)+insaneaa.std.Trim(1577, 2743)+insaneaa7.std.Trim(2744, 2811)+insaneaa.std.Trim(2812, 4761)+stab.std.Trim(4762, 4965)+insaneaa.std.Trim(4966, 5638)+stab.std.Trim(5639, 5958)+insaneaa.std.Trim(5959, 6656)+episode.std.Trim(6657, 6846)+stab.std.Trim(6847, 6994)+insaneaa.std.Trim(6995, 8102)+stab.std.Trim(8103, 8234)+insaneaa.std.Trim(8235, 12325)+stab.std.Trim(12326, 12469)+insaneaa.std.Trim(12470, 13195)+stab.std.Trim(13196, 13279)+insaneaa.std.Trim(13280, 15467)+stab.std.Trim(15468, 15755)+insaneaa.std.Trim(15756, 16988)+stab.std.Trim(16989, 17070)+insaneaa.std.Trim(17071, 20773)+stab.std.Trim(20774, 20929)+insaneaa.std.Trim(20930, 25415)+stab.std.Trim(25416, 25697)+insaneaa.std.Trim(25698, 26385)+stab.std.Trim(26386, 26625)+insaneaa.std.Trim(26626, 26681)+stab.std.Trim(26682, 26759)+insaneaa.std.Trim(26760, 26910)+stab.std.Trim(26911, 27207)+insaneaa.std.Trim(27208, 27515)+insaneaa5.std.Trim(27516, 27959)+insaneaa.std.Trim(27960, 29282)+insaneaa5.std.Trim(29283, 29450)+insaneaa.std.Trim(29451, 31492)+insaneaa6.std.Trim(31493, 31540)+insaneaa.std.Trim(31541, 35047)+insaneaa2.std.Trim(35048, 35305)+insaneaa.std.Trim(35306, 36304)+stab.std.Trim(36305, 36720)+insaneaa.std.Trim(36721, 38586)+stab.std.Trim(38587, 38898)+insaneaa.std.Trim(38899, 50603)+stab.std.Trim(50604, 51333)+insaneaa.std.Trim(51334, 51858)+stab.std.Trim(51859, 52116)+insaneaa.std.Trim(52117, 72095)+insaneaa6.std.Trim(72096, 72235)+insaneaa.std.Trim(72236, 74846)+insaneaa7.std.Trim(74847, 74924)+insaneaa.std.Trim(74925, 77851)+insaneaa8.std.Trim(77852, 77971)+insaneaa.std.Trim(77972, 78285)+insaneaa8.std.Trim(78286, 78421)+insaneaa.std.Trim(78422, 78555)+insaneaa4.std.Trim(78556, 78663)+insaneaa7.std.Trim(78664, 78711)+insaneaa.std.Trim(78712, 85977)+insaneaa7.std.Trim(85978, 86097)+insaneaa.std.Trim(86098, 89968)+insaneaa7.std.Trim(89969, 90051)+insaneaa.std.Trim(90052, 90363)+insaneaa7.std.Trim(90364, 90393)+insaneaa.std.Trim(90394, 90573)+insaneaa7.std.Trim(90574, 90799)+insaneaa.std.Trim(90800, 91331)+insaneaa7.std.Trim(91332, 91499)+insaneaa.std.Trim(91500, 100262)+insaneaa6.std.Trim(100263, 100306)+insaneaa.std.Trim(100307, 100734)+stab.std.Trim(100735, 100878)+insaneaa.std.Trim(100879, 112555)+stab.std.Trim(112556, 112775)+insaneaa.std.Trim(112776, 116078)+insaneaa5.std.Trim(116079, 116128)+insaneaa.std.Trim(116129, 118166)+stab.std.Trim(118167, 118292)+insaneaa.std.Trim(118293, 119965)+stab.std.Trim(119966, 120085)+insaneaa.std.Trim(120086, 125928)+stab.std.Trim(125929, 126356)+insaneaa6.std.Trim(126357, 126390)+insaneaa7.std.Trim(126391, 126422)+insaneaa.std.Trim(126423, 126802)+insaneaa6.std.Trim(126803, 126998)+insaneaa7.std.Trim(126999, 127118)+insaneaa6.std.Trim(127119, 127262)+insaneaa.std.Trim(127263, 134008)+stab.std.Trim(134009, 134278)+insaneaa.std.Trim(134279, 136775)+stab.std.Trim(136776, 136865)+insaneaa.std.Trim(136866, 140805)+insaneaa7.std.Trim(140806, 140949)+insaneaa.std.Trim(140950, 142727)+stab.std.Trim(142728, 143005)+insaneaa.std.Trim(143006, 147197)+stab.std.Trim(147198, 147335)+insaneaa.std.Trim(147336, 150736)+stab.std.Trim(150737, 151096)+insaneaa.std.Trim(151097, 152686)+insaneaa5.std.Trim(152687, 152774)+stab.std.Trim(152775, 152854)+insaneaa.std.Trim(152855, 156450)+insaneaa7.std.Trim(156451, 156702)+insaneaa.std.Trim(156703, 157197)+insaneaa6.std.Trim(157198, 157353)+insaneaa.std.Trim(157354, 159377)+insaneaa7.std.Trim(159378, 159517)+insaneaa.std.Trim(159518, 160057)+episode.std.Trim(160058, 166712)+insaneaa7.std.Trim(166713, 166890)+insaneaa.std.Trim(166891, 167628)+episode.std.Trim(167629, 167715)+insaneaa.std.Trim(167716, 168144)+episode.std.Trim(168145, 168503)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[6873 6988]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\02.png'), "[7014 7122]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\03.png'), "[7152 7266]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\04.png'), "[7298 7403]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\05.png'), "[7431 7533]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\06.png'), "[7560 7653]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\07.png'), "[7680 7792]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[7818 7906]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\09.png'), "[7933 8011]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10.png'), "[8034 8101]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11.png'), "[8122 8227]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\12.png'), "[8251 8349]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\13.png'), "[8372 8501]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\18.png'), "[35048 35305]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\17.png'), "[166713 166800]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\14.png'), "[167471 167628]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\15.png'), "[167793 167971]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\16.png'), "[167999 168144]")

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
mrgc3 = episode3.std.Trim(0, 100142)+episode4.std.Trim(100143, 100306)+episode3.std.Trim(100307, 168503)
mrgc3.set_output()














