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

def DiffRescaleMask(clip: VideoNode, descale_h: int = 720, descale_w: int = None, kernel: str = 'bilinear', mthr: int = 50) -> VideoNode:
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


def re_zero_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.26, kernel='bilinear', descale_height=720) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.6, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    rescale = insaneAA.rescale(graydh, eedi3_mode=1, nnedi3_mode=2, dx=1920, dy=1080, alpha=0.2, beta=0.6, gamma=40) 
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv  


core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'21.dgi')
op_titles = core.std.Trim(episode, 4297, 6449)
ncop = core.dgdecodenv.DGSource(r'NCOP2.dgi').std.Trim(4, 2156)
ncop_aa = core.raws.Source(r'NCOP2_2.y4m').std.Trim(4, 2156)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
insaneaa = re_zero_aa(episode)

mrgc = insaneaa.std.Trim(0, 4296)+op+insaneaa.std.Trim(6450, 41545)+episode.std.Trim(41546, 41617)+insaneaa.std.Trim(41618, 42436)+episode.std.Trim(42437, 42475)

mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, DiffRescaleMask(episode), planes=[0], first_plane=True), "[38868 41391]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, DiffRescaleMask(episode), planes=[0], first_plane=True), "[42300 42436]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=24, thsadc=22, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=19, cb=11, cr=11, grainy=20, grainc=20, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()
