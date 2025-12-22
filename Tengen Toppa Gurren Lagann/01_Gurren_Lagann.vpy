# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00000.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ep_ed_start = 34645
ep_ed_end = 36802

# layer compositing errors fix
layer_error_fix = src.std.Trim(238, 238)
layer_error_fix = layer_error_fix.std.Crop(left=850, right=1020, top=580, bottom=450)
layer_error_fix = haf.Overlay(src, layer_error_fix, x=850, y=580)
layer_error_fix = fvf.rfs(src, layer_error_fix, mappings="[239 252]")

loaded_images = {}

ranges_to_load = [
    (767, 779),
    (789, 805),
    (815, 821)
]

for start, end in ranges_to_load:
    for i in range(start, end):
        path = rf'img_fix\01_Gurren_Lagann_{i}.webp'
        loaded_images[i] = core.imwri.Read(path)

for frame_num in loaded_images.keys():
    image_clip = loaded_images[frame_num]
    layer_error_fix = rfs_img(layer_error_fix, image_clip, [frame_num])

img_fix_16026_16097 = core.imwri.Read(r'img_fix\01_Gurren_Lagann_16030.webp')

layer_error_fix = rfs_img(layer_error_fix, img_fix_16026_16097, [16026, 16027, 16028, 16029, 16030, 16038, 16039, 16040, 16056, 16057, 16058, 16062, 16063, 16064, 16074, 16075, 16076, 16083, 16084, 16085, 16089, 16090, 16091, 16095, 16096, 16097])

# descale/rescale & AA
op_ed_AA_clip = op_ed_AA(layer_error_fix)
ep_AA_clip = main_AA(layer_error_fix, credit_mask=False)

AA_clip = core.std.Trim(op_ed_AA_clip, 0, 2157) + core.std.Trim(ep_AA_clip, 2158, ep_ed_start-1) + core.std.Trim(op_ed_AA_clip, ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1023 1051] [1085 1108] [1260 1276] [1545 1589] [5728 5878] [7615 7618] [19442 19554] [26194 26319] [28122 28228] [30726 30756] [30834 31017] [37024 37040]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(layer_error_fix), mappings="[256 371] [4128 4254] [5642 5643] 7372 7614 [7695 7696] [8105 8139] [8142 8143] [14094 14108] [19555 19597] 19874 [24503 24535] [27268 27269] 27570 [29066 29068] 30637 32246")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(AA_clip), mappings="27268")
AA_clip = fvf.rfs(AA_clip, strong_AA(layer_error_fix), mappings="7371 7613 [7693 7694] [8140 8141] [9690 9691] [14085 14093] [19598 19599] 19873 24502 [25662 25671] [28631 28632]")
AA_clip = fvf.rfs(AA_clip, very_strong_AA(layer_error_fix), mappings="7370 19872 [27266 27267] 27569 [29064 29065] 30636")
AA_clip = fvf.rfs(AA_clip, very_strong_AA(AA_clip), mappings="27266 29064")
AA_clip = fvf.rfs(AA_clip, strongest_AA(layer_error_fix), mappings="27265 27568 [29062 29063]")
AA_clip = fvf.rfs(AA_clip, strongest_AA(AA_clip), mappings="[29062 29063]")

AA_clip = fvf.rfs(AA_clip, layer_error_fix, mappings="[4261 4398]")
AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[37041 37174]")

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[1023 1084] [1423 1435] 1544")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [824 854] [1109 1139] [1191 1259] [1419 1422] [1888 1968] [3714 4081] [4638 4993] [5154 5277] [7370 7612] [9535 9689] [10017 10315] [11649 11701] [13110 13492] [14333 14750] [15098 15330] [17727 17812] [20654 20843] [21131 21326] [21740 22088] [22486 22646] [25960 25994] [30674 30725] [30826 31409] [31963 32010] [32246 32364]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 252] [372 501] [633 677] [761 823] [879 917] [1085 1108] [1417 1418] [1590 1615] [5278 5549] [6218 6337] [6934 7059] [7681 7826] [8068 8200] [8271 8333] [9235 9243] [10912 11485] [12069 12139] [12187 12281] [13050 13109] [13924 13953] [14152 14243] [15002 15097] [15746 16105] [16185 16253] [16297 16369] [18414 18465] [19030 19105] [27386 27567] [28887 28988] 30276 [31553 31936] [32015 32045] [32690 33480] [33698 33722] [33926 34133] [34306 34379]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[5550 5641] [6338 6477] [7233 7369] [10805 10911] [15331 15510] [15516 15538] [16106 16184] [16254 16296] [25662 25671] [29168 29236] [32214 32245]")

for i in range(1436, 1537):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, DFTTest(tr=0).denoise(DD_clip), r'masks\01_Gurren_Lagann_14751-14845.webp'), "[14751 14845]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, denoise_deband_strong(DD_clip, thSAD=120, thr=8.0, sigma=2.0), r'masks\01_Gurren_Lagann_14751-14845.webp'), "[14751 14845]")

for i in range(20844, 20970):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[5550 5641] [14751 14845]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[15331 15510] [15516 15537]")

### mask for [1421 1535]
mask_1421_1535 = core.imwri.Read(r'masks\02_Gurren_Lagann_1421.webp') + core.imwri.Read(r'masks\02_Gurren_Lagann_1535.webp')
mask_1421_1535 = ToRGB(mask_1421_1535, 1, 32)
mask_1421_1535 = core.rife.RIFE(mask_1421_1535, model=24, factor_num=114, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_1421_1535 = core.fmtc.bitdepth(mask_1421_1535, bits=16)
mask_1421_1535 = core.std.Trim(mask_1421_1535, 0, 113)
#
masked_1421_1535 = core.std.MaskedMerge(DD_clip.std.Trim(1421, 1535), main_denoise_deband.std.Trim(1421, 1535), mask_1421_1535, planes=[0,1,2], first_plane=True)

DD_clip = core.std.Trim(DD_clip, 0, 1420) + masked_1421_1535 + core.std.Trim(DD_clip, 1536, src.num_frames-1)

final = depth(DD_clip, 10)

set_output(final)