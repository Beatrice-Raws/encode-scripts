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
episode = core.dgdecodenv.DGSource(r'10.dgi')
op_titles = core.std.Trim(episode, 3238, 4380)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(0, 1142)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(0, 1142)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
op_titles2 = core.std.Trim(episode, 4507, 5394)
ncop2 = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(1269, 2156)
ncop_aa2 = core.raws.Source(r'NCOP.y4m').std.Trim(1269, 2156)
op2 = atf.ApplyCredits(op_titles2, ncop2, ncop_aa2)
ed_titles = core.std.Trim(episode, 30548, 32703)
nced = core.raws.Source(r'NCED40.y4m').std.Trim(25, 2180)
nced_aa = core.raws.Source(r'NCED4.y4m').std.Trim(25, 2180)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Wotaku_aa(episode)
insaneaa1 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)

mrgc = insaneaa1.std.Trim(0, 70)+insaneaa.std.Trim(71, 658)+insaneaa1.std.Trim(659, 766)+insaneaa.std.Trim(767, 1292)+insaneaa1.std.Trim(1293, 1742)+insaneaa.std.Trim(1743, 2003)+insaneaa1.std.Trim(2004, 2455)+insaneaa.std.Trim(2456, 2846)+insaneaa1.std.Trim(2847, 2896)+insaneaa.std.Trim(2897, 3237)+op+insaneaa.std.Trim(4381, 4506)+op2+insaneaa1.std.Trim(5395, 7238)+insaneaa.std.Trim(7239, 9682)+insaneaa1.std.Trim(9683, 10394)+insaneaa.std.Trim(10395, 14866)+episode.std.Trim(14867, 14986)+insaneaa.std.Trim(14987, 16258)+insaneaa1.std.Trim(16259, 16747)+insaneaa.std.Trim(16748, 18253)+insaneaa1.std.Trim(18254, 18698)+insaneaa.std.Trim(18699, 19288)+insaneaa1.std.Trim(19289, 19784)+insaneaa.std.Trim(19785, 21339)+insaneaa1.std.Trim(21340, 21559)+insaneaa.std.Trim(21560, 21624)+insaneaa1.std.Trim(21625, 21706)+insaneaa.std.Trim(21707, 22177)+insaneaa1.std.Trim(22178, 22523)+insaneaa.std.Trim(22524, 22586)+insaneaa1.std.Trim(22587, 22720)+insaneaa.std.Trim(22721, 25237)+insaneaa1.std.Trim(25238, 25928)+insaneaa.std.Trim(25929, 26572)+insaneaa1.std.Trim(26573, 26761)+insaneaa.std.Trim(26762, 26844)+insaneaa1.std.Trim(26845, 26927)+insaneaa.std.Trim(26928, 27293)+insaneaa1.std.Trim(27294, 27521)+insaneaa.std.Trim(27522, 30307)+insaneaa1.std.Trim(30308, 30547)+ed+insaneaa1.std.Trim(32704, 32847)+episode.std.Trim(32848, 32871)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\2900.png'), "[4384 4430]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\2800.png'), "[4431 4481]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\28.png'), "[22924 22998]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\29.png'), "[30464 30546]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\30.png'), "[32719 32790]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
clip_y = mvf.GetPlane(clip16, 0)
pf = core.dfttest.DFTTest(clip_y, sigma=7, tbsize=3, opt=3)
den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=34, thsadc=34, bits=16, blksize=8, overlap=4, pf=pf)
filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(filtered, smode=6, thr_det=2, grainy=28, grainc=24,tv_range=True, planes=[0])
harddb = core.f3kdb.Deband(filtered, range=8, y=42, cb=26, cr=26, grainy=110, grainc=80, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, openCL=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(harddb, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.26))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
mrgc2 = episode3.std.Trim(0, 27460)+episode4.std.Trim(27461, 27531)+episode3.std.Trim(27532, 32871)
mrgc2.set_output()
