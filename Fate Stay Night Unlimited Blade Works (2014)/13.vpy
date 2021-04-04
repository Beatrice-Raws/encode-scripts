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
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=70, useCL=True)
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

def fate_stay_night_aa5(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bilinear', descale_height=853) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=60, useCL=True)
    return mixyuv
 
core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'13.dgi')
mask_clip = core.raws.Source(r'12.yuv').std.Trim(36, 138).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Prewitt().std.Maximum().std.Maximum().std.Deflate()
op_titles = core.std.Trim(episode, 2446, 4602)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(24, 2180)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(24, 2180)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 65692, 68451)
nced = core.dgdecodenv.DGSource(r'NCED_EP12.dgi').std.Trim(3164, 5923)
nced_aa = core.raws.Source(r'NCED_EP12.y4m').std.Trim(3164, 5923)
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
mask_final = core.std.MaskedMerge(insaneaa.std.Trim(4699, 4819), episode.std.Trim(4699, 4819), mask_clip, planes=[0], first_plane=True)

mrgc = insaneaa.std.Trim(0, 2445)+op+insaneaa.std.Trim(4603, 4698)+mask_final+insaneaa.std.Trim(4820, 5587)+stab.std.Trim(5588, 5693)+insaneaa.std.Trim(5694, 10190)+stab.std.Trim(10191, 10472)+insaneaa.std.Trim(10473, 15694)+stab.std.Trim(15695, 16246)+insaneaa.std.Trim(16247, 20820)+stab2.std.Trim(20821, 20888)+insaneaa.std.Trim(20889, 22694)+stab.std.Trim(22695, 23129)+insaneaa.std.Trim(23130, 27668)+stab.std.Trim(27669, 28025)+insaneaa.std.Trim(28026, 29498)+stab2.std.Trim(29499, 29582)+insaneaa3.std.Trim(29583, 29644)+insaneaa.std.Trim(29645, 30015)+stab.std.Trim(30016, 30297)+insaneaa.std.Trim(30298, 34929)+insaneaa2.std.Trim(34930, 34970)+insaneaa.std.Trim(34971, 35378)+stab.std.Trim(35379, 35510)+insaneaa.std.Trim(35511, 39972)+stab.std.Trim(39973, 40254)+insaneaa.std.Trim(40255, 43104)+stab.std.Trim(43105, 43323)+insaneaa.std.Trim(43324, 50325)+stab.std.Trim(50326, 50670)+insaneaa.std.Trim(50671, 50987)+stab.std.Trim(50988, 51182)+insaneaa.std.Trim(51183, 53248)+stab.std.Trim(53249, 53392)+insaneaa.std.Trim(53393, 54224)+stab.std.Trim(54225, 54438)+insaneaa.std.Trim(54439, 54696)+stab2.std.Trim(54697, 54910)+insaneaa.std.Trim(54911, 54962)+stab3.std.Trim(54963, 55062)+insaneaa.std.Trim(55063, 57759)+insaneaa2.std.Trim(57760, 57815)+insaneaa.std.Trim(57816, 60288)+stab.std.Trim(60289, 60370)+insaneaa.std.Trim(60371, 63111)+stab.std.Trim(63112, 63171)+insaneaa.std.Trim(63172, 64592)+stab.std.Trim(64593, 64688)+insaneaa.std.Trim(64689, 65462)+stab2.std.Trim(65463, 65691)+ed+insaneaa.std.Trim(68452, 69096)+episode.std.Trim(69097, 69195)
 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\25.png'), "[5994 6068]") 

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=14, thsadc=12, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=12, cb=10, cr=10, grainy=12, grainc=12, output_depth=16, keep_tv_range=True)
db2 = core.f3kdb.Deband(den, range=31, y=38, cb=10, cr=10, grainy=28, grainc=28, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(db2, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
mrgc3 = episode3.std.Trim(0, 39602)+episode4.std.Trim(39603, 39794)+episode3.std.Trim(39795, 48468)+episode4.std.Trim(48469, 48985)+episode3.std.Trim(48986, 58365)+episode4.std.Trim(58366, 58412)+episode3.std.Trim(58413, 69195)
mrgc3.set_output()









