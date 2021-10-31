from vapoursynth import core, VideoNode, GRAY
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
    pass6 = core.std.Trim(pass5,0,ep_end).vivtc.VDecimate() + core.std.Trim(pass5,ed_start,ed_end).std.AssumeFPS(fpsnum=24000, fpsden=1001) + core.std.Trim(pass5,next_start,source.num_frames-1).vivtc.VDecimate()
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


ep_end = 38119
ed_start = 38120
ed_end = 40460
next_start = 40461


core.max_cache_size = 6000

source = core.dgdecodenv.DGSource(r'00001.dgi')

c0 = fvf.JIVTC(source, pattern=0, draft=False, thr=15)
c1 = fvf.JIVTC(source, pattern=1, draft=False, thr=15)
c2 = fvf.JIVTC(source, pattern=2, draft=False, thr=15)
c3 = fvf.JIVTC(source, pattern=3, draft=False, thr=15)
c4 = fvf.JIVTC(source, pattern=4, draft=False, thr=15)

ivtc_clip = core.vivtc.VFM(source, order=1).std.Trim(0,ep_end).vivtc.VDecimate() + core.nnedi3cl.NNEDI3CL(source, field=1, nsize=6, nns=4, qual=2).std.Trim(ed_start,ed_end).std.AssumeFPS(fpsnum=24000, fpsden=1001) + core.vivtc.VFM(source, order=1).std.Trim(next_start,source.num_frames-1).vivtc.VDecimate()

fix_comb_manual = fvf.ReplaceFrames(ivtc_clip, haf.daa(c2), mappings="7287 7290 7307 7658 19950 20912")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, c3, mappings="8259 8267 9967 11091 16588 22416")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, haf.daa(c3), mappings="26696 26700")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, haf.daa(ivtc_clip), mappings="26699 26702")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, hard_fix_comb(source, EZDenoise=8, rx=1), mappings="9968 10042 11092 20914 20918 [21276 21387] 25834 29570")

crop = core.std.Crop(fix_comb_manual, left=6, top=10, right=6, bottom=10)

# AA block
titles = at.DiffRescaleMask(crop)
AA = nodame_aa(crop, dx=1908, dy=1060)
masked_titles = at.ApplyMaskOnLuma(crop, AA, titles)
AA_clip = core.std.Trim(AA, 0,30496) + core.std.Trim(masked_titles, 30497,ivtc_clip.num_frames-1)
#

overlay = haf.Overlay(fix_comb_manual, AA_clip, x=6, y=10)

DS_clip = core.fmtc.resample(overlay, w=1280, h=710, sx=5, sy=10, sw=-5, sh=-10, kernel='blackmanminlobe', taps=8)

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