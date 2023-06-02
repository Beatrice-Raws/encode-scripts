from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS, YUV420P16, YUV444P16
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc as hf
import mvsfunc as mvf
import GradFun3 as gfa
import insaneAA 
import cooldegrain
import finedehalo as fd
import HardAAp2 as hiaa
import descale as dsc
import functools
import math
import psutil
import regress
core.max_cache_size = 120000

def lumaAA(clip):
    luma = core.std.ShufflePlanes(clip, 0, GRAY)
    interpolated = luma.eedi3m.EEDI3(field=1, dh=True, alpha=0.2,beta=0.25,gamma=10.0,nrad=2,mdis=20, hp=True,ucubic=True,cost3=True,vcheck=3,vthresh0=32,vthresh1=64,vthresh2=4, sclip=luma.nnedi3.nnedi3(field=1, dh=True, nsize=6, nns=4, pscrn=1, qual=2), opt=4)
    rotated = rotate_clockwise(interpolated)
    interpolated = rotated.eedi3m.EEDI3(field=1, dh=True, alpha=0.2,beta=0.25,gamma=10.0,nrad=2,mdis=20, hp=True,ucubic=True,cost3=True,vcheck=3,vthresh0=32,vthresh1=64,vthresh2=4, sclip=rotated.nnedi3.nnedi3(field=1, dh=True, nsize=6, nns=4, pscrn=1, qual=2), opt=4)
    upscale = rotate_counterclockwise(interpolated)
    upscale = core.warp.AWarpSharp2(upscale, type=1, depth=[6, 4, 4], thresh=64, cplace="mpeg2")
    upscale = core.std.ShufflePlanes([upscale, clip, clip], [0,1,2], YUV)
    src = core.resize.Bicubic(upscale, format=YUV444P16, transfer_in_s="709", transfer_s="709", matrix_in_s="709")
    sigmoidized = hf.SigmoidInverse(src, thr=0.5, cont=5.5) 
    scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 804, src_left=-0.5, src_top=-0.5, filter_param_a=2)
    de_sigmoidized = hf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=5.5)
    scaled_gamma = core.resize.Lanczos(de_sigmoidized, format=YUV420P16, transfer_s="709", transfer_in_s="709", matrix_s="709")
    return  scaled_gamma

def rotate_clockwise(clip: VideoNode) -> VideoNode:
    return clip.std.Transpose().std.FlipHorizontal()

def rotate_counterclockwise(clip: VideoNode) -> VideoNode:
    return clip.std.Transpose().std.FlipVertical()
 
def mangle_luma(clip: VideoNode) -> VideoNode:
    luma = mvf.GetPlane(clip,0)
    luma_mangled = luma.resize.Point(960,1080, src_left=-1).resize.Point(960,540)
    return luma_mangled    
  
def demangle_plane(clip: VideoNode) -> VideoNode:
    descaled = mvf.GetPlane(clip,0)
    descaled = core.resize.Lanczos(descaled, 960,1080, filter_param_a=4, format=GRAYS)
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
                                        demangle_plane(mvf.GetPlane(clip, 2)),  use_binary=True, radius=3)
    reconstructed = core.fmtc.resample(reconstructed, css='444')                                    
    return core.std.ShufflePlanes([clip, reconstructed],[0,1,2], YUV)

def do_chroma_aa_not_luma_aa(clip: VideoNode) -> VideoNode:
    luma_descaled = mvf.GetPlane(clip,0)
    luma_mangled = mangle_luma(luma_descaled)
    reconstructed = regress.Reconstruct(luma_descaled.resize.Bicubic(format=GRAYS),
                                        demangle_plane(luma_mangled),
                                        demangle_plane(mvf.GetPlane(clip, 1)),
                                        demangle_plane(mvf.GetPlane(clip, 2)),  use_binary=True, radius=3)
    reconstructed = core.fmtc.resample(reconstructed, css='420')                                    
    return core.std.ShufflePlanes([clip, reconstructed],[0,1,2], YUV)

def Natsu_Eno_Tunnel_Sayonara_No_Deguchi_denoise_deband(clip):
    clip16 = clip 
    clip_y = mvf.GetPlane(clip16, 0)
    pf = core.dfttest.DFTTest(clip_y, sigma=1, tbsize=3, opt=3)
    pf2 = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[1,2])
    den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=20, thsadc=0, bits=16, blksize=8, overlap=4, pf=pf)
    filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
    filtered = cooldegrain.CoolDegrain(filtered, tr=1, thsad=0, thsadc=18, bits=16, blksize=8, overlap=4, pf=pf2)
    db = core.placebo.Deband(filtered, planes = 1, threshold = 0.8, grain = 8, radius = 10)
    Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
    Mask2 = core.std.Binarize(Mask, 9828,0)
    filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
    denoise_deband = core.fmtc.bitdepth(filtered2, bits=10)
    return  denoise_deband

def Natsu_Eno_Tunnel_Sayonara_No_Deguchi_denoise_deband_scene(clip):
    clip16 = clip 
    clip_y = mvf.GetPlane(clip16, 0)
    pf = core.dfttest.DFTTest(clip_y, sigma=7, tbsize=3, opt=3)
    pf2 = core.dfttest.DFTTest(clip16, sigma=7, tbsize=3, opt=3, planes=[1,2])
    den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=24, thsadc=0, bits=16, blksize=8, overlap=4, pf=pf)
    filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
    filtered = cooldegrain.CoolDegrain(filtered, tr=1, thsad=0, thsadc=24, bits=16, blksize=8, overlap=4, pf=pf2)
    db = core.placebo.Deband(filtered, planes = 1 | 2 | 4, threshold = 4.0, grain = 14, radius = 16)
    Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
    filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
    denoise_deband = core.fmtc.bitdepth(filtered2, bits=10)
    return  denoise_deband

episode = core.dgdecodenv.DGSource(r'00000.dgi')
episode_16 = core.fmtc.bitdepth(episode, bits=16)
episode_basic_filtration = do_chroma_aa(episode_16)
db_not_luma_aa = do_chroma_aa_not_luma_aa(episode_16)
db_not_luma_aa = core.std.Crop(db_not_luma_aa, top=138, bottom=138)
db_not_aa = core.std.Crop(episode_16, top=138, bottom=138)
episode_basic_filtration = core.std.Crop(episode_basic_filtration, top=138, bottom=138)
episode_basic_filtration = lumaAA(episode_basic_filtration)
episode_db = Natsu_Eno_Tunnel_Sayonara_No_Deguchi_denoise_deband(episode_basic_filtration)
episode_db_scene = Natsu_Eno_Tunnel_Sayonara_No_Deguchi_denoise_deband_scene(episode_basic_filtration)
episode_db_not_aa = Natsu_Eno_Tunnel_Sayonara_No_Deguchi_denoise_deband(db_not_luma_aa)
episode_db_not_all_aa = Natsu_Eno_Tunnel_Sayonara_No_Deguchi_denoise_deband(db_not_aa)
mrgc = episode_db_not_all_aa.std.Trim(0, 671)+episode_db.std.Trim(672, 69469)+episode_db_scene.std.Trim(69470, 69517)+episode_db.std.Trim(69518, 112799)+episode_db_not_aa.std.Trim(112800, 112919)+episode_db_not_all_aa.std.Trim(112920, 118919)
mrgc.set_output()














