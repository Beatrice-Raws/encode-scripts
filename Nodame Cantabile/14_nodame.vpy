from vapoursynth import core, VideoNode, GRAY
from functools import reduce
import vapoursynth as vs
import atomchtools as at
import fvsfunc as fvf
import havsfunc as haf
import cooldegrain as cd
import HardAA as haa
import insaneAA
import dhh



# MC_A_bob by real.finder
# ported similarly to mcdaa3 from havsfunc
def MC_A_bob_and_deint(input, order=None, mode=None, TFF=None, EZDenoise=None, FPSDivisor=None, opencl=None):
    if not isinstance(input, vs.VideoNode):
        raise TypeError('MC_A_bob: This is not a clip')

    TDeint_cilp=core.tdm.TDeintMod(input, order=order, mode=mode)
    sup = core.hqdn3d.Hqdn3d(TDeint_cilp).fft3dfilter.FFT3DFilter().mv.Super(sharp=1)
    fv1 = core.mv.Analyse(sup, isb=False, delta=1, truemotion=False, dct=2)
    fv2 = core.mv.Analyse(sup, isb=True, delta=1, truemotion=True, dct=2)
    csaa = haf.QTGMC(input, Preset='Placebo', TFF=TFF, FPSDivisor=FPSDivisor, SourceMatch=3, Lossless=2, EZDenoise=EZDenoise, TR0=1, TR1=1, TR2=1, Sharpness=1, opencl=opencl)
    momask1 = core.mv.Mask(TDeint_cilp, fv1, ml=2, kind=1)
    momask2 = core.mv.Mask(TDeint_cilp, fv2, ml=3, kind=1)
    momask = core.std.Merge(momask1, momask2)
    return core.std.MaskedMerge(TDeint_cilp, csaa, momask)
	
def hard_fix_comb(clip: vs.VideoNode, EZDenoise=None, rx=None) -> vs.VideoNode:
    pass1 = MC_A_bob_and_deint(clip, order=1, mode=0, TFF=True, EZDenoise=EZDenoise, FPSDivisor=2, opencl=False)
    pass2 = haf.daa(pass1)
    pass3 = core.nnedi3.nnedi3(pass2, field=1, nsize=6, nns=4, qual=2)
    pass4 = haa.HardAA(pass3, useCL=False, sangnomPP=True)
    pass5 = haf.FineDehalo(pass4, rx=rx, darkstr=0.0)
    pass6 = core.vivtc.VDecimate(pass5)
    return pass6

def nodame_aa(clip: vs.VideoNode, dx=None, dy=None) -> vs.VideoNode:
    gray_clip = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray_clip, descale_strength=0.8, kernel='bicubic', descale_height=480)
    fdehalo = haf.FineDehalo(desc, rx=2.5, darkstr=0.0)
    fdehalo2 = haf.FineDehalo2(fdehalo)
    dehalo_mask = dhh.mask(fdehalo2, radius=3.0, dha=True)
    dehalo = core.std.MaskedMerge(desc, fdehalo2, dehalo_mask)
    fld = haf.FastLineDarkenMOD(dehalo, strength=15, protection=7, luma_cap=191, threshold=4, thinning=17)
    rescale = insaneAA.rescale(fld, eedi3_mode=1, nnedi3_mode=2, dx=1920, dy=1080)
    ds = core.fmtc.resample(rescale, w=853, h=480, kernel='blackmanminlobe', taps=4).fmtc.bitdepth(bits=8)
    rescale2 = insaneAA.rescale(ds, eedi3_mode=1, nnedi3_mode=2, dx=dx, dy=dy)
    return insaneAA.insaneAA(clip, external_aa=rescale2, output_mode=0, input_mode=1)

def dehalo(clip: vs.VideoNode) -> vs.VideoNode:
    fdehalo = haf.FineDehalo(clip, rx=2.0, darkstr=0.0)
    dehalo_mask = dhh.mask(fdehalo, radius=2.3, dha=True)
    merge = core.std.MaskedMerge(clip, fdehalo, dehalo_mask)
    return merge

def denoise_and_deband(clip: vs.VideoNode) -> vs.VideoNode:
    linemask = at.retinex_edgemask(clip, sigma=0.1, opencl=False, draft=False).std.Expr('x 1.75 *')
    den = cd.CoolDegrain(clip, tr=1, thsad=32, thsadc=32, bits=16, blksize=8, overlap=4)
    deb = core.placebo.Deband(den, iterations=10, threshold=2.5)
    debanded = core.std.MaskedMerge(deb, clip, linemask, planes=[0,1,2], first_plane=True)
    return debanded


ep_end = 38125
ed_start = 38126
ed_end = 40460
next_start = 40461


core.max_cache_size = 6000

source = core.dgdecodenv.DGSource(r'00002.dgi')

c0 = fvf.JIVTC(source, pattern=0, draft=False, thr=15)
c1 = fvf.JIVTC(source, pattern=1, draft=False, thr=15)
c2 = fvf.JIVTC(source, pattern=2, draft=False, thr=15)
c3 = fvf.JIVTC(source, pattern=3, draft=False, thr=15)
c4 = fvf.JIVTC(source, pattern=4, draft=False, thr=15)

ivtc_clip = core.vivtc.VFM(source, order=1).std.Trim(0,ep_end).vivtc.VDecimate() + core.nnedi3cl.NNEDI3CL(source, field=1, nsize=6, nns=4, qual=2).std.Trim(ed_start,ed_end).std.AssumeFPS(fpsnum=24000, fpsden=1001) + core.vivtc.VFM(source, order=1).std.Trim(next_start,source.num_frames-1).vivtc.VDecimate()

