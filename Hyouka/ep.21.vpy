from vapoursynth import core, VideoNode, GRAY, YUV, GRAYS
import vapoursynth as vs
import atomchtools as atf
import fvsfunc as fvf
import mvsfunc as mvf
#	import kagefunc as kg
import GradFun3 as gfa
import insaneAA
import cooldegrain
from DGavs import DGSource
import HardAAp2
import finedehalo
import descale as dsc
import regress

def rotate_clockwise(clip: VideoNode) -> VideoNode:
    return clip.std.Transpose().std.FlipHorizontal()

def rotate_counterclockwise(clip: VideoNode) -> VideoNode:
    return clip.std.Transpose().std.FlipVertical()
    
def mangle_luma(clip: VideoNode) -> VideoNode:
    luma = mvf.GetPlane(clip,0)
    luma_orig = dsc.Debicubic(luma, 1700, 956, b=0.0, c=0.5, gray=True)
    luma_mangled = luma_orig.resize.Point(850,956, src_left=-1).resize.Bicubic(850,478, filter_param_a=0.0, filter_param_b=0.5)
    return luma_mangled
    
def demangle_plane(clip: VideoNode) -> VideoNode:
    descaled = clip.resize.Bicubic(850,956, filter_param_a=0, filter_param_b=0.5).resize.Bicubic(format=GRAYS)
    rotated = rotate_clockwise(descaled)
    interpolated = rotated.eedi3m.EEDI3CL(field=1, dh=True, alpha=0.4,beta=0.25,gamma=10.0,nrad=3,mdis=40, hp=False,ucubic=True,cost3=True,vcheck=3,vthresh0=32,vthresh1=64,vthresh2=4, sclip=rotated.nnedi3.nnedi3(field=1, dh=True, nsize=6, nns=4, pscrn=1, qual=2), device=0)
    interpolated = rotate_counterclockwise(interpolated)
    return interpolated
    
def do_chroma_aa(clip: VideoNode) -> VideoNode:
    luma_descaled = mvf.GetPlane(clip,0)
    luma_descaled = dsc.Debicubic(luma_descaled, 1700, 956, b=0.0, c=0.5, gray=True)
    luma_mangled = mangle_luma(luma_descaled)
    reconstructed = regress.Reconstruct(luma_descaled.resize.Bicubic(format=GRAYS),
                                        demangle_plane(luma_mangled),
                                        demangle_plane(mvf.GetPlane(clip, 1)),
                                        demangle_plane(mvf.GetPlane(clip, 2)),  use_binary=True, radius=3)
    return core.std.ShufflePlanes([clip, reconstructed.resize.Bicubic(960,540, filter_param_a=1, filter_param_b=0)],[0,1,2], YUV)

EP = DGSource(r'.\index\ep.21.dgi')
#	name = core.raws.Source(r'21name.yuv') # (3069,3220)
OP = EP.std.Trim(912,3068)
ED = EP.std.Trim(36705,38862)

chroma_aa = do_chroma_aa(EP)
clip420 = core.fmtc.resample(chroma_aa, css='420')
aaep_chroma = insaneAA.insaneAA(clip420,  eedi3_mode=1, nnedi3_mode=2, descale_strength=0.28, kernel='BICUBIC', descale_height=955, mdis=15)
aaep_chroma = core.fmtc.bitdepth(aaep_chroma, bits=8)

aaep = insaneAA.insaneAA(EP,  eedi3_mode=1, nnedi3_mode=2, descale_strength=0.28, kernel='BICUBIC', descale_height=955, mdis=15)
clip1_d = insaneAA.revert_upscale(EP.std.ShufflePlanes(0, vs.GRAY), descale_strength=0.28, kernel='BICUBIC', descale_height=955)
clip1_d = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d = finedehalo.fine_dehalo(clip1_d, rx=1.5, darkstr=0, brightstr=0.8)
clip1_u = insaneAA.rescale(clip1_d, eedi3_mode=1, nnedi3_mode=2, alpha=0.99, beta=0.01, gamma=0.1, pscrn=0, mdis=20, dx=1920, dy=1080)
aaep2 = insaneAA.insaneAA(EP, external_aa=clip1_u)

sousT = core.std.Trim(EP, 3069,3220)
aa_sousT = core.std.Trim(aaep, 3069,3220)
mask_sousT = core.lsmas.LWLibavSource(r'title 21 mask.mp4').std.Binarize().std.Inflate().std.Maximum()
TIT = core.std.MaskedMerge(aa_sousT, sousT, mask_sousT)

mrgc = aaep.std.Trim(0,911) +OP +TIT +aaep.std.Trim(3221,36704) +ED +aaep.std.Trim(38863,39151)
mrgc = fvf.rfs(mrgc, aaep_chroma, "[5141 5233]")
mrgc = fvf.rfs(mrgc, core.std.Expr([mrgc, aaep2], 'x {val} * y 1 {val} - * +'.format(val=0.7)), "[5141 5233]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\2101.png'), "[15116 15178]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, EP, r'.\mask\21nxt.png'), "[39031 39102]")

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
luma = mvf.GetPlane(clip16, 0)
denluma = cooldegrain.CoolDegrain(luma, tr=1, thsad=48, bits=16, blksize=8, overlap=4)
cleaned = core.std.ShufflePlanes([denluma, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(cleaned, smode=6, thr_det=1.4, mask=0, grainy=48, grainc=24,tv_range=False, planes=[0])
mask = atf.retinex_edgemask(clip16, sigma=1, draft=False, openCL=True).std.Expr('x 2 *')
postdb = core.std.MaskedMerge(db, clip16, mask, planes=[0,1,2], first_plane=True)
mix = core.std.Expr([postdb, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.67))

clip = core.fmtc.bitdepth(mix, bits=10)
#	clip = atf.MakeTestEncode(clip)
clip.set_output()