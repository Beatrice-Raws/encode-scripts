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
def DiffRescaleMask(clip: VideoNode, descale_h: int = 720, descale_w: int = None, kernel: str = 'bicubic', b=0.33, c=0.33, mthr: int = 85) -> VideoNode:
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

def Log_Horizon_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6) 
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv  

core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'13.dgi')
op_titles = core.std.Trim(episode, 840, 2996)
ncop = core.dgdecodenv.DGSource(r'00053.dgi').std.Trim(24, 2180)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(24, 2180)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
insaneaa = Log_Horizon_aa(episode)

mrgc = insaneaa.std.Trim(0, 839)+op+insaneaa.std.Trim(2997, 35292)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\37.png'), "[4464 4600]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, DiffRescaleMask(episode), planes=[0], first_plane=True), "[32488 34644]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\38.png'), "[35059 35124]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\39.png'), "[35125 35267]")


#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
clip_y = mvf.GetPlane(clip16, 0)
pf = core.dfttest.DFTTest(clip_y, sigma=7, tbsize=3, opt=3)
den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=26, thsadc=26, bits=16, blksize=8, overlap=4, pf=pf)
filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(filtered, smode=6, thr_det=2, grainy=26, grainc=24,tv_range=True, planes=[0])
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, openCL=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.22))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode3.set_output()






