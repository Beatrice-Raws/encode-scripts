# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00008.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
nced_02 = depth(src,16).std.Trim(24, src.num_frames-1)

layer_error_fix = nced_02.std.Trim(1763, 1763)
layer_error_fix = layer_error_fix.std.Crop(left=100, right=1720, top=0, bottom=1048)
layer_error_fix = haf.Overlay(nced_02, layer_error_fix, x=0, y=0)
layer_error_fix = fvf.rfs(nced_02, layer_error_fix, mappings="[1298 1304]")

layer_error_fix2 = layer_error_fix.std.Trim(1763, 1763)
layer_error_fix2 = layer_error_fix2.std.Crop(left=720, right=1000, top=0, bottom=1020)
layer_error_fix2 = haf.Overlay(layer_error_fix, layer_error_fix2, x=0, y=0)
layer_error_fix2 = fvf.rfs(layer_error_fix, layer_error_fix2, mappings="[1764 1790]")

layer_error_fix3 = layer_error_fix2.std.Trim(1763, 1763)
layer_error_fix3 = layer_error_fix3.std.Crop(left=720, right=1000, top=0, bottom=1020)
layer_error_fix3 = haf.Overlay(layer_error_fix2, layer_error_fix3, x=1720, y=0)
layer_error_fix3 = fvf.rfs(layer_error_fix2, layer_error_fix3, mappings="[1764 1790]")

layer_error_fix4 = layer_error_fix3.std.Trim(1777, 1777)
layer_error_fix4 = layer_error_fix4.std.Crop(left=0, right=0, top=1044, bottom=0)
layer_error_fix4 = haf.Overlay(layer_error_fix3, layer_error_fix4, x=0, y=1044)
layer_error_fix4 = fvf.rfs(layer_error_fix3, layer_error_fix4, mappings="[1778 1785]")

layer_error_fix5 = layer_error_fix4.std.Trim(1785, 1785)
layer_error_fix5 = layer_error_fix5.std.Crop(left=0, right=0, top=1010, bottom=0)
layer_error_fix5 = haf.Overlay(layer_error_fix4, layer_error_fix5, x=0, y=1010)
layer_error_fix5 = fvf.rfs(layer_error_fix4, layer_error_fix5, mappings="[1786 1790]")

nced_AA_clip = main_AA(layer_error_fix5, credit_mask=False)
weakest_nneedi3_AA = weakest_nneedi3_AA(layer_error_fix5)
weak_sangnom_sd_AA = DescaleTarget(width=854, height=480, kernel=Lanczos(3), do_post_descale=dehalo, do_post_double=sangnom, downscaler=Hermite(linear=True), credit_mask=False).get_upscaled(layer_error_fix5)
eedi_sd_AA = DescaleTarget(width=854, height=480, kernel=Lanczos(3), do_post_descale=eedi, downscaler=Hermite(linear=True), credit_mask=False).get_upscaled(layer_error_fix5)

nced_AA_clip = fvf.rfs(nced_AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(layer_error_fix5), mappings="[86 116] [174 201] [1227 1304]")
nced_AA_clip = fvf.rfs(nced_AA_clip, weakest_nnedi3_AA(layer_error_fix5), mappings="[86 116] [551 955] [1010 1048] [1084 1226] [1305 1416] [1552 1660] [1739 1897] [1950 2158]")
nced_AA_clip = fvf.rfs(nced_AA_clip, weakest_nneedi3_AA, mappings="[393 453] [523 550] [1417 1436] [1494 1551] [1661 1738] [1898 1949]")
nced_AA_clip = fvf.rfs(nced_AA_clip, weak_eedi_AA(layer_error_fix5), mappings="[35 52] [69 85] [378 392] [454 477]")
nced_AA_clip = fvf.rfs(nced_AA_clip, eedi_AA(layer_error_fix5), mappings="[32 34] [53 68] [356 377]")
nced_AA_clip = fvf.rfs(nced_AA_clip, eedi_sd_AA, mappings="[327 355]")
nced_AA_clip = fvf.rfs(nced_AA_clip, weak_sangnom_AA(layer_error_fix5), mappings="[478 522] [956 1009]")
nced_AA_clip = fvf.rfs(nced_AA_clip, weak_sangnom_sd_AA, mappings="[13 31] [117 173]")
nced_AA_clip = fvf.rfs(nced_AA_clip, ApplyImageMask(layer_error_fix5, weakest_nneedi3_AA, r'masks\16_Gurren_Lagann_33924-33980.webp'), "[1437 1493]")
nced_AA_clip = depth(src,16).std.Trim(0, 23) + nced_AA_clip

# denoise, deband & regrain
main_denoise_deband = denoise_deband(nced_AA_clip, thSAD=65, thr=3.5, sigma=1.4)
noise1 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, True, luma_scaling=6).grain(main_denoise_deband)
noise2 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, False, luma_scaling=6).grain(main_denoise_deband)
main_denoise_deband = core.std.Expr([noise1, noise2], 'x {strength} * y 1 {strength} - * +'.format(strength=0.5))

DD_clip = main_denoise_deband

set_output(DD_clip)