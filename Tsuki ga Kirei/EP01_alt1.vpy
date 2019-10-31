from vapoursynth import *
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import insaneAA
import cooldegrain
import descale as dsc

def FHDDetailsMask(clip, width=None, height=None, kernel="bicubic"):
    clip_y = mvf.GetPlane(clip, 0)
    if width is None:
        width = 1280
    if height is None:
        height = 720
    native = dsc.Descale(clip_y, width, height, kernel=kernel)
    upscale = core.fmtc.resample(native, clip_y.width, clip_y.height, kernel=kernel, taps=3).fmtc.bitdepth(bits=clip_y.format.bits_per_sample)
    diff = core.std.MakeDiff(clip_y, upscale)
    diff = core.hist.Luma(diff).std.Binarize(90)
    diff = core.rgvs.RemoveGrain(diff, 1).std.Maximum().std.Minimum()
    diff = core.rgvs.RemoveGrain(diff, 4).std.Maximum().std.Deflate()
    return diff
    
def DiffCreditlessMask(titles, nc):
	test = core.std.MakeDiff(titles, nc, [0])
	test = mvf.GetPlane(test, 0)
	test = test.std.Prewitt().std.Expr('x 25 < 0 x ?').std.Expr('x 2 *')
	test = core.rgvs.RemoveGrain(test, 4).std.Expr('x 35 > 255 x ?')
	return test

core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
epis = core.avs.DGSource(r'.\index\EP01.dgi')
aaep = insaneAA.insaneAA(epis, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.32, kernel='bicubic', descale_h=720, outputMode=0)
mrgc = aaep
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\01.png'), "[32876 32944]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\02.png'), "[32951 33022]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\03.png'), "[33029 33100]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\04.png'), "[33107 33178]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\05.png'), "[33185 33256]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\06.png'), "[33263 33334]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\07.png'), "[33341 33412]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\08.png'), "[33419 33490]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\09.png'), "[33497 33568]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\10.png'), "[33575 33646]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\11.png'), "[33654 33725]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\12.png'), "[33733 33804]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\13.png'), "[34530 34601]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\14.png'), "[34608 34679]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\15.png'), "[34686 34757]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\16.png'), "[34764 34835]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\17.png'), "[34842 34913]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\18.png'), "[34920 35028]")
clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=80, thsadc=80, bits=16, blksize=8, overlap=4)
clip = gfa.GradFun3(clip,thr_det=2.8,smode=6,tv_range=True,debug=0)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
