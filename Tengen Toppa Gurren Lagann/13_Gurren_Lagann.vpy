# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00002.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ep_ed_start = 32490
ep_ed_end = 34647

# layer compositing errors fix
layer_error_fix = src.std.Trim(238, 238)
layer_error_fix = layer_error_fix.std.Crop(left=850, right=1020, top=580, bottom=450)
layer_error_fix = haf.Overlay(src, layer_error_fix, x=850, y=580)
layer_error_fix = fvf.rfs(src, layer_error_fix, mappings="[239 252]")

loaded_images = {}

ranges_to_load = [
    (639, 651),
    (661, 677),
    (687, 693)
]

for start, end in ranges_to_load:
    for i in range(start, end):
        path = rf'img_fix\09_Gurren_Lagann_{i}.webp'
        loaded_images[i] = core.imwri.Read(path)

for frame_num in loaded_images.keys():
    image_clip = loaded_images[frame_num]
    layer_error_fix = rfs_img(layer_error_fix, image_clip, [frame_num])

layer_error_fix2 = layer_error_fix.std.Trim(28629, 28629)
layer_error_fix2 = layer_error_fix2.std.Crop(left=50, right=1512, top=50, bottom=490)
layer_error_fix2 = haf.Overlay(layer_error_fix, layer_error_fix2, x=50, y=50)
layer_error_fix2 = fvf.rfs(layer_error_fix, layer_error_fix2, mappings="[28630 29042]")

layer_error_fix3 = layer_error_fix2.std.Trim(28755, 28755)
layer_error_fix3 = layer_error_fix3.std.Crop(left=1656, right=236, top=766, bottom=280)
layer_error_fix3 = haf.Overlay(layer_error_fix2, layer_error_fix3, x=1656, y=766)
layer_error_fix3 = fvf.rfs(layer_error_fix2, layer_error_fix3, mappings="[28756 28914]")

layer_error_fix = layer_error_fix3

# descale/rescale & AA
op_ed_AA_clip = op_ed_AA(layer_error_fix)
ep_AA_clip = main_AA(layer_error_fix, credit_mask=False)

AA_clip = core.std.Trim(op_ed_AA_clip, 0, 2157) + core.std.Trim(ep_AA_clip, 2158, ep_ed_start-1) + core.std.Trim(op_ed_AA_clip, ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

sangnom_AA = sangnom_AA(layer_error_fix)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1086 1109] [1260 1276] [1545 1598] 1749 [8349 8465] [13678 13857] [14470 14479] [14822 14837] [15128 15148] [16019 16132] 17840 [20008 20551] [32262 32298] [22362 22364] [22675 22754] [22839 22894] [23585 23592] 23750 [25179 25181] 27350 [28383 28549] [31129 31271] [31854 31891] [32032 32107] [32329 32331]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(layer_error_fix), mappings="[10753 10755] [14486 14565] [24056 24090] [32332 32393]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA, mappings="[256 371] 20676 21984 [22360 22361] 25178")
AA_clip = fvf.rfs(AA_clip, strong_AA(layer_error_fix), mappings="15548 21983 27349")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\13_Gurren_Lagann_11136-11159.webp'), "[11136 11159]")

for i in range(11160, 11176):
    mask_path = fr'masks\13_Gurren_Lagann_{i}.webp'
    AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, mask_path), str(i))

AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\13_Gurren_Lagann_11176-11179.webp'), "[11176 11179]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\13_Gurren_Lagann_11180-11182.webp'), "[11180 11182]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\13_Gurren_Lagann_11183-11185.webp'), "[11183 11185]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\13_Gurren_Lagann_11186-11188.webp'), "[11186 11188]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\13_Gurren_Lagann_11189-11191.webp'), "[11189 11191]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\13_Gurren_Lagann_11192-11194.webp'), "[11192 11194]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\13_Gurren_Lagann_11195-11196.webp'), "[11195 11196]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\13_Gurren_Lagann_11197.webp'), "11197")

for i in range(15887, 15978):
    mask_path = fr'masks\13_Gurren_Lagann_{i}.webp'
    AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, mask_path), str(i))

AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[763 879] [1110 1139] [8182 8277] [8356 8465] [21524 21650] [34871 35019]")

# denoise, deband & regrain
weakest_denoise_deband = denoise_deband(AA_clip, thSAD=32, thr=1.5, sigma=0.7)
weak_denoise_deband = denoise_deband(AA_clip, thSAD=65, thr=2.0, sigma=1.0)

main_denoise_deband = denoise_deband(AA_clip, thSAD=65, thr=3.5, sigma=1.4)
noise1 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, True, luma_scaling=6).grain(main_denoise_deband)
noise2 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, False, luma_scaling=6).grain(main_denoise_deband)
main_denoise_deband = core.std.Expr([noise1, noise2], 'x {strength} * y 1 {strength} - * +'.format(strength=0.5))

