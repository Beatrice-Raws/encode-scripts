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

EP = DGSource(r'.\index\ep.13.dgi')
#	name = core.raws.Source(r'13name.yuv') # (2830,2949)
OP = EP.std.Trim(672,2829)
ED = EP.std.Trim(34551,36708)

aaep = insaneAA.insaneAA(EP,  eedi3_mode=1, nnedi3_mode=2, descale_strength=0.28, kernel='BICUBIC', descale_height=955, mdis=15)
clip1_d = insaneAA.revert_upscale(EP.std.ShufflePlanes(0, vs.GRAY), descale_strength=0.28, kernel='BICUBIC', descale_height=955)
clip1_d = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d = finedehalo.fine_dehalo(clip1_d, rx=1.5, darkstr=0, brightstr=0.8)
clip1_u = insaneAA.rescale(clip1_d, eedi3_mode=1, nnedi3_mode=2, alpha=0.99, beta=0.01, gamma=0.1, pscrn=0, mdis=20, dx=1920, dy=1080)
aaep2 = insaneAA.insaneAA(EP, external_aa=clip1_u)

sousT = core.std.Trim(EP, 2830,2949)
aa_sousT = core.std.Trim(aaep, 2830,2949)
mask_sousT = core.lsmas.LWLibavSource(r'title 13 mask.mp4').std.Binarize().std.Inflate().std.Maximum()
TIT = core.std.MaskedMerge(aa_sousT, sousT, mask_sousT)

mrgc = aaep.std.Trim(0,671) +OP +TIT +aaep.std.Trim(2950,34550) +ED +aaep.std.Trim(36709,36999)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1301.png'), "[9792 9982]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1301.png'), "[10084 10353]") # написанному верить
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1303.png'), "[11224 11348]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, EP, r'.\mask\13nxt.png'), "[36879 36948]")

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