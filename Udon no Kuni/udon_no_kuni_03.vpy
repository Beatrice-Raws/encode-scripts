import vapoursynth as vs
import atomchtools as atf
import kagefunc as kg
import havsfunc
import insaneAA
from toolz import functoolz

core = vs.core
core.max_cache_size = 18432

def open_source(path: str) -> vs.VideoNode:
    return core.dgdecodenv.DGSource(path)

def do_main_aa(clip: vs.VideoNode) -> vs.VideoNode:
    return insaneAA.insaneAA(clip, eedi3Mode='cpu', nnedi3Mode='nnedi3', descale_strength=0.45, kernel='bicubic', bicubic_b=0.0, bicubic_c=1.0, descale_height=720)

def fix_edges(clip: vs.VideoNode) -> vs.VideoNode:
    return core.edgefixer.Continuity(clip, 2, 2, 2, 2)

def deband_scene(clip: vs.VideoNode) -> vs.VideoNode:
    clip16 = clip.fmtc.bitdepth(bits=16)
    dbmask = kg.retinex_edgemask(clip16, sigma=0.1, draft=False).std.Binarize(7680,0).std.Invert()

    debanded = core.f3kdb.Deband(clip, range=31, y=128, cb=96, cr=96, grainy=112, grainc=80, keep_tv_range=True, output_depth=16)
    dbmerged = core.std.MaskedMerge(clip16, debanded, dbmask, planes=[0,1,2], first_plane=True)

    return atf.rfs(clip, dbmerged.fmtc.bitdepth(bits=8), [[309,392]])

@functoolz.curry
def overlay_credits_in_oped(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    ncop_src = open_source(r'.\udon_no_kuni_ncop.dgi').std.Trim(0,2156)
    ncop_processed = core.lsmas.LWLibavSource(r'.\udon_no_kuni_ncop_loss.mkv').std.Trim(0,2156)

    nced_src = open_source(r'.\udon_no_kuni_nced.dgi').std.Trim(0,2157)
    nced_processed = core.lsmas.LWLibavSource(r'.\udon_no_kuni_nced_loss.mkv').std.Trim(0,2157)

    op = atf.ApplyCredits(source.std.Trim(1200,3356), ncop_src, ncop_processed)
    ed = atf.ApplyCredits(source.std.Trim(26133,28290), nced_src, nced_processed)

    return clip.std.Trim(0,1199) + op + clip.std.Trim(3357,26132) + ed + clip.std.Trim(28291)

@functoolz.curry
def overlay_episode_title(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    mask = havsfunc.mt_expand_multi(atf.DiffRescaleMask(core.std.Trim(source, 3450, 3450), descale_h=720, kernel='bicubic', b=1/3, c=1/3, mthr=90), sw=4, sh=4).std.Binarize()
    return atf.rfs(clip, core.std.MaskedMerge(clip, source, mask, planes=[0], first_plane=True), [[3407,3500]])

@functoolz.curry
def overlay_credits_in_preview(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    mask = atf.ProcessRegion(atf.DiffRescaleMask(core.std.Trim(source, 32752, 32752), descale_h=720, kernel='bicubic', b=1/3, c=1/3, mthr=150), lambda clip: clip, 128, 1384, 944, 80)
    return atf.rfs(clip, core.std.MaskedMerge(clip, source, mask, planes=[0], first_plane=True), [[32606,32845]])



source_file = r'.\udon_no_kuni_03.dgi'

src = open_source(source_file)

filter_chain = functoolz.compose(overlay_credits_in_preview(source=src), overlay_episode_title(source=src), overlay_credits_in_oped(source=src), deband_scene, fix_edges, do_main_aa)

filtered = filter_chain(src)

filtered.set_output(0)
