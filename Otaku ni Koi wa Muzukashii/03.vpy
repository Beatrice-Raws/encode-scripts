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
def DiffRescaleMask(clip: VideoNode, descale_h: int = 874, descale_w: int = None, kernel: str = 'bicubic', b=0.33, c=0.33, mthr: int = 165) -> VideoNode:
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

def Wotaku_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=873, bicubic_b=0.33, bicubic_c=0.33)
    graydh = fd.fine_dehalo(desc, darkstr=0.2, brightstr=0.5, showmask=0, thmi=40, thma=60, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'03.dgi')
op_titles = core.std.Trim(episode, 1512, 3668)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(1, 2157)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(1, 2157)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 29563, 31720)
nced = core.raws.Source(r'NCED33.y4m').std.Trim(25, 2182)
nced_aa = core.raws.Source(r'NCED333.y4m').std.Trim(25, 2182)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Wotaku_aa(episode)
insaneaa1 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 1511)+op+insaneaa.std.Trim(3669, 3774)+insaneaa1.std.Trim(3775, 3917)+insaneaa.std.Trim(3918, 10692)+episode.std.Trim(10693, 10812)+insaneaa.std.Trim(10813, 10871)+insaneaa1.std.Trim(10872, 11020)+insaneaa.std.Trim(11021, 11616)+insaneaa1.std.Trim(11617, 11800)+insaneaa.std.Trim(11801, 11854)+insaneaa1.std.Trim(11855, 11931)+insaneaa.std.Trim(11932, 12552)+insaneaa1.std.Trim(12553, 12752)+insaneaa.std.Trim(12753, 21764)+insaneaa1.std.Trim(21765, 22534)+insaneaa.std.Trim(22535, 23349)+insaneaa1.std.Trim(23350, 23808)+insaneaa.std.Trim(23809, 23879)+insaneaa1.std.Trim(23880, 23956)+insaneaa.std.Trim(23957, 25271)+insaneaa1.std.Trim(25272, 25407)+insaneaa.std.Trim(25408, 25881)+insaneaa1.std.Trim(25882, 26000)+insaneaa.std.Trim(26001, 26693)+insaneaa1.std.Trim(26694, 27100)+insaneaa.std.Trim(27101, 28341)+insaneaa1.std.Trim(28342, 28509)+insaneaa.std.Trim(28510, 29360)+insaneaa1.std.Trim(29361, 29490)+insaneaa.std.Trim(29491, 29562)+ed+insaneaa.std.Trim(31721, 31791)+insaneaa1.std.Trim(31792, 31838)+insaneaa.std.Trim(31839, 32280)+insaneaa1.std.Trim(32281, 32572)+insaneaa.std.Trim(32573, 32871)+episode.std.Trim(32872, 32895)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\10.png'), "[3682 3757]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\11.png'), "[29492 29561]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\12.png'), "[31734 31791]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
clip_y = mvf.GetPlane(clip16, 0)
pf = core.dfttest.DFTTest(clip_y, sigma=7, tbsize=3, opt=3)
den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=34, thsadc=34, bits=16, blksize=8, overlap=4, pf=pf)
filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(filtered, smode=6, thr_det=2, grainy=28, grainc=24,tv_range=True, planes=[0])
harddb = core.f3kdb.Deband(filtered, range=8, y=42, cb=26, cr=26, grainy=110, grainc=80, output_depth=16, keep_tv_range=True)
harddb2 = core.f3kdb.Deband(filtered, range=8, y=42, cb=26, cr=26, grainy=90, grainc=60, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, openCL=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(harddb, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered4 = core.std.MaskedMerge(harddb2, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.26))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
episode5 = core.fmtc.bitdepth(filtered4, bits=10)
mrgc2 = episode3.std.Trim(0, 856)+episode4.std.Trim(857, 976)+episode3.std.Trim(977, 1143)+episode4.std.Trim(1144, 1509)+episode3.std.Trim(1510, 14646)+episode4.std.Trim(14647, 14681)+episode3.std.Trim(14682, 23956)+episode4.std.Trim(23957, 24010)+episode3.std.Trim(24011, 27953)+episode5.std.Trim(27954, 28001)+episode3.std.Trim(28002, 28294)+episode4.std.Trim(28295, 28341)+episode3.std.Trim(28342, 32895)
mrgc2.set_output()
