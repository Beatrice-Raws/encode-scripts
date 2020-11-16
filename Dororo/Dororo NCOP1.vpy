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

op_deb_fix_start, op_deb_fix_end = 2036, 2071
NCOP1 = core.dgdecodenv.DGSource(r'NCOP1.dgi')

set_matrix = core.resize.Bicubic(NCOP1, matrix_in_s='170m', matrix_s='709')

AA_clip = insaneAA.insaneAA(set_matrix, kernel='bicubic', descale_height=806, eedi3_mode=insaneAA.EEDI3Mode.OPENCL, nnedi3_mode=insaneAA.NNEDI3Mode.NNEDI3CL)

DD_clip = denoise_and_deband(AA_clip).std.Trim(0, op_deb_fix_start-1) + hard_deband(AA_clip).std.Trim(op_deb_fix_start, op_deb_fix_end) + denoise_and_deband(AA_clip).std.Trim(op_deb_fix_end+1, NCOP1.num_frames-1)

DD_clip.fmtc.bitdepth(bits=10).set_output()