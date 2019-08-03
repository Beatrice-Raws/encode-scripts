import sys
from pathlib import Path
sys.path.append(str(Path(".").resolve()))
from nekofunc import core, MainAA, DenoiseDebandMain, DenoiseDebandPV2, DenoiseDebandPV2_TOHO, at

core.max_cache_size = 18000
source = core.dgdecodenv.DGSource(r'.\..\index\PV2.dgi')
aaclip = MainAA(source)
native_res  = [[0, 35]]
captions    = [[76, 216], [313, 481], [502, 570], [649, 779], [808, 1072], [1080, 1142], [1150, 1219], [1227, 1308], [1314, 1393], [1401, 1485]]
mthr_30     = [[313, 481], [502, 570]]
watermark   = [[483, 1999]]
static_mask = [[2131, 2227]]
mask_1 = at.DiffRescaleMask(source, descale_h=848, mthr=40, kernel='spline36').std.Maximum().std.Inflate()
mask_2 = at.DiffRescaleMask(source, descale_h=848, mthr=30, kernel='spline36').std.Maximum().std.Inflate()
mask   = at.rfs(mask_1, mask_2, mthr_30)
clip = core.std.MaskedMerge(aaclip, source, mask)
clip = at.rfs(aaclip, clip, captions)
watermark_mask = at.ApplyImageMask(clip, source, r'.\masks\PV02\WATERMARK.png', preview=False)
copyright_mask = at.ApplyImageMask(clip, source, r'.\masks\PV02\COPYRIGHT.png', preview=False)
clip = at.rfs(clip, watermark_mask, watermark)
clip = at.rfs(clip, copyright_mask, static_mask)
clip = at.rfs(clip, source, native_res)
deb1 = DenoiseDebandPV2(clip)
deb2 = DenoiseDebandPV2_TOHO(clip)
clip = at.rfs(deb1, deb2, native_res)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()