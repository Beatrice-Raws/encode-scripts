from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS, YUV422P16, YUV420P16
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
core.max_cache_size = 120000

def evangelion_dehalo(clip):
    dh_step_one = fd.fine_dehalo(clip, darkstr=0.32, brightstr=0, showmask=0, thlimi=10, thlima=40, thmi=10, thma=40, rx=2.0, ry=2.0, useMtEdge=True, lowsens=10, highsens=20, ss=1, edgeproc=1)
    warp = core.warp.AWarpSharp2(dh_step_one, type=1, depth=[6, 4, 4], thresh=64, cplace="mpeg2")
    dh_step_two = fd.fine_dehalo(warp, darkstr=0.62, brightstr=0.72, showmask=0, thlimi=10, thlima=40, thmi=10, thma=40, rx=2.2, ry=2.2, useMtEdge=True, lowsens=10, highsens=90, ss=1, edgeproc=1)
    return  dh_step_two

def evangelion_Sigmoid_scaled(clip):
    src = core.resize.Bicubic(clip, format=YUV422P16, transfer_in_s="709", transfer_s="709", matrix_in_s="709")
    sigmoidized = hf.SigmoidInverse(src, thr=0.5, cont=5.5) 
    scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 816, filter_param_a=4)
    de_sigmoidized = hf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=5.5)
    scaled_gamma = core.resize.Bicubic(de_sigmoidized, format=YUV422P16, transfer_s="709", transfer_in_s="709", matrix_s="709")
    return  scaled_gamma

def evangelion_denoise_deband(clip):
    clip16 = clip 
    return_to_yuv_420 = core.fmtc.resample(clip16, css="420")
    clip_y = mvf.GetPlane(return_to_yuv_420, 0)
    pf = core.dfttest.DFTTest(clip_y, sigma=1, tbsize=3, opt=3)
    pf2 = core.dfttest.DFTTest(return_to_yuv_420, sigma=1, tbsize=3, opt=3, planes=[1,2])
    den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=8, thsadc=0, bits=16, blksize=8, overlap=4, pf=pf)
    filtered = core.std.ShufflePlanes([den_y, return_to_yuv_420, return_to_yuv_420], [0,1,2], colorfamily=return_to_yuv_420.format.color_family)
    filtered = cooldegrain.CoolDegrain(filtered, tr=1, thsad=0, thsadc=6, bits=16, blksize=8, overlap=4, pf=pf2)
    db = core.placebo.Deband(filtered, planes = 1, threshold = 0.6, grain = 4, radius = 10, dither = False)
    Mask = atf.retinex_edgemask(return_to_yuv_420, sigma=0.1, draft=False, opencl=True)
    Mask2 = core.std.Binarize(Mask,9828,0)
    filtered2 = core.std.MaskedMerge(db, return_to_yuv_420, Mask2, planes=[0,1,2], first_plane=True)
    denoise_deband = core.fmtc.bitdepth(filtered2, bits=10)
    return  denoise_deband

episode = core.lsmas.LWLibavSource(r"F:\eva709\eva4.mxf")
episode = core.std.Crop(episode, top=264, bottom=264)
episode_s = evangelion_Sigmoid_scaled(episode)
episode_dh = evangelion_dehalo(episode_s)
episode_db = evangelion_denoise_deband(episode_dh)
episode_db_not_dh = evangelion_denoise_deband(episode_s)
mrgc = episode_db_not_dh.std.Trim(0, 92)+episode_db.std.Trim(93, 104)+episode_db_not_dh.std.Trim(105, 137)+episode_db.std.Trim(138, 1750)+episode_db_not_dh.std.Trim(1751, 1784)+episode_db.std.Trim(1785, 3346)+episode_db_not_dh.std.Trim(3347, 3383)+episode_db.std.Trim(3384, 5523)+episode_db_not_dh.std.Trim(5524, 6005)+episode_db.std.Trim(6006, 20607)+episode_db_not_dh.std.Trim(20608, 20747)+episode_db.std.Trim(20748, 92007)+episode_db_not_dh.std.Trim(92008, 92075)+episode_db.std.Trim(92076, 208646)+episode_db_not_dh.std.Trim(208647, 222743)
mrgc.set_output()














