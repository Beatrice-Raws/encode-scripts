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

EP = DGSource(r'.\index\ep.02.dgi')

nced = DGSource(r'.\index\nc.dgi').std.Trim(2280,4437)
edaa = insaneAA.insaneAA(nced,  eedi3_mode=1, nnedi3_mode=2, descale_strength=0.28, kernel='BICUBIC', descale_height=955, mdis=15)
ed_t = core.std.Trim(EP, 34598,36755)
ED = atf.ApplyCredits(ed_t, nced, edaa)

aaep = insaneAA.insaneAA(EP,  eedi3_mode=1, nnedi3_mode=2, descale_strength=0.28, kernel='BICUBIC', descale_height=955, mdis=15)
clip1_d = insaneAA.revert_upscale(EP.std.ShufflePlanes(0, vs.GRAY), descale_strength=0.28, kernel='BICUBIC', descale_height=955)
clip1_d = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d = finedehalo.fine_dehalo(clip1_d, rx=1.5, darkstr=0, brightstr=0.8)
clip1_u = insaneAA.rescale(clip1_d, eedi3_mode=1, nnedi3_mode=2, alpha=0.99, beta=0.01, gamma=0.1, pscrn=0, mdis=20, dx=1920, dy=1080)
aaep2 = insaneAA.insaneAA(EP, external_aa=clip1_u)

sousT = core.std.Trim(EP, 4086,4295)
aa_sousT = core.std.Trim(aaep, 4086,4295)
mask_sousT = core.lsmas.LWLibavSource(r'title 02 mask.mp4').std.Binarize().std.Inflate().std.Maximum().std.Trim(0,209)
TIT = core.std.MaskedMerge(aa_sousT, sousT, mask_sousT)
TIT = fvf.rfs(TIT, atf.ApplyImageMask(aa_sousT, sousT, r'.\mask\0201.png'), "[114 128]")
TIT = fvf.rfs(TIT, atf.ApplyImageMask(aa_sousT, sousT, r'.\mask\0202.png'), "[129 129]")
TIT = fvf.rfs(TIT, atf.ApplyImageMask(aa_sousT, sousT, r'.\mask\0203.png'), "[130 130]")
TIT = fvf.rfs(TIT, atf.ApplyImageMask(aa_sousT, sousT, r'.\mask\0204.png'), "[131 131]")
TIT = fvf.rfs(TIT, atf.ApplyImageMask(aa_sousT, sousT, r'.\mask\0205.png'), "[132 132]")
TIT = fvf.rfs(TIT, atf.ApplyImageMask(aa_sousT, sousT, r'.\mask\0206.png'), "[133 133]")
TIT = fvf.rfs(TIT, atf.ApplyImageMask(aa_sousT, sousT, r'.\mask\0207.png'), "[134 134]")
TIT = fvf.rfs(TIT, atf.ApplyImageMask(aa_sousT, sousT, r'.\mask\0208.png'), "[135 135]")
TIT = fvf.rfs(TIT, atf.ApplyImageMask(aa_sousT, sousT, r'.\mask\0209.png'), "[136 136]")
TIT = fvf.rfs(TIT, atf.ApplyImageMask(aa_sousT, sousT, r'.\mask\0210.png'), "[137 137]")

mrgc = aaep.std.Trim(0,1869) +EP.std.Trim(1870,4028) +aaep.std.Trim(4029,4085) +TIT +aaep.std.Trim(4296,34597) +ED +aaep.std.Trim(36756,36947)
mrgc = fvf.rfs(mrgc, core.std.Expr([mrgc, aaep2], 'x {val} * y 1 {val} - * +'.format(val=0.9)), "[22977 23120]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, EP, r'.\mask\02nxt.png'), "[36835 36923]")

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