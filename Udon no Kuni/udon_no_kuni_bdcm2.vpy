import vapoursynth as vs
import atomchtools as atf
import havsfunc
import insaneAA
from toolz import functoolz

core = vs.core
core.max_cache_size = 18432

def open_source(path: str) -> vs.VideoNode:
    return core.dgdecodenv.DGSource(path)

@functoolz.curry
def do_main_aa(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    mask = havsfunc.mt_expand_multi(atf.DiffRescaleMask(source, descale_h=720, kernel='bicubic', b=0.0, c=1.0, mthr=45), sw=3, sh=3)
    insaneaaed = insaneAA.insaneAA(clip, eedi3Mode='cpu', nnedi3Mode='nnedi3', descale_strength=0.45, kernel='bicubic', bicubic_b=0.0, bicubic_c=1.0, descale_height=720)
    return atf.rfs(clip, core.std.MaskedMerge(insaneaaed, source, mask, planes=[0], first_plane=True), [[46,359]])

@functoolz.curry
def fix_edges(clip: vs.VideoNode) -> vs.VideoNode:
    return core.edgefixer.Continuity(clip, 2, 2, 2, 2)

source_file = r'.\udon_no_kuni_bdcm2.dgi'

src = open_source(source_file)

filter_chain = functoolz.compose(fix_edges, do_main_aa(source=src))

filtered = filter_chain(src)

filtered.set_output(0)
