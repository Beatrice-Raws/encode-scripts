import sys
from pathlib import Path
sys.path.append(str(Path(".").resolve()))
from nekofunc import core, MainAA, DenoiseDebandMain, DenoiseDebandStronger, at

core.max_cache_size = 18000

source = core.dgdecodenv.DGSource(r'.\..\index\PV1.dgi')
aaclip = MainAA(source)
captions  = [[39, 170], [320, 429], [474, 539], [548, 637], [772, 835], [845, 929], [1266, 1394]]
end_title = [[1400, 1679]]
stronger_deband = [[0, 96], [176, 213], [469, 495], [544, 570], [642, 668], [729, 761], [766, 786], [934, 965], [1004, 1029], [1132, 1214], [1236, 1285], [1368, 1394]]
mask = at.DiffRescaleMask(source, descale_h=848, mthr=30, kernel='spline36').std.Maximum().std.Inflate()
clip = core.std.MaskedMerge(aaclip, source, mask)
clip = at.rfs(aaclip, clip, captions)
clip = at.rfs(clip, source, end_title)
deb1 = DenoiseDebandMain(clip)
deb2 = DenoiseDebandStronger(clip)
clip = at.rfs(deb1, deb2, stronger_deband)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()