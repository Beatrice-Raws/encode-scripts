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
	
def hard_deband(clip: vs.VideoNode) -> vs.VideoNode:
    linemask = at.retinex_edgemask(clip, sigma=0.1, opencl=False, draft=False)
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    deb1 = core.placebo.Deband(clip16, iterations=10, threshold=4)
    deb2 = xvs.SAdeband(deb1)
    debanded = core.std.MaskedMerge(deb2, clip16, linemask, planes=[0,1,2], first_plane=True)
    return debanded


op_deb_fix_start, op_deb_fix_end, ed_start, ed_end = 3939, 3974, 31899, 34069
episode = core.dgdecodenv.DGSource(r'00002.dgi')

AA = insaneAA.insaneAA(episode, kernel='bicubic', descale_height=806, eedi3_mode=insaneAA.EEDI3Mode.OPENCL, nnedi3_mode=insaneAA.NNEDI3Mode.NNEDI3CL)
AA_clip = AA.std.Trim(0, ed_start-1) + episode.std.Trim(ed_start, ed_end) + AA.std.Trim(ed_end+1, episode.num_frames-1)

mask = fvf.rfs(AA_clip, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-1.webp'), "[1953 2066]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-2.webp'), "[2068 2144]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-3.webp'), "[2146 2239]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-4.webp'), "[2246 2329]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-5.webp'), "[2333 2459]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-6.webp'), "[2754 2835]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-7.webp'), "[2984 3066]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-8.webp'), "[3069 3145]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-9.webp'), "[3305 3403]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-10.webp'), "[3416 3486]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-11.webp'), "[3487 3558]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-12.webp'), "[3560 3663]")
mask = fvf.rfs(mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op-13.webp'), "[4014 4074]")

DD_clip = denoise_and_deband(mask).std.Trim(0, op_deb_fix_start-1) + hard_deband(mask).std.Trim(op_deb_fix_start, op_deb_fix_end) + denoise_and_deband(mask).std.Trim(op_deb_fix_end+1, ed_start-1) + hard_deband(mask).std.Trim(ed_start, episode.num_frames-1)

DD_clip.fmtc.bitdepth(bits=10).set_output()