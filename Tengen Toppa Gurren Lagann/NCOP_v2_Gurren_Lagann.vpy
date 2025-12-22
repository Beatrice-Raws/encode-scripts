# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
ncop_v2 = core.bs.VideoSource(r'00007.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
ncop_v2 = depth(ncop_v2,16)

# layer compositing errors fix
layer_error_fix = ncop_v2.std.Trim(238, 238)
layer_error_fix = layer_error_fix.std.Crop(left=850, right=1020, top=580, bottom=450)
layer_error_fix = haf.Overlay(ncop_v2, layer_error_fix, x=850, y=580)
layer_error_fix = fvf.rfs(ncop_v2, layer_error_fix, mappings="[239 252]")

loaded_images = {}

ranges_to_load = [
    (639, 651),
    (661, 677),
    (687, 693)
]

for start, end in ranges_to_load:
    for i in range(start, end):
        path = rf'img_fix\09_Gurren_Lagann_{i}_nc.webp'
        loaded_images[i] = core.imwri.Read(path)

for frame_num in loaded_images.keys():
    image_clip = loaded_images[frame_num]
    layer_error_fix = rfs_img(layer_error_fix, image_clip, [frame_num])

# descale/rescale & AA
AA_clip = DescaleTarget(width=1280, height=720, kernel=Bilinear, do_post_descale=dehalo, downscaler=Hermite(linear=True), credit_mask=False).get_upscaled(layer_error_fix)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1023 1051] [1085 1108] [1260 1276] [1545 1598] 1749")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(layer_error_fix), mappings="[256 371]")

AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=False), mappings="[763 879] [1110 1139]")

# denoise, deband & regrain
weakest_denoise_deband = denoise_deband(AA_clip, thSAD=32, thr=1.5, sigma=0.7)
weak_denoise_deband = denoise_deband(AA_clip, thSAD=65, thr=2.0, sigma=1.0)

main_denoise_deband = denoise_deband(AA_clip, thSAD=65, thr=3.5, sigma=1.4)
noise1 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, True, luma_scaling=6).grain(main_denoise_deband)
noise2 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, False, luma_scaling=6).grain(main_denoise_deband)
main_denoise_deband = core.std.Expr([noise1, noise2], 'x {strength} * y 1 {strength} - * +'.format(strength=0.5))

strong_denoise_deband = denoise_deband(AA_clip, thSAD=65, thr=5.0, sigma=1.6)
strong_denoise_deband = AddNoise.GAUSS((1.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(strong_denoise_deband)

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[1423 1435] [1536 1538] 1544 [1628 1674]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [696 726] [826 879] [1110 1139] [1187 1259] [1319 1391] [1399 1416] [1419 1422] [1539 1583] [1616 1627] [1884 1916] [1939 1992]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 252] [372 501] [633 677] [761 823] [879 917] [1085 1108] [1417 1418] [1590 1615] [1675 1681]")

for i in range(1436, 1536):
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

DD_clip = core.std.Trim(DD_clip, 0, 1420) + masked_1421_1526 + core.std.Trim(DD_clip, 1527, ncop_v2.num_frames-1)

### mask for [1527 1535]
mask_1527_1535 = core.imwri.Read(r'masks\09_Gurren_Lagann_1527.webp') + core.imwri.Read(r'masks\10_Gurren_Lagann_1535.webp')
mask_1527_1535 = ToRGB(mask_1527_1535, 1, 32)
mask_1527_1535 = core.rife.RIFE(mask_1527_1535, model=24, factor_num=8, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_1527_1535 = core.fmtc.bitdepth(mask_1527_1535, bits=16)
mask_1527_1535 = core.std.Trim(mask_1527_1535, 0, 7)
#
masked_1527_1535 = core.std.MaskedMerge(DD_clip.std.Trim(1527, 1535), main_denoise_deband.std.Trim(1527, 1535), mask_1527_1535, planes=[0,1,2], first_plane=True)

DD_clip = core.std.Trim(DD_clip, 0, 1526) + masked_1527_1535 + core.std.Trim(DD_clip, 1536, ncop_v2.num_frames-1)

final = depth(DD_clip, 10)

set_output(final)