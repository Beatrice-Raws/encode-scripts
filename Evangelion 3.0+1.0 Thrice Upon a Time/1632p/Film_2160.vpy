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
    dh_step_one = fd.fine_dehalo(clip, darkstr=0.38, brightstr=0, showmask=0, thlimi=10, thlima=40, thmi=10, thma=40, rx=3.0, ry=3.0, useMtEdge=True, lowsens=10, highsens=20, ss=1, edgeproc=1)
    #warp = core.warp.AWarpSharp2(dh_step_one, type=1, depth=[6, 4, 4], thresh=64, cplace="mpeg2")
    mask = core.warp.ASobel(dh_step_one)
    mask = core.warp.ABlur(mask)
    alignment = core.fmtc.resample(dh_step_one, w=dh_step_one.width * 4, h=dh_step_one.height * 4, sx=0.375, sy=0.375)
    mixyuv1 = core.warp.AWarp(alignment, mask, cplace="mpeg2")
    #warp = core.warp.AWarpSharp2(dh_step_one, cplace="mpeg2", thresh=14)
    dh_step_two = fd.fine_dehalo(mixyuv1, darkstr=0.58, brightstr=0.70, showmask=0, thlimi=10, thlima=40, thmi=10, thma=40, rx=3.0, ry=3.0, useMtEdge=True, lowsens=10, highsens=20, ss=1, edgeproc=1)
    return  dh_step_two

def evangelion_denoise_deband(clip):
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    clip_y = mvf.GetPlane(clip16, 0)
    pf = core.dfttest.DFTTest(clip_y, sigma=1, tbsize=3, opt=3)
    pf2 = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[1,2])
    den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=8, thsadc=0, bits=16, blksize=8, overlap=4, pf=pf)
    filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
    filtered = cooldegrain.CoolDegrain(filtered, tr=1, thsad=0, thsadc=6, bits=16, blksize=8, overlap=4, pf=pf2)
    db = core.placebo.Deband(filtered, planes = 1, threshold = 0.6, grain = 4, radius = 10, dither = False)
    Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
    Mask2 = core.std.Binarize(Mask,9828,0)
    filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
    denoise_deband = core.fmtc.bitdepth(filtered2, bits=10)
    return  denoise_deband

episode = core.dgdecodenv.DGSource(r'00006.dgi')
episode = core.std.Crop(episode, top=264, bottom=264)
episode_dh = evangelion_dehalo(episode)
episode_db = evangelion_denoise_deband(episode_dh)
episode_db_not_dh = evangelion_denoise_deband(episode)
#mrgc = episode_db.std.Trim(51726, 52059)+episode_db.std.Trim(793, 845)+episode_db.std.Trim(17025, 17069)+episode_db.std.Trim(22957, 23235)+episode_db.std.Trim(32844, 32979)+episode_db.std.Trim(98127, 98691)+episode_db.std.Trim(111565, 111681)
mrgc = episode_db_not_dh.std.Trim(0, 92)+episode_db.std.Trim(93, 104)+episode_db_not_dh.std.Trim(105, 137)+episode_db.std.Trim(138, 1750)+episode_db_not_dh.std.Trim(1751, 1784)+episode_db.std.Trim(1785, 3346)+episode_db_not_dh.std.Trim(3347, 3383)+episode_db.std.Trim(3384, 5523)+episode_db_not_dh.std.Trim(5524, 6005)+episode_db.std.Trim(6006, 20607)+episode_db_not_dh.std.Trim(20608, 20747)+episode_db.std.Trim(20748, 92007)+episode_db_not_dh.std.Trim(92008, 92075)+episode_db.std.Trim(92076, 208646)+episode_db_not_dh.std.Trim(208647, 222743)
mrgc.set_output()














