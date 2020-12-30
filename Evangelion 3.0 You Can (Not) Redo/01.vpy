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
episode = core.dgdecodenv.DGSource(r'55555555555555.dgi')
insaneaa = evangelion_aa(episode)
insaneaa2 = evangelion_aa2(episode)
insaneaa3 = evangelion_aa3(episode)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa3, InputType=1, SourceMatch=3)

mrgc = episode.std.Trim(0, 1102)+insaneaa.std.Trim(1103, 30485)+stab.std.Trim(30486, 30828)+insaneaa.std.Trim(30829, 31114)+stab2.std.Trim(31115, 31243)+insaneaa.std.Trim(31244, 31327)+stab.std.Trim(31328, 31439)+insaneaa.std.Trim(31440, 32456)+stab2.std.Trim(32457, 32684)+insaneaa.std.Trim(32685, 34404)+stab.std.Trim(34405, 34602)+insaneaa.std.Trim(34603, 34992)+stab2.std.Trim(34993, 35578)+insaneaa.std.Trim(35579, 35753)+stab.std.Trim(35754, 35907)+insaneaa.std.Trim(35908, 47430)+episode.std.Trim(47431, 47538)+insaneaa.std.Trim(47539, 48762)+stab.std.Trim(48763, 48984)+insaneaa.std.Trim(48985, 53216)+stab.std.Trim(53217, 53336)+insaneaa.std.Trim(53337, 53432)+stab.std.Trim(53433, 53696)+insaneaa.std.Trim(53697, 76438)+episode.std.Trim(76439, 76606)+insaneaa.std.Trim(76607, 126126)+stab2.std.Trim(126127, 126385)+insaneaa.std.Trim(126386, 126910)+stab2.std.Trim(126911, 127357)+insaneaa.std.Trim(127358, 130786)+episode.std.Trim(130787, 137022)+insaneaa.std.Trim(137023, 137560)+episode.std.Trim(137561, 137880)
mrgc = core.std.Crop(mrgc, top=132, bottom=132) 

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
mrgc2 = episode3.std.Trim(0, 26592)+episode5.std.Trim(26593, 26656)+episode3.std.Trim(26657, 79318)+episode5.std.Trim(79319, 79509)+episode3.std.Trim(79510, 79940)+episode5.std.Trim(79941, 80164)+episode3.std.Trim(80165, 81188)+episode5.std.Trim(81189, 81648)+episode3.std.Trim(81649, 99029)+episode5.std.Trim(99030, 99074)+episode3.std.Trim(99075, 103009)+episode5.std.Trim(103010, 103061)+episode3.std.Trim(103062, 104582)+episode5.std.Trim(104583, 104825)+episode3.std.Trim(104826, 107393)+episode5.std.Trim(107394, 107535)+episode3.std.Trim(107536, 107703)+episode5.std.Trim(107704, 107935)+episode3.std.Trim(107936, 107958)+episode5.std.Trim(107959, 108114)+episode3.std.Trim(108115, 112227)+episode5.std.Trim(112228, 112330)+episode3.std.Trim(112331, 137880)
mrgc3 = mrgc2.std.Trim(126, 137880)
mrgc3.set_output()


 


 
 
















