from vapoursynth import core, VideoNode, GRAY, YUV, GRAYS
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


def oreigaru2_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.35, kernel='lanczos', descale_height=981) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.75, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv
    
def oreigaru2_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.35, kernel='lanczos', descale_height=981) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.75, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30, useCL=True)
    return mixyuv   
 
core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'NCOP_OA.dgi')
insaneaa = oreigaru2_aa(episode)
insaneaa2 = oreigaru2_aa2(episode)
insaneaa3 = havsfunc.QTGMC(episode, InputType=1, SourceMatch=3)
insaneaa4 = oreigaru2_aa2(insaneaa3)
insaneaa5 = havsfunc.QTGMC(insaneaa4, InputType=1, SourceMatch=3)
insaneaa6 = havsfunc.QTGMC(episode, InputType=1, SourceMatch=3)
mrgc = insaneaa.std.Trim(0, 60)+insaneaa5.std.Trim(61, 177)+insaneaa.std.Trim(178, 205)+episode.std.Trim(206, 405)+insaneaa.std.Trim(406, 735)+insaneaa2.std.Trim(736, 868)+insaneaa.std.Trim(869, 1005)+insaneaa2.std.Trim(1006, 1137)+insaneaa.std.Trim(1138, 1732)+insaneaa6.std.Trim(1733, 1864)+insaneaa.std.Trim(1865, 2207)
clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=24, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=31, cb=11, cr=11, grainy=32, grainc=32, output_depth=16, keep_tv_range=True)
db2 = do_chroma_aa(db)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db2, clip16, Mask, planes=[0,1,2], first_plane=True)
filtered2 = core.grain.Add(filtered2, var=0.3, uvar=0.2)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()








