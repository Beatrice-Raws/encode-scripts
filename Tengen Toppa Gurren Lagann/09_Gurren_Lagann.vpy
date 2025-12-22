# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00003.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ep_ed_start = 32488
ep_ed_end = 34645

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

# descale/rescale & AA
op_ed_AA_clip = op_ed_AA(layer_error_fix)
ep_AA_clip = main_AA(layer_error_fix, credit_mask=False)

AA_clip = core.std.Trim(op_ed_AA_clip, 0, 2157) + core.std.Trim(ep_AA_clip, 2158, ep_ed_start-1) + core.std.Trim(op_ed_AA_clip, ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

eedi_AA = eedi_AA(layer_error_fix)
sangnom_AA = sangnom_AA(layer_error_fix)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1023 1051] [1085 1108] [1260 1276] [1545 1598] 1749")
AA_clip = fvf.rfs(AA_clip, eedi_AA, mappings="[7750 7808] 31247 [34897 34912]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA, mappings="[256 371] 34882")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(eedi_AA, sangnom_AA, r'masks\09_Gurren_Lagann_11850-11858.webp'), "[11850 11858]")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(eedi_AA, sangnom_AA, r'masks\09_Gurren_Lagann_11859-11861.webp'), "[11859 11861]")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(eedi_AA, sangnom_AA, r'masks\09_Gurren_Lagann_11862-11864.webp'), "[11862 11864]")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(eedi_AA, sangnom_AA, r'masks\09_Gurren_Lagann_11865-11867.webp'), "[11865 11867]")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(eedi_AA, sangnom_AA, r'masks\09_Gurren_Lagann_11868-11962.webp'), "[11868 11962]")

for i in range(11963, 11988):
    mask_path = fr'masks\09_Gurren_Lagann_{i}.webp'
    AA_clip = fvf.rfs(AA_clip, ApplyImageMask(eedi_AA, sangnom_AA, mask_path), str(i))

AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(eedi_AA, sangnom_AA, r'masks\09_Gurren_Lagann_11988-12026.webp'), "[11988 12026]")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(eedi_AA, sangnom_AA, r'masks\09_Gurren_Lagann_12027-12034.webp'), "[12027 12034]")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25270.webp'), "25270")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25271.webp'), "25271")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25272.webp'), "25272")

for i in range(25279, 25324):
    mask_path = fr'masks\09_Gurren_Lagann_{i}.webp'
    AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, mask_path), str(i))

AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25324-25326.webp'), "25324")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25325.webp'), "25325")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25324-25326.webp'), "25326")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25327-25329.webp'), "25327")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25328.webp'), "25328")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25327-25329.webp'), "25329")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25330-25332.webp'), "25330")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25331.webp'), "25331")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25330-25332.webp'), "25332")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25333-25335.webp'), "25333")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25334.webp'), "25334")
AA_clip = fvf.ReplaceFrames(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\09_Gurren_Lagann_25333-25335.webp'), "25335")
AA_clip =  fvf.ReplaceFrames(AA_clip, strong_AA(layer_error_fix), mappings="31246")
AA_clip =  fvf.ReplaceFrames(AA_clip, strongest_AA(layer_error_fix), mappings="16247 34881")

AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[763 879] [1110 1139] [2870 2965] [2971 3062] [3151 3229] [3235 3480] [3486 3623] [34913 35017]")

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

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[1423 1435] [1536 1538] 1544 [1628 1674] [2171 2184]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [696 726] [826 879] [1110 1139] [1187 1259] [1319 1391] [1399 1416] [1419 1422] [1539 1583] [1616 1627] [1884 1916] [1939 1992] [2185 2221] [2758 3062] [5852 6153] [6387 6504] [6958 7110] [7636 7706] [7809 7867] [11263 11381] [11424 11849] [14385 14694] [15021 15147] [15595 15864] [15983 16025] [16498 16636] [16879 16940] [17337 18149] [18521 18702] [18810 19729] [19754 19861] [20273 20599] [20877 20985] [21282 21400] [21520 21578] [21997 22162] [24687 24741] [24786 24829] [25079 25245] [25288 25335] [25475 25725] [25872 26807] [31493 31625]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 252] [372 501] [633 677] [761 823] [879 917] [1085 1108] [1417 1418] [1590 1615] [1675 1681] [4466 4750] [5283 5464] [6291 6321] [6638 6726] [7707 7749] [8930 9024] [9435 9517] [9925 10282] [10736 11050] [11382 11423] [12035 12117] [12291 12483] [12656 13098] [13533 13971] [14695 14867] [15247 15248] [16475 16497] [20986 21063] [22609 22667] [27992 28038] [29747 30045] [30536 30589] [30662 30771] [31970 32236] [34883 34896]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[11850 12034] [13099 13361] [22881 22981]")

for i in range(1436, 1537):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

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