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


op_deb_fix_start, op_deb_fix_end, ed_AA_start, ed_AA_end, ed_start, ed_end = 1394, 1427, 33777, 33881, 31898, 34068
episode = core.dgdecodenv.DGSource(r'00004.dgi')

AA = insaneAA.insaneAA(episode, kernel='bicubic', descale_height=806, eedi3_mode=insaneAA.EEDI3Mode.OPENCL, nnedi3_mode=insaneAA.NNEDI3Mode.NNEDI3CL)
AA_clip = AA.std.Trim(0, ed_start-1) + episode.std.Trim(ed_start, ed_AA_start-1) + AA.std.Trim(ed_AA_start, ed_AA_end) + episode.std.Trim(ed_AA_end+1, ed_end) + AA.std.Trim(ed_end+1, episode.num_frames-1)

AA_mask = fvf.rfs(AA_clip, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-1.webp'), "[726 823]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-2.webp'), "[840 947]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-3.webp'), "[966 1073]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-4.webp'), "[1094 1201]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-5.webp'), "[1207 1300]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-6.webp'), "[1394 1479]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-7.webp'), "[1647 1742]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-8.webp'), "[1760 1830]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-9.webp'), "[1958 2061]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-10.webp'), "[2085 2168]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-11.webp'), "[2177 2264]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-12.webp'), "[2463 2565]")
AA_mask = fvf.rfs(AA_mask, at.ApplyImageMask(AA_clip, episode, r'.\mask\op2-13.webp'), "[2566 2612]")

DD_clip = denoise_and_deband(AA_mask).std.Trim(0, op_deb_fix_start-1) + hard_deband2(AA_mask).std.Trim(op_deb_fix_start, op_deb_fix_end) + denoise_and_deband(AA_mask).std.Trim(op_deb_fix_end+1, episode.num_frames-1)
AA_mask16 = core.fmtc.bitdepth(AA_mask, bits=16)

deb_mask = fvf.rfs(DD_clip, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-1.webp'), "[1394 1394]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-2.webp'), "[1395 1396]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-3.webp'), "[1402 1403]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-4.webp'), "[1404 1405]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-5.webp'), "[1406 1407]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-6.webp'), "[1408 1409]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-7.webp'), "[1410 1411]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-8.webp'), "[1412 1413]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-9.webp'), "[1414 1415]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-10.webp'), "[1416 1417]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-11.webp'), "[1418 1419]")
deb_mask = fvf.rfs(deb_mask, at.ApplyImageMask(DD_clip, AA_mask16, r'.\mask\op2-deb-12.webp'), "[1420 1421]")

deb_mask.fmtc.bitdepth(bits=10).set_output()