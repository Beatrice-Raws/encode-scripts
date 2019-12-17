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
def DiffRescaleMask(clip: VideoNode, descale_h: int = 872, descale_w: int = None, kernel: str = 'bicubic', b=0, c=0.5, mthr: int = 85) -> VideoNode:
    ''' Builds mask from difference of original and re-upscales clips '''
    funcName = 'DiffRescaleMask'
    if not isinstance(clip, VideoNode):
        raise TypeError(funcName + ': \"clip\" must be a clip!')
    descale_w = havsfunc.m4((clip.width * descale_h) / clip.height) if descale_w == None else descale_w
    dclip = dsc.Descale(clip, descale_w, descale_h, kernel=kernel, b=b, c=c)
    uclip = core.fmtc.resample(dclip, clip.width, clip.height, kernel=kernel, a1=b, a2=c).fmtc.bitdepth(bits=8)
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
episode = core.dgdecodenv.DGSource(r'03.dgi')
op_titles = core.std.Trim(episode, 1654, 3812)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(0, 2158)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(0, 2158)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 33981, 35411)
nced = core.dgdecodenv.DGSource(r'NCED1.dgi').std.Trim(7, 1437)
nced_aa = core.raws.Source(r'NCED1.y4m').std.Trim(7, 1437)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = zaika(episode)

mrgc = insaneaa.std.Trim(0, 1653)+op+insaneaa.std.Trim(3813, 17861)+episode.std.Trim(17862, 17916)+insaneaa.std.Trim(17917, 33980)+ed+insaneaa.std.Trim(35412, 35891)+episode.std.Trim(35892, 36227)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\07.png'), "[3814 3933]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\08.png'), "[11446 11510]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\09.png'), "[12795 12846]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\10.png'), "[18950 19045]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\11.png'), "[32355 32401]")

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













