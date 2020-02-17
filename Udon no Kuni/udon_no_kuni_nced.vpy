import vapoursynth as vs
import atomchtools as atf
import mvsfunc as mvf
import insaneAA
import HardAAp2 as HardAA
from functools import reduce
from toolz import functoolz

core = vs.core
core.max_cache_size = 18432

def open_source(path: str) -> vs.VideoNode:
    return core.dgdecodenv.DGSource(path)

def do_main_aa(clip: vs.VideoNode) -> vs.VideoNode:
    return insaneAA.insaneAA(clip, eedi3Mode='cpu', nnedi3Mode='nnedi3', descale_strength=0.45, kernel='bicubic', bicubic_b=0.0, bicubic_c=1.0, descale_height=720)

@functoolz.curry
def do_stars_aa(clip: vs.VideoNode, source: vs.VideoNode) -> vs.VideoNode:
    diff_mask_frames = [[1169,1296], [1297,1299], [1300,1302], [1303,1305], [1306,1308], [1309,1311], [1312,1314], [1315,1317], [1318,1320], [1321,1323], [1324,1430]]
    diff_mask_clips = [atf.DiffOn2FramesMask(source, f1, f2) for [f1, f2] in diff_mask_frames]
    diff_mask = reduce(lambda c1, c2: mvf.Max(c1, c2, mode=1), diff_mask_clips).std.Binarize(35)

    desc = insaneAA.revert_upscale(clip, kernel='bicubic', bicubic_b=0, bicubic_c=1, descale_height=720, descale_strength=0.45)
    hardaa =  HardAA.HardAA(desc, mask=None, nrad=2, alpha=0.9, beta=0.1, gamma=5)
    appliedaa = core.std.MaskedMerge(desc, hardaa, diff_mask.resize.Spline36(1280,720))
    rescaledaa = insaneAA.rescale(appliedaa, eedi3Mode='cpu', nnedi3Mode='nnedi3', dx=1920, dy=1080)
    return atf.rfs(clip, core.std.MaskedMerge(clip, rescaledaa, diff_mask, planes=[0], first_plane=True), [[1169,1430]])

def fix_edges(clip: vs.VideoNode) -> vs.VideoNode:
    return core.edgefixer.Continuity(clip, 2, 2, 2, 2)

source_file = r'.\udon_no_kuni_nced.dgi'

src = open_source(source_file)

filter_chain = functoolz.compose(fix_edges, do_stars_aa(source=src), do_main_aa)

filtered = filter_chain(src)

filtered.set_output(0)
