from vapoursynth import core, VideoNode, GRAY, YUV
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

def Grancrest_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6) 
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv  

core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'NCOP4.dgi')
insaneaa = Grancrest_aa(episode)
episode8 = core.dgdecodenv.DGSource(r'23.dgi').std.Trim(4897, 5027)
episode9 = Grancrest_aa(episode8)
insaneaa = Grancrest_aa(episode)
insaneaa2 = havsfunc.QTGMC(episode, InputType=1, SourceMatch=3)

mrgc = episode.std.Trim(0, 248)+insaneaa2.std.Trim(249, 316)+episode.std.Trim(317, 735)+insaneaa.std.Trim(736, 879)+episode9+insaneaa.std.Trim(1011, 2195)




clip16 = core.fmtc.bitdepth(mrgc, bits=16)
clip_y = mvf.GetPlane(clip16, 0)
pf = core.dfttest.DFTTest(clip_y, sigma=7, tbsize=3, opt=3)
den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=48, thsadc=48, bits=16, blksize=8, overlap=4, pf=pf)
filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(filtered, smode=6, thr_det=2, grainy=36, grainc=26,tv_range=True, planes=[0])
harddb = core.f3kdb.Deband(filtered, range=31, y=48, cb=48, cr=48, grainy=60, grainc=40, output_depth=16, keep_tv_range=True)
harddb2 = core.f3kdb.Deband(filtered, range=31, y=70, cb=70, cr=70, grainy=70, grainc=50, output_depth=16, keep_tv_range=True)
Mask = kg.retinex_edgemask(clip16, sigma=0.1, draft=False)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(harddb, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered4 = core.std.MaskedMerge(harddb2, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.24))
episode3 = core.fmtc.bitdepth(mrgc, bits=8)
episode4 = core.fmtc.bitdepth(filtered3, bits=8)
episode5 = core.fmtc.bitdepth(filtered4, bits=8)
mrgc2 = episode3.std.Trim(0, 315)+episode4.std.Trim(316, 735)+episode3.std.Trim(736, 1752)+episode5.std.Trim(1753, 1783)+episode3.std.Trim(1784, 2195)
mrgc2.set_output()