strong_denoise_deband = denoise_deband(AA_clip, thSAD=65, thr=5.0, sigma=1.6)
strong_denoise_deband = AddNoise.GAUSS((1.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(strong_denoise_deband)

very_strong_denoise_deband = denoise_deband_strong(AA_clip, thSAD=120, thr=8.0, sigma=2.0)
strongest_denoise_deband = denoise_deband_strongest(AA_clip, thSAD=120, thr=12.0, sigma=2.0)

simple_darkmask = core.fmtc.bitdepth(AA_clip, bits=8, dmode=9).std.Levels(min_in=0, max_in=40, min_out=0, max_out=255, planes=[0]).std.Invert().std.Levels(min_in=0, max_in=40, min_out=0, max_out=255, planes=[0]).std.Invert().fmtc.bitdepth(bits=16)

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[1423 1435] [1536 1538] 1544 [1628 1674] [31442 31487]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [696 726] [826 879] [1110 1139] [1187 1259] [1319 1391] [1399 1416] [1419 1422] [1539 1583] [1616 1627] [1884 1916] [1939 1992] [2166 2172] [13167 13213] [18598 18728] 19346 [19348 19354] [21775 22005] [21988 22005] [25300 25311] [25881 26093] [26266 26336] [26644 26787] [28051 28121] [28319 28401] [29801 29816] [31008 31009]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 501] [633 695] [763 825] [880 917] [1392 1398] [1417 1418] [1590 1615] [1675 1681] [2371 2389] [3070 3164] [3224 3287] [3406 3450] [5553 5671] [8174 8280] [8349 8465] [8582 8667] [9214 9253] [10622 10714] [11927 12275] [13363 13369] [13458 13511] [14888 15053] [15102 15148] [16856 16903] [16990 17135] [17834 17838] [18008 18091] [18729 18911] [20712 20763] [20828 21459] [21651 21774] [22006 22359] [22492 22526] [22616 22674] [22839 22894] [22965 23620] [24244 24314] [24336 24349] [25504 25623] [26448 26560] [30736 30794] [31129 31271] [31632 31853] [32108 32261] [32299 32393] [34933 34939]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[9254 9289] [17136 17452] [18320 18597] [19531 19595]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(main_denoise_deband, strongest_denoise_deband, simple_darkmask), mappings="[31854 31894]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(weak_denoise_deband, strong_denoise_deband, simple_darkmask), mappings="[32262 32298]")

for i in range(1436, 1535):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, r'masks\09_Gurren_Lagann_1535.webp'), "1535")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, very_strong_denoise_deband, r'masks\13_Gurren_Lagann_11198-11199.webp'), "[11198 11199]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strong_denoise_deband, r'masks\13_Gurren_Lagann_31272-31631.webp'), "[31272 31441] [31488 31631]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((3.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[17136 17452] [18320 18597] [19531 19595]")

### mask for [1421 1526]
mask_1421_1526 = core.imwri.Read(r'masks\02_Gurren_Lagann_1421.webp') + core.imwri.Read(r'masks\09_Gurren_Lagann_1526.webp')
mask_1421_1526 = ToRGB(mask_1421_1526, 1, 32)
mask_1421_1526 = core.rife.RIFE(mask_1421_1526, model=24, factor_num=105, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_1421_1526 = core.fmtc.bitdepth(mask_1421_1526, bits=16)
mask_1421_1526 = core.std.Trim(mask_1421_1526, 0, 104)
#
masked_1421_1526 = core.std.MaskedMerge(DD_clip.std.Trim(1421, 1526), main_denoise_deband.std.Trim(1421, 1526), mask_1421_1526, planes=[0,1,2], first_plane=True)

DD_clip = core.std.Trim(DD_clip, 0, 1420) + masked_1421_1526 + core.std.Trim(DD_clip, 1527, src.num_frames-1)

### mask for [1527 1535]
mask_1527_1535 = core.imwri.Read(r'masks\09_Gurren_Lagann_1527.webp') + core.imwri.Read(r'masks\10_Gurren_Lagann_1535.webp')
mask_1527_1535 = ToRGB(mask_1527_1535, 1, 32)
mask_1527_1535 = core.rife.RIFE(mask_1527_1535, model=24, factor_num=8, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_1527_1535 = core.fmtc.bitdepth(mask_1527_1535, bits=16)
mask_1527_1535 = core.std.Trim(mask_1527_1535, 0, 7)
#
masked_1527_1535 = core.std.MaskedMerge(DD_clip.std.Trim(1527, 1535), main_denoise_deband.std.Trim(1527, 1535), mask_1527_1535, planes=[0,1,2], first_plane=True)

DD_clip = core.std.Trim(DD_clip, 0, 1526) + masked_1527_1535 + core.std.Trim(DD_clip, 1536, src.num_frames-1)

final = depth(DD_clip, 10)

set_output(final)