from vapoursynth import core, VideoNode, GRAY
import vapoursynth as vs
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc as hf
import mvsfunc as mvf
import gradfun_amod as gfa
import insaneAA
import HardAAp2 as HardAA
import cooldegrain as cd
import finedehalo as fdh

core.max_cache_size = 40000


def SAC_aa(clip: vs.VideoNode) -> vs.VideoNode:
    clipY = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(clipY, descale_strength=0.8, kernel='bicubic', bicubic_b=0, bicubic_c=0.75, descale_width=None, descale_height=540)
    hard = HardAA.HardAA(desc, mask=None, nrad=2, alpha=0.15, beta=0.2)
    mask = core.std.MakeDiff(desc, hard).hist.Luma().std.Expr('x 2 *').rgvs.RemoveGrain(2).std.Expr('x 50 < 0 x 2 * ?').std.Maximum()
    maskedHard = core.std.MaskedMerge(desc, hard, mask)
    rescale = insaneAA.rescale(maskedHard, eedi3Mode='cpu', nnedi3Mode='opencl', dx=1920, dy=1080)
    return insaneAA.insaneAA(clip, externalAA=rescale, outputMode=0, inputMode=1)
    
def denoise_and_deband_OP(clip: vs.VideoNode) -> vs.VideoNode:
    clip16 = core.fmtc.bitdepth(clip, bits=16)

    peak = (1 << clip16.format.bits_per_sample) - 1
    pref1 = core.dfttest.DFTTest(clip16, tbsize=1, sstring='0.0:10.0 0.2:14.0 1.0:20.0')
    mask = core.std.Expr(clip16.std.ShufflePlanes(0, GRAY), 'x {i} < {peak} x {j} > 0 {peak} x {i} - {peak} {j} {i} - / * - ? ?'.format(i=hf.scale(16, peak), j=hf.scale(75, peak), peak=peak))
    pref2 = core.std.MaskedMerge(pref1, clip16, mask)

    den = cd.CoolDegrain(clip16, tr=1, pf=pref2, thsad=48, thsadc=48, bits=16, blksize=8, overlap=4)
    deb = gfa.GradFun3(den, smode=6, thr_det=3.0, grainy=32, grainc=22, tv_range=True, planes=[0])
    Mask = kg.retinex_edgemask(clip16, sigma=0.1, draft=False)
    filtered = core.std.MaskedMerge(deb, clip16, Mask, planes=[0,1,2], first_plane=True)
    return  core.fmtc.bitdepth(filtered, bits=10)
    
def denoise_and_deband(clip: vs.VideoNode) -> vs.VideoNode:
    clip16 = core.fmtc.bitdepth(clip, bits=16)

    peak = (1 << clip16.format.bits_per_sample) - 1
    pref1 = core.dfttest.DFTTest(clip16, tbsize=1, sstring='0.0:4.0 0.2:7.0 1.0:12.0')
    mask = core.std.Expr(clip16.std.ShufflePlanes(0, GRAY), 'x {i} < {peak} x {j} > 0 {peak} x {i} - {peak} {j} {i} - / * - ? ?'.format(i=hf.scale(16, peak), j=hf.scale(75, peak), peak=peak))
    pref2 = core.std.MaskedMerge(pref1, clip16, mask)

    den = cd.CoolDegrain(clip16, tr=1, pf=pref2, thsad=32, thsadc=32, bits=16, blksize=8, overlap=4)
    deb = gfa.GradFun3(den, smode=6, thr_det=2.0, grainy=32, grainc=22, tv_range=True, planes=[0])
    Mask = kg.retinex_edgemask(clip16, sigma=0.1, draft=False)
    filtered = core.std.MaskedMerge(deb, clip16, Mask, planes=[0,1,2], first_plane=True)
    return  core.fmtc.bitdepth(filtered, bits=10)
    
def denoise_and_deband_ED(clip: vs.VideoNode) -> vs.VideoNode:
    den = core.dfttest.DFTTest(clip, sigma=10, tbsize=1)
    deb = gfa.GradFun3(den, thr_det=6.0, grainy=32, grainc=22)
    return  deb
    

episode = core.lsmas.LWLibavSource(r'12-1.avi')
qtgmclines = core.raws.Source(r'../qtgmclines.y4m')
qtgmclines = core.std.AssumeFPS(qtgmclines, fpsnum=367810000, fpsden=15088073)

borderfix = core.edgefixer.Continuity(episode, 2, 0, 2, 0, 2)

deb_ed_1 = atf.rfs(borderfix, atf.ApplyImageMask(borderfix, denoise_and_deband_ED(borderfix), r'..\mask01.png'), [[33779,34071]])
deb_ed_2 = atf.rfs(deb_ed_1, atf.ApplyImageMask(borderfix, denoise_and_deband_ED(borderfix), r'..\mask02.png'), [[34367,34634]])
deb_ed_3 = atf.rfs(deb_ed_2, atf.ApplyImageMask(borderfix, denoise_and_deband_ED(borderfix), r'..\mask03.png'), [[35294,35415]])

titles = atf.DiffRescaleMask(deb_ed_3)

mrgc = SAC_aa(deb_ed_3).std.Trim(0, 889) + qtgmclines + SAC_aa(deb_ed_3).std.Trim(977, 33657) + deb_ed_3.std.Trim(33658, 35851) + SAC_aa(deb_ed_3).std.Trim(35852, episode.num_frames-1)

masktitles = atf.ApplyMaskOnLuma(deb_ed_3, mrgc, titles)

crop = core.std.CropRel(masktitles, left=0, top=22, right=0, bottom=22)

ds = core.fmtc.resample(crop, 1280, 690, kernel='blackmanminlobe', taps=16)

dh_end = ds.std.Trim(0, 33657) + fdh.fine_dehalo(ds, rx=1.5,darkstr=0.0).std.Trim(33658, 35851) +  ds.std.Trim(35852, episode.num_frames-1)

filt = denoise_and_deband(dh_end).std.Trim(0, 782) + denoise_and_deband_OP(dh_end).std.Trim(783, 834) + denoise_and_deband(dh_end).std.Trim(835, 1715) + denoise_and_deband_OP(dh_end).std.Trim(1716, 1795) + denoise_and_deband(dh_end).std.Trim(1796, 2017) + denoise_and_deband_OP(dh_end).std.Trim(2018, 2081) + denoise_and_deband(dh_end).std.Trim(2082, 2306) + denoise_and_deband_OP(dh_end).std.Trim(2307, 2326) + denoise_and_deband(dh_end).std.Trim(2327, 2380) + denoise_and_deband_OP(dh_end).std.Trim(2381, 2432) + denoise_and_deband(dh_end).std.Trim(2433, 27482) + denoise_and_deband_OP(dh_end).std.Trim(27483, 29356) +      denoise_and_deband(dh_end).std.Trim(29357, episode.num_frames-1)

filt.set_output()