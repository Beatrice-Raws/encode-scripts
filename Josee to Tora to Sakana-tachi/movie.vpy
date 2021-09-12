from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import GradFun3 as gfa
import insaneAA 
import finesharp
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
    
def lumaAA(clip, pscrn=1, dev=-1):
    ux = clip.width * 4
    uy = clip.height * 4
    luma = core.std.ShufflePlanes(clip, 0, GRAY)
    graydh = fd.fine_dehalo(luma, darkstr=0, brightstr=1, showmask=0, rx=1.5, ry=1.5, useMtEdge=True)
    upscale = core.nnedi3cl.NNEDI3CL(graydh, field=1, dh=True, dw=True, nsize=6, nns=4, pscrn=pscrn, device=dev)
    upscale = fd.fine_dehalo(upscale, darkstr=0, brightstr=1, showmask=0, rx=2, ry=2, useMtEdge=True)
    rotated = rotate_clockwise(upscale)
    interpolated = rotated.eedi3m.EEDI3CL(field=1, dh=True, alpha=0.4,beta=0.25,gamma=20.0,nrad=2,mdis=20, hp=False,ucubic=True,cost3=True,vcheck=2,vthresh0=32,vthresh1=64,vthresh2=4, sclip=rotated.nnedi3.nnedi3(field=1, dh=True, nsize=0, nns=4, pscrn=1, qual=2), device=dev)
    interpolated = rotate_counterclockwise(interpolated)
    interpolated = interpolated.eedi3m.EEDI3CL(field=1, dh=True, alpha=0.4,beta=0.25,gamma=20.0,nrad=2,mdis=20, hp=False,ucubic=True,cost3=True,vcheck=2,vthresh0=32,vthresh1=64,vthresh2=4, sclip=interpolated.nnedi3.nnedi3(field=1, dh=True, nsize=0, nns=4, pscrn=1, qual=2), device=dev)
    graydh2 = fd.fine_dehalo(interpolated, darkstr=0, brightstr=1, showmask=0, rx=2.3, ry=2.3, useMtEdge=True)
    downscale = core.resize.Spline36(graydh2, clip.width, clip.height, src_left=-1.5, src_top=-1.5, src_width=ux, src_height=uy, filter_param_a=0.33, filter_param_b=0.33)
    downscale = core.std.ShufflePlanes([downscale,clip], [0,1,2], YUV) 
    downscale = finesharp.sharpen(downscale, mode=-3, sstr=0.1)
    mixyuv = fd.fine_dehalo(downscale, darkstr=0, brightstr=0.7, showmask=0, rx=2, ry=2, useMtEdge=True)
    return  mixyuv 
  
core.max_cache_size = 120000
episode1 = core.dgdecodenv.DGSource(r'00003.dgi')
episode = core.std.Crop(episode1, top=138, bottom=138)
ed_titles = core.std.Trim(episode, 133466, 139412)
nced = core.dgdecodenv.DGSource(r'00010.dgi').std.Trim(367, 6313)
nced = core.std.Crop(nced, top=138, bottom=138)
nced_aa = core.raws.Source(r'nc.y4m').std.Trim(367, 6313)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = lumaAA(episode)
mrgc = episode.std.Trim(0, 941)+insaneaa.std.Trim(942, 1541)+episode.std.Trim(1542, 1654)+insaneaa.std.Trim(1655, 133465)+ed+episode.std.Trim(139413, 139952)+insaneaa.std.Trim(139953, 141077)+episode.std.Trim(141078, 141239)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[1733 1788]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\02.png'), "[1839 1911]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\03.png'), "[1912 1980]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\04.png'), "[1981 2070]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\05.png'), "[2147 2205]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\06.png'), "[2206 2272]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\07.png'), "[2273 2324]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[2325 2399]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\09.png'), "[2428 2485]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10.png'), "[2486 2547]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11.png'), "[2548 2606]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\12.png'), "[2787 2857]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\13.png'), "[2966 3025]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\14.png'), "[3116 3206]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\15.png'), "[3221 3301]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\16.png'), "[3380 3488]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\17.png'), "[139953 139976]")
clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=19, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
den2 = cooldegrain.CoolDegrain(clip16, tr=1, thsad=24, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=17, cb=10, cr=10, grainy=21, grainc=21, output_depth=16, keep_tv_range=True)
db2 = core.f3kdb.Deband(den2, range=31, y=31, cb=10, cr=10, grainy=48, grainc=48, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
filtered3 = core.std.MaskedMerge(db2, clip16, Mask, planes=[0,1,2], first_plane=True)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
mrgc2 = episode3.std.Trim(0, 133465)+episode4.std.Trim(133466, 133754)+episode3.std.Trim(133755, 138321)+episode4.std.Trim(138322, 138668)+episode3.std.Trim(138669, 139534)+episode4.std.Trim(139535, 139952)+episode3.std.Trim(139953, 141239)
mrgc2.set_output()