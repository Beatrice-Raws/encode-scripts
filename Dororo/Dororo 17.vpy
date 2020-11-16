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


op_deb_fix_start, op_deb_fix_end, ed_AA_start, ed_AA_end, ed_start, ed_end = 5421, 5454, 33778, 33882, 31912, 34069
episode = core.dgdecodenv.DGSource(r'00005.dgi')

AA = insaneAA.insaneAA(episode, kernel='bicubic', descale_height=806, eedi3_mode=insaneAA.EEDI3Mode.OPENCL, nnedi3_mode=insaneAA.NNEDI3Mode.NNEDI3CL)
AA_clip = AA.std.Trim(0, ed_start-1) + episode.std.Trim(ed_start, ed_AA_start-1) + AA.std.Trim(ed_AA_start, ed_AA_end) + episode.std.Trim(ed_AA_end+1, ed_end) + AA.std.Trim(ed_end+1, episode.num_frames-1)

AA_mask = fvf.rfs(AA_clip, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-1.webp'), "[4753 4850]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-2.webp'), "[4867 4974]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-3.webp'), "[4993 5100]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-4.webp'), "[5121 5228]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-5.webp'), "[5234 5327]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-6.webp'), "[5421 5506]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-7.webp'), "[5674 5769]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-8.webp'), "[5787 5857]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-9.webp'), "[5985 6088]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-10.webp'), "[6112 6195]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-11.webp'), "[6204 6291]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-12.webp'), "[6490 6592]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-13.webp'), "[6593 6641]")

DD_clip = denoise_and_deband(AA_mask).std.Trim(0, op_deb_fix_start-1) + hard_deband2(AA_mask).std.Trim(op_deb_fix_start, op_deb_fix_end) + denoise_and_deband(AA_mask).std.Trim(op_deb_fix_end+1, episode.num_frames-1)
AA_mask16 = core.fmtc.bitdepth(AA_mask, bits=16)

deb_mask = fvf.rfs(DD_clip, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-1.webp'), "[5421 5421]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-2.webp'), "[5422 5423]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-3.webp'), "[5429 5430]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-4.webp'), "[5431 5432]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-5.webp'), "[5433 5434]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-6.webp'), "[5435 5436]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-7.webp'), "[5437 5438]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-8.webp'), "[5439 5440]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-9.webp'), "[5441 5442]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-10.webp'), "[5443 5444]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-11.webp'), "[5445 5446]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-12.webp'), "[5447 5448]")

deb_mask.fmtc.bitdepth(bits=10).set_output()