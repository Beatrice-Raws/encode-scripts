import vapoursynth as vs
import atomchtools as atf
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

def fix_shimmering(clip: vs.VideoNode) -> vs.VideoNode:
    return atf.rfs(clip, havsfunc.QTGMC(clip, InputType=1, SourceMatch=3), [[19277,19444],[24013,24225],[24472,24549]])

@functoolz.curry
def overlay_credits_in_oped(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    ncop_src = open_source(r'.\udon_no_kuni_ncop.dgi').std.Trim(0,2158)
    ncop_processed = core.lsmas.LWLibavSource(r'.\udon_no_kuni_ncop_loss.mkv').std.Trim(0,2158)

    nced_src = open_source(r'.\udon_no_kuni_nced.dgi')
    nced_src = nced_src.std.Trim(0,2156)
    nced_processed = core.lsmas.LWLibavSource(r'.\udon_no_kuni_nced_loss.mkv')
    nced_processed = nced_processed.std.Trim(0,2156)

    op = atf.ApplyCredits(source.std.Trim(1534,3692), ncop_src, ncop_processed)
    ed = atf.ApplyCredits(source.std.Trim(28508,30664), nced_src, nced_processed)

    return clip.std.Trim(0,1533) + op + clip.std.Trim(3693,28507) + ed + clip.std.Trim(30665)

@functoolz.curry
def overlay_episode_title(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    mask = havsfunc.mt_expand_multi(atf.DiffRescaleMask(core.std.Trim(source, 3900, 3900), descale_h=720, kernel='bicubic', b=1/3, c=1/3, mthr=150), sw=4, sh=4).std.Binarize()
    return atf.rfs(clip, core.std.MaskedMerge(clip, source, mask, planes=[0], first_plane=True), [[3844,3937]])

@functoolz.curry
def overlay_credits_in_preview(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    mask = atf.ProcessRegion(atf.DiffRescaleMask(core.std.Trim(source, 32607, 32607), descale_h=720, kernel='bicubic', b=1/3, c=1/3, mthr=150), lambda clip: clip, 128, 1384, 944, 80)
    return atf.rfs(clip, core.std.MaskedMerge(clip, source, mask, planes=[0], first_plane=True), [[32607,32846]])



source_file = r'.\udon_no_kuni_05.dgi'

src = open_source(source_file)

filter_chain = functoolz.compose(overlay_credits_in_preview(source=src), overlay_episode_title(source=src), overlay_credits_in_oped(source=src), fix_shimmering, fix_edges, do_main_aa)

filtered = filter_chain(src)

filtered.set_output(0)
