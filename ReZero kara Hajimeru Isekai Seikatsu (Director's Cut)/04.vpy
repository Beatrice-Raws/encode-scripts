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

def DiffRescaleMask(clip: VideoNode, descale_h: int = 720, descale_w: int = None, kernel: str = 'bilinear', mthr: int = 40) -> VideoNode:
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
    rescale = insaneAA.rescale(desc, eedi3_mode=1, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'04.dgi')
insaneaa = re_zero_aa(episode)

mrgc = insaneaa.std.Trim(0, 2309)+episode.std.Trim(2310, 2437)+insaneaa.std.Trim(2438, 71614)+episode.std.Trim(71615, 71743)+insaneaa.std.Trim(71744, 74325)+episode.std.Trim(74326, 74351)

orig_rfs = fvf.rfs

def overriden_rfs(passed_clip, replacement, zones):
    import re
    ranges = re.findall('\[\s*\d+\s+\d+\s*\]', zones)
    maps = []
    for range_ in ranges:
        maps.append([int(x) for x in range_.strip('[ ]').split()])
    start, end = maps[0]
    ep01_op = 1605
    ep02_op = 1030
    start, end = int(start)-ep01_op, int(end)-ep01_op
    start, end = start+ep02_op, end+ep02_op
    return orig_rfs(passed_clip, replacement, f"[{start} {end}]")

fvf.rfs = overriden_rfs

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[1649 1751]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\02.png'), "[1862 1958]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\03.png'), "[1994 2070]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\04.png'), "[2106 2181]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\05.png'), "[2227 2302]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\06.png'), "[2347 2424]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\07.png'), "[2492 2574]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[2591 2664]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\09.png'), "[2714 2785]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10.png'), "[3053 3127]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11.png'), "[3134 3231]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\12.png'), "[3335 3406]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\13.png'), "[3527 3597]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\14.png'), "[3693 3763]")

fvf.rfs = orig_rfs

mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, DiffRescaleMask(episode), planes=[0], first_plane=True), "[71744 74325]")

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
pf2 = core.dfttest.DFTTest(clip16, sigma=7, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=24, thsadc=22, bits=16, blksize=8, overlap=4, pf=pf)
den2 = cooldegrain.CoolDegrain(clip16, tr=1, thsad=24, thsadc=22, bits=16, blksize=8, overlap=4, pf=pf2)
db = core.f3kdb.Deband(den, range=31, y=18, cb=11, cr=11, grainy=18, grainc=18, output_depth=16, keep_tv_range=True)
db2 = core.f3kdb.Deband(den2, range=31, y=74, cb=11, cr=11, grainy=28, grainc=28, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(db2, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
mrgc2 = episode4.std.Trim(0, 76)+episode3.std.Trim(77, 1902)+episode4.std.Trim(1903, 2132)+episode3.std.Trim(2133, 71734)+episode4.std.Trim(71735, 72934)+episode3.std.Trim(72935, 72999)+episode4.std.Trim(73000, 73576)+episode3.std.Trim(73577, 74351)
mrgc2.set_output()
