from vapoursynth import core
import vapoursynth as vs
import atomchtools as atf
import fvsfunc as fvf
import mvsfunc as mvf
import kagefunc as kg
import GradFun3 as gfa
import insaneAA
import cooldegrain
from DGavs import DGSource
import HardAAp2
import finedehalo

EP = DGSource(r'.\index\ep.04.dgi')
#	name = core.raws.Source(r'04name.yuv')
#	haa01 = core.raws.Source(r'04haa01.yuv') # (8567,8597)
#	haa02 = core.raws.Source(r'04haa02.yuv') # (34421,34519)

nced = DGSource(r'.\index\nc.dgi').std.Trim(2280,4437)
edaa = insaneAA.insaneAA(nced,  eedi3_mode=1, nnedi3_mode=2, descale_strength=0.28, kernel='BICUBIC', descale_height=955, mdis=15)
ed_t = core.std.Trim(EP, 34526,36683)
ED = atf.ApplyCredits(ed_t, nced, edaa)

aaep = insaneAA.insaneAA(EP,  eedi3_mode=1, nnedi3_mode=2, descale_strength=0.28, kernel='BICUBIC', descale_height=955, mdis=15)
clip1_d = insaneAA.revert_upscale(EP.std.ShufflePlanes(0, vs.GRAY), descale_strength=0.28, kernel='BICUBIC', descale_height=955)
clip1_d = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d = finedehalo.fine_dehalo(clip1_d, rx=1.5, darkstr=0, brightstr=0.8)
clip1_u = insaneAA.rescale(clip1_d, eedi3_mode=1, nnedi3_mode=2, alpha=0.99, beta=0.01, gamma=0.1, pscrn=0, mdis=20, dx=1920, dy=1080)
aaep2 = insaneAA.insaneAA(EP, external_aa=clip1_u)

sousT = core.std.Trim(EP, 4269,4410)
aa_sousT = core.std.Trim(aaep, 4269,4410)
mask_sousT = core.lsmas.LWLibavSource(r'title 04 mask.mp4').std.Binarize().std.Inflate().std.Maximum()
TIT = core.std.MaskedMerge(aa_sousT, sousT, mask_sousT)

mrgc = aaep.std.Trim(0,2109) +EP.std.Trim(2110,4268) +TIT +aaep.std.Trim(4411,34525) +ED +aaep.std.Trim(36684,36947)
mrgc = fvf.rfs(mrgc, core.std.Expr([mrgc, aaep2], 'x {val} * y 1 {val} - * +'.format(val=0.6)), "[8567 8597]")
mrgc = fvf.rfs(mrgc, core.std.Expr([mrgc, aaep2], 'x {val} * y 1 {val} - * +'.format(val=0.55)), "[34421 34519]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep, r'.\mask\0401.png'), "[34434 34518]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, EP, r'.\mask\04nxt.png'), "[36838 36923]")

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
luma = mvf.GetPlane(clip16, 0)
denluma = cooldegrain.CoolDegrain(luma, tr=1, thsad=48, bits=16, blksize=8, overlap=4)
cleaned = core.std.ShufflePlanes([denluma, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(cleaned, smode=6, thr_det=1.4, mask=0, grainy=48, grainc=24,tv_range=False, planes=[0])
mask = atf.retinex_edgemask(clip16, sigma=1, draft=False, openCL=True).std.Expr('x 2 *')
postdb = core.std.MaskedMerge(db, clip16, mask, planes=[0,1,2], first_plane=True)
mix = core.std.Expr([postdb, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.67))

clip = core.fmtc.bitdepth(mix, bits=10)
#	clip = atf.MakeTestEncode(clip)
clip.set_output()