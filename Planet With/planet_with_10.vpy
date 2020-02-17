import vapoursynth as vs
import atomchtools as atf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import gradfun_amod as gfa
import insaneAA
import HardAAp2 as HardAA
import cooldegrain
from toolz import functoolz

core = vs.core
core.max_cache_size = 24576

def open_source(path: str) -> vs.VideoNode:
    return core.dgdecodenv.DGSource(path)

def do_main_aa(clip: vs.VideoNode) -> vs.VideoNode:
    return insaneAA.insaneAA(clip, eedi3Mode='cpu', nnedi3Mode='nnedi3', descale_strength=0.3, kernel='bicubic', bicubic_b=1/3, bicubic_c=1/3, descale_height=958, descale_width=1704)

def do_hard_aa(clip: vs.VideoNode) -> vs.VideoNode:
    gray_clip = core.std.ShufflePlanes(clip, 0, vs.GRAY)
    linemask = core.std.Sobel(gray_clip).std.Expr("x 2 *").std.Maximum()
    desc = insaneAA.revert_upscale(clip, kernel='bicubic', bicubic_b=1/3, bicubic_c=1/3, descale_height=958, descale_width=1704, descale_strength=0.3)
    hardaa =  HardAA.HardAA(desc, mask=None, nrad=2, alpha=0.9, beta=0.1, gamma=5)
    appliedaa = core.std.MaskedMerge(desc, hardaa, linemask.resize.Spline36(1704,958))
    rescaledaa = insaneAA.rescale(appliedaa, eedi3Mode='cpu', nnedi3Mode='nnedi3', dx=1920, dy=1080)

    the_rest = atf.rfs(clip, core.std.MaskedMerge(clip, rescaledaa, linemask, planes=[0], first_plane=True), [[11208,11311],[13322,13363],[13567,13804]])
    return the_rest

def denoise_and_deband(clip: vs.VideoNode) -> vs.VideoNode:
    clip16 = core.fmtc.bitdepth(clip, bits=16)
    clip_y = mvf.GetPlane(clip16, 0)
    pf = core.dfttest.DFTTest(clip_y, sigma=4, tbsize=3, opt=2)
    deg_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=32, thsadc=32, bits=16, blksize=8, overlap=4, pf=pf)
    deg = core.std.ShufflePlanes([deg_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
    db = gfa.GradFun3(deg, smode=6, thr_det=2, grainy=34, grainc=24,tv_range=True, planes=[0])
    linemask = kg.retinex_edgemask(clip16, sigma=0.1, draft=False).std.Binarize(9828,0)
    debanded = core.std.MaskedMerge(db, clip16, linemask, planes=[0,1,2], first_plane=True)
    mixed = core.std.Expr([debanded, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.40))
    return mixed.fmtc.bitdepth(bits=10)

@functoolz.curry
def overlay_credits_in_oped(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    ncop_src = open_source(r'.\planet_with_ncop.dgi').std.Trim(2184,4340)
    ncop_processed = core.lsmas.LWLibavSource(r'.\planet_with_ncop2_ll.mkv').std.Trim(0,2156)

    nced_src = open_source(r'.\planet_with_nced.dgi').std.Trim(2568,4341)
    nced_processed = core.lsmas.LWLibavSource(r'.\planet_with_nced2_ll.mkv').std.Trim(384,2157)

    op = atf.ApplyCredits(source.std.Trim(2878,5034), ncop_src, ncop_processed)
    ed = atf.ApplyCredits(source.std.Trim(32271,34044), nced_src, nced_processed)

    return clip.std.Trim(0,2877) + op + clip.std.Trim(5035,32270) + ed + clip.std.Trim(34045)

@functoolz.curry
def overlay_episode_title(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    mask = havsfunc.mt_expand_multi(atf.ProcessRegion(atf.DiffRescaleMask(core.std.Trim(source, 5300, 5300), descale_h=958, descale_w = 1704, kernel='bicubic', b=1.0, c=0.0, mthr=40), lambda clip: clip, 428, 104, 896, 40), sw=5, sh=5)
    return atf.rfs(clip, core.std.MaskedMerge(clip, source, mask, planes=[0], first_plane=True), [[5230,5329]])


source_file = r'.\planet_with_10.dgi'

src = open_source(source_file)

filter_chain = functoolz.compose(denoise_and_deband, overlay_episode_title(source=src), overlay_credits_in_oped(source=src), do_hard_aa, do_main_aa)

filtered = filter_chain(src)

filtered.set_output(0)
