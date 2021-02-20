from vapoursynth import core, VideoNode, GRAY, YUV
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import GradFun3 as gfa
import insaneAA
import cooldegrain
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
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'01.dgi')
op_titles = core.std.Trim(episode, 3727, 5873)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(9, 2155)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(9, 2155)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 30714, 32413)
nced = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(195, 1894)
nced_aa = core.raws.Source(r'NCED.y4m').std.Trim(195, 1894)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Wotaku_aa(episode)
insaneaa1 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)

mrgc = insaneaa1.std.Trim(0, 192)+insaneaa.std.Trim(193, 3726)+op+insaneaa1.std.Trim(5874, 5968)+insaneaa.std.Trim(5969, 14266)+insaneaa1.std.Trim(14267, 14457)+episode.std.Trim(14458, 14577)+insaneaa.std.Trim(14578, 18923)+insaneaa1.std.Trim(18924, 19063)+insaneaa.std.Trim(19064, 23738)+insaneaa1.std.Trim(23739, 24025)+insaneaa.std.Trim(24026, 25144)+insaneaa1.std.Trim(25145, 25347)+insaneaa.std.Trim(25348, 27323)+insaneaa1.std.Trim(27324, 27671)+insaneaa.std.Trim(27672, 29423)+insaneaa1.std.Trim(29424, 29563)+insaneaa.std.Trim(29564, 30200)+insaneaa1.std.Trim(30201, 30469)+insaneaa.std.Trim(30470, 30713)+ed+insaneaa.std.Trim(32414, 32895)

mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, DiffRescaleMask(episode), planes=[0], first_plane=True), "[3319 3592]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\01.png'), "[16567 16614]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, DiffRescaleMask(episode), planes=[0], first_plane=True), "[14696 14840]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\02.png'), "[21059 21141]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\03.png'), "[30619 30713]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\04.png'), "[32446 32571]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\05.png'), "[32644 32763]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\06.png'), "[32795 32870]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip = mrgc
inputY = core.std.ShufflePlanes(clip, 0, GRAY)
descaledY = insaneAA.revert_upscale(inputY, descale_strength=0.28, kernel='bicubic', descale_height=873)
resizedY = core.resize.Bicubic(descaledY, 1280, 720)
resizedUV = core.resize.Bicubic(clip, 1280, 720)
out = core.std.ShufflePlanes([resizedY,resizedUV,resizedUV], [0,1,2], clip.format.color_family)
clip16 = core.fmtc.bitdepth(out, bits=16)
clip_y = mvf.GetPlane(clip16, 0)
pf = core.dfttest.DFTTest(clip_y, sigma=7, tbsize=3, opt=3)
den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=20, thsadc=20, bits=16, blksize=8, overlap=4, pf=pf)
filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(filtered, smode=6, thr_det=2, grainy=24, grainc=20,tv_range=True, planes=[0])
harddb = core.f3kdb.Deband(filtered, range=8, y=32, cb=26, cr=26, grainy=80, grainc=60, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, openCL=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(harddb, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.10))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
mrgc2 = episode3.std.Trim(0, 9794)+episode4.std.Trim(9795, 9859)+episode3.std.Trim(9860, 11730)+episode4.std.Trim(11731, 11765)+episode3.std.Trim(11766, 17825)+episode4.std.Trim(17826, 17890)+episode3.std.Trim(17891, 25407)+episode4.std.Trim(25408, 25478)+episode3.std.Trim(25479, 32895)
mrgc2.set_output()
