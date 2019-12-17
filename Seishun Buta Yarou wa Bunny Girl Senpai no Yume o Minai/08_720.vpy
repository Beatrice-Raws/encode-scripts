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
def DiffRescaleMask(clip: VideoNode, descale_h: int = 878, descale_w: int = None, kernel: str = 'bilinear', mthr: int = 128) -> VideoNode:
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


def zaika(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bilinear', descale_height=878)
    rescale = insaneAA.rescale(desc, fasterAA=False, eedi3Mode='opencl', eedi3Device=0, nnedi3Mode='opencl', nnedi3Device=0, dx=1920, dy=1080, nsize=6)
    graydh = fd.fine_dehalo(rescale, darkstr=0, brightstr=0.8, showmask=0, rx=1.8, ry=1.8, thmi=50, thma=95, useMtEdge=True)
    aa = insaneAA.insaneAA(clip, externalAA=graydh, outputMode=0, inputMode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

core.set_max_cache_size(60000)	
episode = core.dgdecodenv.DGSource(r'08.dgi')
op_titles = core.std.Trim(episode, 2, 2157)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(2, 2157)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(2, 2157)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 34006, 35436)
nced = core.dgdecodenv.DGSource(r'NCED3.dgi').std.Trim(7, 1437)
nced_aa = core.raws.Source(r'NCED3.y4m').std.Trim(7, 1437)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = zaika(episode)

mrgc = insaneaa.std.Trim(0, 1)+op+insaneaa.std.Trim(2158, 18772)+episode.std.Trim(18773, 18820)+insaneaa.std.Trim(18821, 34005)+ed+insaneaa.std.Trim(35437, 35891)+episode.std.Trim(35892, 36231)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\31.png'), "[2366 2486]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\32.png'), "[7830 7900]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\33.png'), "[10616 10669]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\34.png'), "[11497 11625]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\35.png'), "[23648 23707]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\36.png'), "[32090 32159]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip = mrgc
inputY = core.std.ShufflePlanes(clip, 0, GRAY)
descaledY = insaneAA.revert_upscale(inputY, descale_strength=0.28, kernel='bicubic', descale_height=720)
resizedY = core.resize.Bicubic(descaledY, 1280, 720)
resizedUV = core.resize.Bicubic(clip, 1280, 720,)
out = core.std.ShufflePlanes([resizedY,resizedUV,resizedUV], [0,1,2], clip.format.color_family)
clip16 = core.fmtc.bitdepth(out, bits=16)
clip_y = mvf.GetPlane(clip16, 0)
pf = core.dfttest.DFTTest(clip_y, sigma=7, tbsize=3, opt=3)
den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=32, thsadc=32, bits=16, blksize=8, overlap=4, pf=pf)
filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(filtered, smode=6, thr_det=2, grainy=32, grainc=22,tv_range=True, planes=[0])
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, openCL=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.15))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode3.set_output()













