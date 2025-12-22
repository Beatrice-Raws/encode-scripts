# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00001.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
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

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1086 1109] [1260 1276] [1545 1598] 1749 [2359 2381] [8954 8999] [9994 10106] [10418 10465] [11114 11257] [11562 11692] [14253 14323] [18209 18242] [21887 21993] [22870 22934] [23539 23540]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(layer_error_fix), mappings="16472 [16474 16476] 23538 [28343 28355]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(layer_error_fix), mappings="[256 371] 15201 23537")
AA_clip = fvf.rfs(AA_clip, strong_AA(layer_error_fix), mappings="[15176 15200] 23536")
AA_clip = fvf.rfs(AA_clip, very_strong_AA(layer_error_fix), mappings="23535")

AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[763 879] [1110 1139] [15615 15679] [34872 35017]")

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

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[1423 1435] [1536 1538] 1544 [1628 1674]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [696 726] [826 879] [1110 1139] [1187 1259] [1319 1391] [1399 1416] [1419 1422] [1539 1583] [1616 1627] [1884 1916] [1939 1992] [2166 2172] [2508 2598] [2808 2809] [2834 2877] [13164 13372] [13414 13461] [13762 13815] [15070 15128] [15680 16183] [17461 17497] [17863 17961] [21488 21571] [21887 21993] [26996 27133] [29994 29998]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 501] [633 695] [763 825] [880 917] [1392 1398] [1417 1418] [1590 1615] [1675 1681] [2261 2298] [2599 2641] [3609 3679] [3749 3861] [9456 9520] [9556 9993] [10567 11005] [11036 11076] [11258 11561] [11693 11827] [11882 12117] [12156 12985] [13057 13163] [13830 13833] [13870 13873] [15271 15389] [16459 16468] [16489 16489] [17458 17459] [18670 18921] [19381 19529] [19932 20002] [23862 23872] [23922 23951] [23990 24021] [24130 24182] [24273 24429] [24485 24491] [25120 25229] [25473 25549] [26639 26685] [27134 27165] [28390 28531] [28746 28840] [29012 29055] [30201 30283] [32113 32212] [34814 34822]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[2466 2477] [20417 20739] [29056 29151]")

for i in range(1436, 1535):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, r'masks\09_Gurren_Lagann_1535.webp'), "1535")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, r'masks\12_Gurren_Lagann_3502-3550.webp'), "[3502 3513]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strongest_denoise_deband, r'masks\12_Gurren_Lagann_3502-3550.webp'), "[3514 3550]")

for i in range(3551, 3556):
    mask_path = fr'masks\12_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strongest_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strongest_denoise_deband, r'masks\12_Gurren_Lagann_3556.webp'), "[3556 3572] [3575 3596] [3599 3608]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strongest_denoise_deband, r'masks\12_Gurren_Lagann_3573.webp'), "3573 3574 3597 3598")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, denoise_deband_strongest(AA_clip, thSAD=120, thr=7.0, sigma=2.0), r'masks\12_Gurren_Lagann_18582-18614.webp'), "[18582 18614]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, denoise_deband_strongest(AA_clip, thSAD=120, thr=5.0, sigma=2.0), r'masks\12_Gurren_Lagann_18615-18628.webp'), "[18615 18628]")

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