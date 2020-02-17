import vapoursynth as vs
import atomchtools as atf
import insaneAA
from toolz import functoolz

core = vs.core
core.max_cache_size = 18432

def open_source(path: str) -> vs.VideoNode:
    return core.dgdecodenv.DGSource(path)

def do_main_aa(clip: vs.VideoNode) -> vs.VideoNode:
    insaneaaed = insaneAA.insaneAA(clip, eedi3Mode='cpu', nnedi3Mode='nnedi3', descale_strength=0.45, kernel='bicubic', bicubic_b=0.0, bicubic_c=1.0, descale_height=720)
    return atf.rfs(clip, insaneaaed, [[186,272],[316,378],[430,487],[573,603],[646,704],[751,1392]] )

def fix_edges(clip: vs.VideoNode) -> vs.VideoNode:
    return core.edgefixer.Continuity(clip, 2, 2, 2, 2)


source_file = r'.\udon_no_kuni_pv1.dgi'

src = open_source(source_file)

filter_chain = functoolz.compose(fix_edges, do_main_aa)

filtered = filter_chain(src)

filtered.set_output(0)
