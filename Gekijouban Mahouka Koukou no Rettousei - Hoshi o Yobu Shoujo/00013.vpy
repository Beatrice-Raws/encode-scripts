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
def Mahouka_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bilinear', descale_height=810) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    hardaa = hiaa.HardAA(graydh, mask='simple', mthr=60, alpha=0.4, beta=0.25, gamma=20.0, nrad=3, mdis=40, useCL=True, sangnomPP=False)
    rescale1 = insaneAA.rescale(hardaa, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)
    rescale2 = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)
    rescale = core.std.Expr([rescale2, rescale1], 'x 0.60 * y 0.40 * +')   
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv 
 
core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'00013.dgi')
matched_clip = core.vivtc.VFM(episode, 1)
insaneaa = Mahouka_aa(matched_clip)
degalo = havsfunc.DeHalo_alpha(insaneaa, rx=2, ry=2, darkstr=0, brightstr=0.8, lowsens=80, highsens=80, ss=1)

mrgc = insaneaa.std.Trim(0, 199) + degalo.std.Trim(200, 385) + insaneaa.std.Trim(386, 494) + degalo.std.Trim(495, 569) + insaneaa.std.Trim(570, 823) + degalo.std.Trim(824, 869) + episode.std.Trim(870, 959)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\sp1.png'), "[30 96]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\sp1-1.png'), "[200 385] [495 569] [824 869]")


clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=26, thsadc=24, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=24, y=16, cb=8, cr=8, grainy=16, grainc=16, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()







