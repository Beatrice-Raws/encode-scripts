from vapoursynth import *
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import havsfunc as haf
import insaneAA
import cooldegrain
import descale as dsc

def DiffRescaleMask(clip, descale_h=720, kernel='bicubic', mthr=55):
    descale_w = haf.m4((clip.width * descale_h) / clip.height)
    dclip = dsc.Descale(clip, descale_w, descale_h, kernel=kernel)
    uclip = core.fmtc.resample(dclip, clip.width, clip.height, kernel=kernel).fmtc.bitdepth(bits=8)
    uclip = mvf.GetPlane(uclip, 0)
    clip = mvf.GetPlane(clip, 0)
    diff = core.std.MakeDiff(clip, uclip)
    mask = diff.rgvs.RemoveGrain(2).rgvs.RemoveGrain(2).hist.Luma()
    mask = mask.std.Expr('x {thr} < 0 x ?'.format(thr=mthr))
    mask = mask.std.Prewitt().std.Maximum().std.Maximum().std.Deflate()
    return mask

def ApplyMaskOnLuma(src, aa, mask):
	src_y = mvf.GetPlane(src, 0)
	aa_y = mvf.GetPlane(aa, 0)
	mask_y = mvf.GetPlane(mask, 0)
	masked = core.std.MaskedMerge(aa_y, src_y, mask_y)
	result = core.std.ShufflePlanes([masked, mvf.GetPlane(src, 1), mvf.GetPlane(src, 2)], planes=[0, 0, 0], colorfamily=src.format.color_family)
	return result

core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
epis = core.avs.DGSource(r'.\..\index\EP12.dgi')
aaep = insaneAA.insaneAA(epis, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.33, kernel='bicubic', descale_h=720)
ed_src = core.std.Trim(epis, 31372, 33871)
ed_aa  = core.std.Trim(aaep, 31372, 33871)
msk_ed = DiffRescaleMask(ed_src)
ed = ApplyMaskOnLuma(ed_src, ed_aa, msk_ed)
mrgc = aaep.std.Trim(0, 31371) + ed + aaep.std.Trim(33872, int(epis.num_frames-1))
clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=120, thsadc=0, bits=16, blksize=8, overlap=4)
clip = gfa.GradFun3(clip,thr_det=2.5,smode=6,tv_range=True)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
