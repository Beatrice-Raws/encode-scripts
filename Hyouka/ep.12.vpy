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


EP = DGSource(r'.\index\ep.12.dgi')
#	name = core.raws.Source(r'12name.yuv') # (5467,5644)
#	fix1 = core.raws.Source(r'12f-1.yuv') # (12192,12425)
OP = EP.std.Trim(3309,5466)
ED = EP.std.Trim(36683,38840)

aaep = insaneAA.insaneAA(EP,  eedi3_mode=1, nnedi3_mode=2, descale_strength=0.28, kernel='BICUBIC', descale_height=955, mdis=15)
clip1_d = insaneAA.revert_upscale(EP.std.ShufflePlanes(0, vs.GRAY), descale_strength=0.28, kernel='BICUBIC', descale_height=955)
clip1_d = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d5 = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d5 = HardAAp2.HardAA(clip1_d5, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d5 = HardAAp2.HardAA(clip1_d5, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d5 = HardAAp2.HardAA(clip1_d5, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d = finedehalo.fine_dehalo(clip1_d, rx=1.5, darkstr=0, brightstr=0.8)
clip1_u = insaneAA.rescale(clip1_d, eedi3_mode=1, nnedi3_mode=2, alpha=0.99, beta=0.01, gamma=0.1, pscrn=0, mdis=20, dx=1920, dy=1080)
aaep2 = insaneAA.insaneAA(EP, external_aa=clip1_u)
clip1_d5 = finedehalo.fine_dehalo(clip1_d5, rx=1.5, darkstr=0, brightstr=0.8)
clip1_u5 = insaneAA.rescale(clip1_d5, eedi3_mode=1, nnedi3_mode=2, alpha=0.99, beta=0.01, gamma=0.1, pscrn=0, mdis=20, dx=1920, dy=1080)
aaep5 = insaneAA.insaneAA(EP, external_aa=clip1_u5)

sousT = core.std.Trim(EP, 5467,5644)
aa_sousT = core.std.Trim(aaep, 5467,5644)
mask_sousT = core.lsmas.LWLibavSource(r'title 12 mask.mp4').std.Binarize().std.Inflate().std.Maximum()
TIT = core.std.MaskedMerge(aa_sousT, sousT, mask_sousT)

mrgc = aaep.std.Trim(0,3308) +OP +TIT +aaep.std.Trim(5645,36682) +ED +aaep.std.Trim(38841,39104)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1201.png'), "[10828 10987]")
mrgc = fvf.rfs(mrgc, core.std.Expr([mrgc, aaep2], 'x {val} * y 1 {val} - * +'.format(val=0.4)), "[12192 12425]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep5, r'.\mask\120200.png'), "[12192 12425]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep, r'.\mask\120201.png'), "[12192 12425]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1203.png'), "[13595 13644]")
mrgc = fvf.rfs(mrgc, core.std.Expr([mrgc, aaep2], 'x {val} * y 1 {val} - * +'.format(val=0.6)), "[19014 19061]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1204.png'), "[26794 26829]")
#	mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1205.png'), "[28996 29052]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1206.png'), "[34140 34259]")
mrgc = fvf.rfs(mrgc, core.std.Expr([mrgc, aaep2], 'x {val} * y 1 {val} - * +'.format(val=0.7)), "[36370 36545]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, EP, r'.\mask\12nxt.png'), "[39009 39080]")

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