fix_comb_manual = fvf.ReplaceFrames(ivtc_clip, hard_fix_comb(source, EZDenoise=5, rx=2), mappings="6200 12628 [25722 25839] 29186 29190 29408")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, hard_fix_comb(source, EZDenoise=1, rx=1), mappings="9696")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, c2, mappings="6714 12170 12830 12834 12838 12842 12846 12850 12854 15810 15862")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, hard_fix_comb(source, EZDenoise=8, rx=4), mappings="12828 12831 12832 12836 12840 12844 12848 12852 20328 20330 22966 25374 26158 29842")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, c3, mappings="8119 12251 12835 12839 12843 12847 12851 19800 21800 22032 23032")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, haf.daa(c2), mappings="12110 12290 12446 12590 27416 27444")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, haf.daa(ivtc_clip), mappings="6731 7435 7438 7627 7630 7639 7642 7651 7654 7663 7666 7671 7699 7702 7711 10635 10638 10739 10742 10751 10754 12023 12035 12038 12050 12098 12109 12131 12167 12182 12191 12227 12259 12278 12287 12299 12302 12362 12374 12390 12398 12475 12486 12554 12566 12587 12589 12611 12622 12630 12632 27980 27988 28000 29188 29410")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, c4, mappings="16905 16932 16944 16968 21892 30284")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, haf.daa(c4), mappings="21894 27372 27384 27396 27408 30284")
fix_comb_manual = core.std.DeleteFrames(fix_comb_manual, 22888)
fix_comb_manual = core.std.DuplicateFrames(fix_comb_manual, 22888)
fix_comb_manual = core.std.DeleteFrames(fix_comb_manual, 22890)
fix_comb_manual = core.std.DuplicateFrames(fix_comb_manual, 22890)
fix_comb_manual = core.std.DeleteFrames(fix_comb_manual, 28502)
fix_comb_manual = core.std.DuplicateFrames(fix_comb_manual, 28502)

crop = core.std.Crop(fix_comb_manual, left=6, top=10, right=6, bottom=10)

# AA block
titles = at.DiffRescaleMask(crop)
AA = nodame_aa(crop, dx=1908, dy=1060)
masked_titles = at.ApplyMaskOnLuma(crop, AA, titles)
AA_clip = core.std.Trim(AA, 0,30500) + core.std.Trim(masked_titles, 30501,ivtc_clip.num_frames-1)
#

overlay = haf.Overlay(fix_comb_manual, AA_clip, x=6, y=10)

DS_clip = core.fmtc.resample(overlay, w=1280, h=710, sx=5, sy=10, sw=-5, sh=-10, kernel='blackmanminlobe', taps=8)

# fix scene [25265 25372] with bad interlacing
img_25265_25372 = core.imwri.Read(r'.\..\img\25265_25372.webp').resize.Point(format=ivtc_clip.format.id, matrix_s="709", chromaloc_s="top_left")
crop_25265_25372 = core.std.Crop(img_25265_25372, left=6, top=0, right=6, bottom=0)
AA_25265_25372 = nodame_aa(crop_25265_25372, dx=1908, dy=1218)
overlay_25265_25372 = haf.Overlay(img_25265_25372, AA_25265_25372, x=6, y=0)
DS_25265_25372 = core.fmtc.resample(overlay_25265_25372, w=1280, h=816, sx=5, sy=0, sw=-5, sh=0, kernel='blackmanminlobe', taps=8).resize.Point(format=vs.RGB48, matrix_in_s="709")

fix_25265_25372 = reduce(
    lambda x, y: x+y,
    [
        core.std.Crop(DS_25265_25372, bottom=(0+t), top=(106-t))
        for t in range(1, 107)
    ]
).resize.Point(format=DS_clip.format.id, matrix_s="709", chromaloc_s="top_left").std.AssumeFPS(fpsnum=24000, fpsden=1001)
#

DS_clip = DS_clip.std.Trim(0,25264) + fix_25265_25372 + DS_clip.std.Trim(25373,ivtc_clip.num_frames-1)

DH_clip = dehalo(DS_clip)

DD_clip = denoise_and_deband(DH_clip)

deb_mask = fvf.rfs(DD_clip, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1649.webp'), "1649")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1650.webp'), "1650")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1651.webp'), "1651")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1652.webp'), "1652")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1653.webp'), "1653")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1654.webp'), "1654")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1655.webp'), "1655")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1656.webp'), "1656")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1657.webp'), "1657")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1658.webp'), "1658")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1659.webp'), "1659")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1660.webp'), "1660")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1661.webp'), "1661")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1662.webp'), "1662")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1663.webp'), "1663")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1664.webp'), "1664")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1665.webp'), "1665")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1666.webp'), "1666")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1667.webp'), "1667")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1668.webp'), "1668")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1669.webp'), "1669")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1670.webp'), "1670")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1671.webp'), "1671")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1672.webp'), "1672")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1673.webp'), "1673")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1674.webp'), "1674")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1675.webp'), "1675")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1676.webp'), "1676")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1677.webp'), "1677")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1678.webp'), "1678")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1679.webp'), "1679")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1680.webp'), "1680")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, DH_clip, r'.\..\mask\01_nodame_1681.webp'), "1681")

deb_mask.fmtc.bitdepth(bits=10).set_output()