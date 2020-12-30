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

def DiffRescaleMask(clip: VideoNode, descale_h: int = 720, descale_w: int = None, kernel: str = 'bilinear', mthr: int = 50) -> VideoNode:
    ''' Builds mask from difference of original and re-upscales clips '''
    funcName = 'DiffRescaleMask'
    if not isinstance(clip, VideoNode):
        raise TypeError(funcName + ': \"clip\" must be a clip!')
    descale_w = havsfunc.m4((clip.width * descale_h) / clip.height) if descale_w == None else descale_w
    dclip = dsc.Descale(clip, descale_w, descale_h, kernel=kernel)
    uclip = core.fmtc.resample(dclip, clip.width, clip.height, kernel=kernel).fmtc.bitdepth(bits=8)
    uclip = core.std.ShufflePlanes(uclip, 0, GRAY)
    clip = core.std.ShufflePlanes(clip, 0, GRAY)
    diff = core.std.MakeDiff(clip, uclip)
    mask = diff.rgvs.RemoveGrain(2).rgvs.RemoveGrain(2).hist.Luma()
    mask = mask.std.Expr('x {thr} < 0 x ?'.format(thr=mthr))
    mask = mask.std.Prewitt().std.Maximum().std.Maximum().std.Deflate()
    return mask


def evangelion_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.0, ry=2.0, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)    
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv  

def evangelion_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33)
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.0, ry=2.0, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)    
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30, useCL=True, sangnomPP=True, LumaOnly=False)
    return mixyuv    
    
def evangelion_aa3(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33)
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.0, ry=2.0, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)    
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=40, useCL=True, sangnomPP=True)
    return mixyuv      


core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'00148.dgi')
insaneaa = evangelion_aa(episode)
insaneaa2 = evangelion_aa2(episode)
insaneaa3 = evangelion_aa3(episode)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa3, InputType=1, SourceMatch=3)

mrgc = episode.std.Trim(0, 979)+insaneaa.std.Trim(980, 13048)+stab.std.Trim(13049, 13295)+insaneaa.std.Trim(13296, 24104)+stab.std.Trim(24105, 24216)+insaneaa.std.Trim(24217, 33767)+insaneaa2.std.Trim(33768, 33965)+insaneaa.std.Trim(33966, 34583)+stab.std.Trim(34584, 35118)+insaneaa.std.Trim(35119, 50037)+insaneaa3.std.Trim(50038, 50265)+stab2.std.Trim(50266, 50343)+insaneaa.std.Trim(50344, 50607)+stab2.std.Trim(50608, 50694)+insaneaa.std.Trim(50695, 53820)+stab2.std.Trim(53821, 54147)+insaneaa.std.Trim(54148, 55444)+stab.std.Trim(55445, 55616)+insaneaa.std.Trim(55617, 55698)+stab.std.Trim(55699, 55757)+insaneaa.std.Trim(55758, 60068)+stab.std.Trim(60069, 60127)+insaneaa.std.Trim(60128, 75163)+episode.std.Trim(75164, 75259)+insaneaa.std.Trim(75260, 85005)+stab.std.Trim(85006, 85263)+insaneaa.std.Trim(85264, 91560)+stab.std.Trim(91561, 91635)+insaneaa.std.Trim(91636, 120846)+stab.std.Trim(120847, 120992)+insaneaa.std.Trim(120993, 137157)+episode.std.Trim(137158, 144451)+insaneaa.std.Trim(144452, 144494)+episode.std.Trim(144495, 144499)+insaneaa.std.Trim(144500, 144547)+episode.std.Trim(144548, 144551)+insaneaa.std.Trim(144552, 144594)+episode.std.Trim(144595, 144598)+insaneaa.std.Trim(144599, 144659)+episode.std.Trim(144660, 144664)+insaneaa.std.Trim(144665, 144749)+episode.std.Trim(144750, 144754)+insaneaa.std.Trim(144755, 144767)+episode.std.Trim(144768, 144771)+insaneaa.std.Trim(144772, 144962)+episode.std.Trim(144963, 145259)

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
pf2 = core.dfttest.DFTTest(clip16, sigma=7, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=22, thsadc=21, bits=16, blksize=8, overlap=4, pf=pf)
den2 = cooldegrain.CoolDegrain(clip16, tr=1, thsad=28, thsadc=24, bits=16, blksize=8, overlap=4, pf=pf2)
db = core.f3kdb.Deband(den, range=21, y=10, cb=11, cr=11, grainy=18, grainc=18, output_depth=16, keep_tv_range=True)
db2 = core.f3kdb.Deband(den2, range=31, y=31, cb=42, cr=42, grainy=200, grainc=200, output_depth=16, keep_tv_range=True)
db3 = core.f3kdb.Deband(den, range=31, y=42, cb=14, cr=14, grainy=74, grainc=74, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(db2, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered4 = core.std.MaskedMerge(db3, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
episode5 = core.fmtc.bitdepth(filtered4, bits=10)
mrgc2 = episode3.std.Trim(0, 31895)+episode4.std.Trim(31896, 31949)+episode3.std.Trim(31950, 70141)+episode5.std.Trim(70142, 70228)+episode3.std.Trim(70229, 74571)+episode5.std.Trim(74572, 74600)+episode3.std.Trim(74601, 145259)
mrgc2.set_output()














