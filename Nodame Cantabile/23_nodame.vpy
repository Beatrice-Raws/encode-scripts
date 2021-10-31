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


ep_end = 34215
ed_start = 34216
ed_end = 37760
next_start = 37761


core.max_cache_size = 6000

source = core.dgdecodenv.DGSource(r'00005.dgi')

c0 = fvf.JIVTC(source, pattern=0, draft=False, thr=15)
c1 = fvf.JIVTC(source, pattern=1, draft=False, thr=15)
c2 = fvf.JIVTC(source, pattern=2, draft=False, thr=15)
c3 = fvf.JIVTC(source, pattern=3, draft=False, thr=15)
c4 = fvf.JIVTC(source, pattern=4, draft=False, thr=15)

ivtc_clip = core.vivtc.VFM(source, order=1).std.Trim(0,ep_end).vivtc.VDecimate() + core.nnedi3cl.NNEDI3CL(source, field=1, nsize=6, nns=4, qual=2).std.Trim(ed_start,ed_end).std.AssumeFPS(fpsnum=24000, fpsden=1001) + core.vivtc.VFM(source, order=1).std.Trim(next_start,source.num_frames-1).vivtc.VDecimate()

fix_comb_manual = fvf.ReplaceFrames(ivtc_clip, c2, mappings="8754")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, c3, mappings="9239 23237")
fix_comb_manual = fvf.ReplaceFrames(fix_comb_manual, c0, mappings="23741 23749 23765 23773 23785 23788 23793 23796 23817")
fix_comb_manual = core.std.DeleteFrames(fix_comb_manual, 23745)
fix_comb_manual = core.std.DuplicateFrames(fix_comb_manual, 23744)
fix_comb_manual = core.std.DeleteFrames(fix_comb_manual, 31252)
fix_comb_manual = core.std.DuplicateFrames(fix_comb_manual, 31252)

trim_28208 = core.std.Trim(fix_comb_manual, 28208, 28208)
trim_28209 = core.std.Trim(fix_comb_manual, 28209, 28209)
crop_28209 = core.std.Crop(trim_28209, left=920, top=0, right=0, bottom=0)
fix_28209 = haf.Overlay(trim_28208, crop_28209, x=920, y=0)

fix_comb_manual = core.std.Trim(fix_comb_manual,0,28208) + fix_28209 + core.std.Trim(fix_comb_manual,28210,ivtc_clip.num_frames-1)

crop = core.std.Crop(fix_comb_manual, left=6, top=10, right=6, bottom=10)

# AA block
titles = at.DiffRescaleMask(crop)
AA = nodame_aa(crop, dx=1908, dy=1060)
masked_titles = at.ApplyMaskOnLuma(crop, AA, titles)
AA_clip = core.std.Trim(AA, 0,27372) + core.std.Trim(masked_titles, 27373,ivtc_clip.num_frames-1)
#

overlay = haf.Overlay(fix_comb_manual, AA_clip, x=6, y=10)

DS_clip = core.fmtc.resample(overlay, w=1280, h=710, sx=5, sy=10, sw=-5, sh=-10, kernel='blackmanminlobe', taps=8)

DH_clip = dehalo(DS_clip)

DD_clip = denoise_and_deband(DH_clip)

DD_clip.fmtc.bitdepth(bits=10).set_output()