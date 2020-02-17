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

@functoolz.curry
def overlay_credits_in_oped(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    ncop_src = open_source(r'.\udon_no_kuni_ncop.dgi').std.Trim(0,2156)
    ncop_processed = core.lsmas.LWLibavSource(r'.\udon_no_kuni_ncop_loss.mkv').std.Trim(0,2156)

    nced_src = open_source(r'.\udon_no_kuni_nced.dgi')
    nced_src = nced_src.std.Trim(301,585) + nced_src.std.Trim(587,2159) + nced_src.std.BlankClip(length=179)
    nced_src = nced_src.std.FreezeFrames([1858], [2036], [1857])
    nced_processed = core.lsmas.LWLibavSource(r'.\udon_no_kuni_nced_loss.mkv')
    nced_processed = nced_processed.std.Trim(301,585) + nced_processed.std.Trim(587,2159) + nced_processed.std.BlankClip(length=179)
    nced_processed = nced_processed.std.FreezeFrames([1858], [2036], [1857])

    op = atf.ApplyCredits(source.std.Trim(1104,3260), ncop_src, ncop_processed)
    ed = atf.ApplyCredits(source.std.Trim(28244,30280), nced_src, nced_processed)

    return clip.std.Trim(0,1103) + op + clip.std.Trim(3261,28243) + ed + clip.std.Trim(30281)

@functoolz.curry
def overlay_episode_title(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    mask = havsfunc.mt_expand_multi(atf.DiffRescaleMask(core.std.Trim(source, 3370, 3370), descale_h=720, kernel='bicubic', b=1/3, c=1/3, mthr=150), sw=3, sh=3)
    return atf.rfs(clip, core.std.MaskedMerge(clip, source, mask, planes=[0], first_plane=True), [[3348,3465]])

@functoolz.curry
def overlay_credits_in_preview(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    mask = atf.ProcessRegion(atf.DiffRescaleMask(core.std.Trim(source, 32752, 32752), descale_h=720, kernel='bicubic', b=1/3, c=1/3, mthr=150), lambda clip: clip, 128, 1384, 944, 80)
    return atf.rfs(clip, core.std.MaskedMerge(clip, source, mask, planes=[0], first_plane=True), [[32690,32846]])



source_file = r'.\udon_no_kuni_01.dgi'

src = open_source(source_file)

filter_chain = functoolz.compose(overlay_credits_in_preview(source=src), overlay_episode_title(source=src), overlay_credits_in_oped(source=src), fix_edges, do_main_aa)

filtered = filter_chain(src)

filtered.set_output(0)
