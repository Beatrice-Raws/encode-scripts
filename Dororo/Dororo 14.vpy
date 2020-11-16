from vapoursynth import core, VideoNode, GRAY
import vapoursynth as vs
import atomchtools as at
import fvsfunc as fvf
import cooldegrain as cd
import xvs
import insaneAA

core.max_cache_size = 40000


def denoise_and_deband(clip: vs.VideoNode) -> vs.VideoNode:
    linemask = at.retinex_edgemask(clip, sigma=0.1, opencl=True, draft=False).std.Expr('x 2 *')
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    den = cd.CoolDegrain(clip16, tr=1, thsad=32, thsadc=32, bits=16, blksize=8, overlap=4)
    deb = core.placebo.Deband(den, iterations=10, threshold=1.9)
    debanded = core.std.MaskedMerge(deb, clip16, linemask, planes=[0,1,2], first_plane=True)
    return debanded
	
def hard_deband2(clip: vs.VideoNode) -> vs.VideoNode:
    linemask = at.retinex_edgemask(clip, sigma=0.1, opencl=True, draft=False).std.Expr('x 2 *')
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    vPF = core.neo_dfttest.DFTTest(clip16, sigma=2, tbsize=1)
    den = cd.CoolDegrain(clip16, tr=1, pf=vPF, thsad=64, thsadc=64, bits=16, blksize=8, overlap=4)
    deb = core.placebo.Deband(den, iterations=10, threshold=4.0)
    debanded = core.std.MaskedMerge(deb, clip16, linemask, planes=[0,1,2], first_plane=True)
    return debanded


op_deb_fix_start, op_deb_fix_end, ed_AA_start, ed_AA_end, ed_start, ed_end = 3575, 3608, 33754, 33858, 31880, 34045
episode = core.dgdecodenv.DGSource(r'00002.dgi')

AA = insaneAA.insaneAA(episode, kernel='bicubic', descale_height=806, eedi3_mode=insaneAA.EEDI3Mode.OPENCL, nnedi3_mode=insaneAA.NNEDI3Mode.NNEDI3CL)
AA_clip = AA.std.Trim(0, ed_start-1) + episode.std.Trim(ed_start, ed_AA_start-1) + AA.std.Trim(ed_AA_start, ed_AA_end) + episode.std.Trim(ed_AA_end+1, ed_end) + AA.std.Trim(ed_end+1, episode.num_frames-1)

AA_mask = fvf.rfs(AA_clip, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-1.webp'), "[2907 3004]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-2.webp'), "[3021 3128]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-3.webp'), "[3147 3254]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-4.webp'), "[3275 3382]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-5.webp'), "[3388 3481]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-6.webp'), "[3575 3660]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-7.webp'), "[3828 3923]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-8.webp'), "[3941 4011]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-9.webp'), "[4139 4242]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-10.webp'), "[4266 4349]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-11.webp'), "[4358 4445]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-12.webp'), "[4644 4746]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-13.webp'), "[4747 4794]")

DD_clip = denoise_and_deband(AA_mask).std.Trim(0, op_deb_fix_start-1) + hard_deband2(AA_mask).std.Trim(op_deb_fix_start, op_deb_fix_end) + denoise_and_deband(AA_mask).std.Trim(op_deb_fix_end+1, episode.num_frames-1)
AA_mask16 = core.fmtc.bitdepth(AA_mask, bits=16)

deb_mask = fvf.rfs(DD_clip, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-1.webp'), "[3575 3575]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-2.webp'), "[3576 3577]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-3.webp'), "[3583 3584]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-4.webp'), "[3585 3586]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-5.webp'), "[3587 3588]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-6.webp'), "[3589 3590]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-7.webp'), "[3591 3592]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-8.webp'), "[3593 3594]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-9.webp'), "[3595 3596]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-10.webp'), "[3597 3598]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-11.webp'), "[3599 3600]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-12.webp'), "[3601 3602]")

deb_mask.fmtc.bitdepth(bits=10).set_output()