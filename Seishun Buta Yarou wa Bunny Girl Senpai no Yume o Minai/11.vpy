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
episode = core.dgdecodenv.DGSource(r'11.dgi')
op_titles = core.std.Trim(episode, 2159, 4316)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(1, 2158)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(1, 2158)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 34413, 35656)
nced = core.dgdecodenv.DGSource(r'NCED5.dgi').std.Trim(7, 1250)
nced_aa = core.raws.Source(r'NCED5.y4m').std.Trim(7, 1250)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = zaika(episode)

mrgc = insaneaa.std.Trim(0, 2158)+op+insaneaa.std.Trim(4317, 20522)+episode.std.Trim(20523, 20570)+insaneaa.std.Trim(20571, 34412)+ed+insaneaa.std.Trim(35657, 35891)+episode.std.Trim(35892, 35987)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\47.png'), "[4318 4429]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\48.png'), "[4442 4561]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\49.png'), "[6485 6553]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\50.png'), "[21189 21241]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\51.png'), "[25258 25304]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\52.png'), "[25985 26043]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\53.png'), "[31265 31525]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\54.png'), "[31961 32026]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, DiffRescaleMask(episode), planes=[0], first_plane=True), "[35757 35843]")


#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
clip_y = mvf.GetPlane(clip16, 0)
pf = core.dfttest.DFTTest(clip_y, sigma=7, tbsize=3, opt=3)
den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=34, thsadc=34, bits=16, blksize=8, overlap=4, pf=pf)
filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(filtered, smode=6, thr_det=2, grainy=34, grainc=24,tv_range=True, planes=[0])
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, openCL=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.29))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode3.set_output()













