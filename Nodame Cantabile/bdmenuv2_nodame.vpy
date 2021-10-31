from vapoursynth import core, VideoNode, GRAY
import vapoursynth as vs
import atomchtools as at
import havsfunc as haf
import cooldegrain as cd
import dhh


def denoise_and_deband(clip: vs.VideoNode) -> vs.VideoNode:
    linemask = at.retinex_edgemask(clip, sigma=0.1, opencl=True, draft=False).std.Expr('x 1.75 *')
    pf = core.neo_dfttest.DFTTest(clip, tbsize=1, slocation=[0.0,0.1, 0.15,0.5, 0.3,1.0, 0.8,2.0, 1.0,3.0])
    den = cd.CoolDegrain(clip, tr=1, thsad=32, thsadc=32, bits=16, blksize=8, overlap=4, pf=pf)
    deb = core.placebo.Deband(den, iterations=10, threshold=2.5)
    debanded = core.std.MaskedMerge(deb, clip, linemask, planes=[0,1,2], first_plane=True)
    return debanded

def dehalo(clip: vs.VideoNode) -> vs.VideoNode:
    fdehalo = haf.FineDehalo(clip, rx=2.0, darkstr=0.0)
    dehalo_mask = dhh.mask(fdehalo, radius=2.0, dha=True)
    merge = core.std.MaskedMerge(clip, fdehalo, dehalo_mask)
    return merge


core.max_cache_size = 48000

source = core.dgdecodenv.DGSource(r'00011.dgi')

ivtc_clip = core.vivtc.VFM(source, order=1)

DS_clip = core.fmtc.resample(ivtc_clip, w=1280, h=720, kernel='blackmanminlobe', taps=8)

DH_clip = dehalo(DS_clip)

DD_clip = denoise_and_deband(DH_clip).fmtc.bitdepth(bits=10)

DD_clip.set_output()