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
import regress

def rotate_clockwise(clip: VideoNode) -> VideoNode:
    return clip.std.Transpose().std.FlipHorizontal()

def rotate_counterclockwise(clip: VideoNode) -> VideoNode:
    return clip.std.Transpose().std.FlipVertical()

def lumaAA(clip, pscrn=1, dev=-1):
    ux = clip.width * 4
    uy = clip.height * 4
    luma = core.std.ShufflePlanes(clip, 0, GRAY)
    upscale = core.nnedi3cl.NNEDI3CL(luma, field=1, dh=True, dw=True, nsize=6, nns=4, pscrn=pscrn, device=dev)
    rotated = rotate_clockwise(upscale)
    interpolated = rotated.eedi3m.EEDI3CL(field=1, dh=True, alpha=0.4,beta=0.25,gamma=20.0,nrad=2,mdis=20, hp=False,ucubic=True,cost3=True,vcheck=2,vthresh0=32,vthresh1=64,vthresh2=4, sclip=rotated.nnedi3.nnedi3(field=1, dh=True, nsize=0, nns=4, pscrn=1, qual=2), device=dev)
    interpolated = rotate_counterclockwise(interpolated)
    interpolated = interpolated.eedi3m.EEDI3CL(field=1, dh=True, alpha=0.4,beta=0.25,gamma=20.0,nrad=2,mdis=20, hp=False,ucubic=True,cost3=True,vcheck=2,vthresh0=32,vthresh1=64,vthresh2=4, sclip=interpolated.nnedi3.nnedi3(field=1, dh=True, nsize=0, nns=4, pscrn=1, qual=2), device=dev)
    downscale = core.resize.Spline36(interpolated, clip.width, clip.height, src_left=-1.5, src_top=-1.5, src_width=ux, src_height=uy)
    downscale = core.std.Expr([downscale, luma], 'x 0.65 * y 0.35 * +')
    return core.std.ShufflePlanes([downscale,clip], [0,1,2], YUV)
    
def mangle_luma(clip: VideoNode) -> VideoNode:
    luma = mvf.GetPlane(clip,0)
    luma_mangled = luma.resize.Point(960,1080, src_left=-1).resize.Bicubic(960,540, filter_param_a=0.0, filter_param_b=0.5)
    return luma_mangled    
  
def demangle_plane(clip: VideoNode) -> VideoNode:
    descaled = mvf.GetPlane(clip,0)
    descaled = descaled.resize.Bicubic(960,1080, filter_param_a=0.0, filter_param_b=0.5, format=GRAYS)
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
    return core.std.ShufflePlanes([clip, reconstructed],[0,1,2], YUV)

core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'00003.dgi')
episode1 = lumaAA(episode)
episode2 = do_chroma_aa(episode1)

clip420 = core.fmtc.resample(episode2, css='420')
clip420.set_output()











