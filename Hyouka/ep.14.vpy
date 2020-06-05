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

EP = DGSource(r'.\index\ep.14.dgi')
name = core.raws.Source(r'14name.yuv') # (3333,3502)
OP = EP.std.Trim(1176,3332)
ED = EP.std.Trim(34525,36682)

aaep = insaneAA.insaneAA(EP,  eedi3_mode=1, nnedi3_mode=2, descale_strength=0.28, kernel='BICUBIC', descale_height=955, mdis=15)
clip1_d = insaneAA.revert_upscale(EP.std.ShufflePlanes(0, vs.GRAY), descale_strength=0.28, kernel='BICUBIC', descale_height=955)
clip1_d = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d = HardAAp2.HardAA(clip1_d, mask=None, alpha=0.99, beta=0.01, gamma=0.1, sangnomPP=True)
clip1_d = finedehalo.fine_dehalo(clip1_d, rx=1.5, darkstr=0, brightstr=0.8)
clip1_u = insaneAA.rescale(clip1_d, eedi3_mode=1, nnedi3_mode=2, alpha=0.99, beta=0.01, gamma=0.1, pscrn=0, mdis=20, dx=1920, dy=1080)
aaep2 = insaneAA.insaneAA(EP, external_aa=clip1_u)

mrgc = aaep.std.Trim(0,1175) +OP +name +aaep.std.Trim(3503,34524) +ED +aaep.std.Trim(36683,36946)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, EP, r'.\mask\14nxt.png'), "[36853 36922]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1401.png'), "[6070 6075]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1402.png'), "[6076 6078]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1403.png'), "[6079 6081]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1404.png'), "[6082 6084]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1405.png'), "[6085 6087]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1406.png'), "[6088 6090]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1407.png'), "[6091 6093]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1408.png'), "[6094 6096]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1409.png'), "[6097 6099]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, aaep2, r'.\mask\1410.png'), "[6100 6102]")

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