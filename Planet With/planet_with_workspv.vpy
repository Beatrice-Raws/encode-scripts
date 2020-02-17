import vapoursynth as vs
from toolz import functoolz

core = vs.core
core.max_cache_size = 24576

def open_source(path: str) -> vs.VideoNode:
    return core.dgdecodenv.DGSource(path)


source_file = r'.\planet_with_pv.dgi'

src = open_source(source_file).std.Trim(2692,4875)

src.set_output(0)
