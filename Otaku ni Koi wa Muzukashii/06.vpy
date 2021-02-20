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
episode = core.dgdecodenv.DGSource(r'06.dgi')
op_titles = core.std.Trim(episode, 553, 1745)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(0, 1192)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(0, 1192)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
op_titles2 = core.std.Trim(episode, 1822, 2709)
ncop2 = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(1269, 2156)
ncop_aa2 = core.raws.Source(r'NCOP.y4m').std.Trim(1269, 2156)
op2 = atf.ApplyCredits(op_titles2, ncop2, ncop_aa2)
ed_titles = core.std.Trim(episode, 30355, 32510)
nced = core.raws.Source(r'NCED66.y4m').std.Trim(25, 2180)
nced_aa = core.raws.Source(r'NCED666.y4m').std.Trim(25, 2180)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Wotaku_aa(episode)
insaneaa1 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 299)+insaneaa1.std.Trim(300,  552)+op+insaneaa.std.Trim(1746, 1821)+op2+insaneaa.std.Trim(2710, 7004)+insaneaa1.std.Trim(7005, 7213)+insaneaa.std.Trim(7214, 7388)+insaneaa1.std.Trim(7389, 7512)+insaneaa.std.Trim(7513, 7560)+insaneaa1.std.Trim(7561, 7641)+insaneaa.std.Trim(7642, 8259)+insaneaa1.std.Trim(8260, 8370)+insaneaa.std.Trim(8371, 9772)+insaneaa1.std.Trim(9773, 9999)+insaneaa.std.Trim(10000, 11254)+insaneaa1.std.Trim(11255, 11493)+insaneaa.std.Trim(11494, 11861)+insaneaa1.std.Trim(11862, 11938)+insaneaa.std.Trim(11939, 14231)+insaneaa1.std.Trim(14232, 14433)+episode.std.Trim(14434, 14553)+insaneaa.std.Trim(14554, 14991)+insaneaa1.std.Trim(14992, 15468)+insaneaa.std.Trim(15469, 15515)+insaneaa1.std.Trim(15516, 15705)+insaneaa.std.Trim(15706, 16165)+insaneaa1.std.Trim(16166, 17064)+insaneaa.std.Trim(17065, 17360)+insaneaa1.std.Trim(17361, 17500)+insaneaa.std.Trim(17501, 17646)+insaneaa1.std.Trim(17647, 17705)+insaneaa.std.Trim(17706, 20035)+insaneaa1.std.Trim(20036, 20286)+insaneaa.std.Trim(20287, 22671)+insaneaa1.std.Trim(22672, 22763)+insaneaa.std.Trim(22764, 25702)+insaneaa1.std.Trim(25703, 25773)+insaneaa.std.Trim(25774, 26563)+insaneaa1.std.Trim(26564, 26717)+insaneaa.std.Trim(26718, 28297)+insaneaa1.std.Trim(28298, 28667)+insaneaa.std.Trim(28668, 28761)+insaneaa1.std.Trim(28762, 28878)+insaneaa.std.Trim(28879, 29540)+insaneaa1.std.Trim(29541, 29754)+insaneaa.std.Trim(29755, 30354)+ed+insaneaa.std.Trim(32511, 32714)+insaneaa1.std.Trim(32715, 32870)+episode.std.Trim(32871, 32895)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\20.png'), "[189 212]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\21.png'), "[213 260]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\2333.png'), "[1745 1796]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\22.png'), "[6532 6626]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\2222.png'), "[27921 27967]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\23.png'), "[30275 30353]")

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
mrgc2 = episode3.std.Trim(0, 32895)
mrgc2.set_output()
