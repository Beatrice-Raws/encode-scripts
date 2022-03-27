from vapoursynth import core, VideoNode, GRAY8, YUV, GRAY
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
    
def lumaAA(clip, pscrn=1):
    ux = clip.width * 2
    uy = clip.height * 2
    luma = core.std.ShufflePlanes(clip, 0, GRAY)
    upscale = core.nnedi3cl.NNEDI3CL(luma, field=1, dh=True, dw=True, nsize=6, nns=4, pscrn=pscrn, device=-1)
    upscale = fd.fine_dehalo(upscale, darkstr=0, brightstr=0.75, showmask=0, rx=2, ry=2, useMtEdge=True, thmi=20, thma=100, thlimi=20, thlima=100)
    downscale = core.resize.Spline36(upscale, clip.width, clip.height, src_left=-0.5, src_top=-0.5, src_width=ux, src_height=uy, filter_param_a=0.33, filter_param_b=0.33)
    downscale = core.std.ShufflePlanes([downscale,clip, clip], [0,1,2], YUV) 
    mixyuv = core.warp.AWarpSharp2(downscale, type=1, depth=[4, 4, 4], thresh=64, cplace="mpeg2")
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=0.75, showmask=0, thmi=20, thma=100, thlimi=20, thlima=100, rx=2.4, ry=2.4, useMtEdge=True)
    return  mixyuv 

core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'01.dgi')
insaneaa = lumaAA(episode)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)

mrgc = episode.std.Trim(0, 455)+insaneaa.std.Trim(456, 21216)+stab.std.Trim(21217, 21318)+insaneaa.std.Trim(21319, 22193)+stab.std.Trim(22194, 22323)+insaneaa.std.Trim(22324, 25312)+stab.std.Trim(25313, 25376)+insaneaa.std.Trim(25377, 29392)+stab.std.Trim(29393, 29541)+insaneaa.std.Trim(29542, 34649)+stab.std.Trim(34650, 34749)+insaneaa.std.Trim(34750, 48240)+stab.std.Trim(48241, 48413)+insaneaa.std.Trim(48414, 53663)+episode.std.Trim(53664, 57385)
  
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[1510 1590]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\02.png'), "[1628 1677]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\03.png'), "[1678 1707]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\04.png'), "[1708 1741]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\05.png'), "[1749 1811]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\06.png'), "[1812 1835]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11.png'), "[15128 15201]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\12.png'), "[15202 15240]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\13.png'), "[15241 15250]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\14.png'), "[15251 15315]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\07.png'), "[15938 16003]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[16004 16029]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\09.png'), "[16030 16073]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10.png'), "[16074 16119]")

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=22, thsadc=20, bits=16, blksize=8, overlap=4, pf=pf)
db = core.placebo.Deband(den, planes = 1, threshold = 0.9, grain = 4, radius = 10)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()
