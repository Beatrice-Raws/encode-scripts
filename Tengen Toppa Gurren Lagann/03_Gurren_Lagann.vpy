# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00002.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
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

# descale/rescale & AA
op_ed_AA_clip = op_ed_AA(layer_error_fix)
ep_AA_clip = main_AA(layer_error_fix, credit_mask=False)

AA_clip = core.std.Trim(op_ed_AA_clip, 0, 2157) + core.std.Trim(ep_AA_clip, 2158, ep_ed_start-1) + core.std.Trim(op_ed_AA_clip, ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1023 1051] [1085 1108] [1260 1276] [1545 1589] [5698 6401] [6527 6669] [6694 7196] [7279 7487] [7566 7872] [7888 8042] [8223 8616] [8833 9068] [9848 9997] [10184 10368] [10475 10973] [12749 12802] [13081 13199] [13498 13537] [13726 13789] [18440 18522] [20076 20079] [20471 20510] [20570 20638] [20727 20758] [21026 21067] [25842 26020] [26087 26124] [26575 26616]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(layer_error_fix), mappings="[8043 8173] 13871 20701")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(layer_error_fix), mappings="[256 371] [26085 26086]")
AA_clip = fvf.rfs(AA_clip, strong_AA(layer_error_fix), mappings="26084")
AA_clip = fvf.rfs(AA_clip, strong_AA(AA_clip), mappings="26084")
AA_clip = fvf.rfs(AA_clip, strong_AA(AA_clip), mappings="26084")

AA_clip = fvf.rfs(AA_clip, layer_error_fix, mappings="[4406 4543]")
AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[34890 35017]")

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
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [824 854] [1109 1139] [1191 1259] [1419 1422] [1888 1968] [2166 4399] [4544 5835] [8835 8851] [8893 9068] [10974 11286] [11658 11906] [12302 12481] [12905 12998] [13919 14067] [14217 14289] [14363 15127] [15370 16062] [16284 16542] [16796 17682] [17754 17878] [17980 18320] [18440 18840] [18965 20169] [20308 20350] [20371 20454] [20727 20798] [20906 20993] [21068 21118] [21200 21701] [21840 22442] [22653 22842] [23059 23077] [24063 25202] [25584 25637] [26282 26492] [26747 26842] [27071 27640] [28101 28477] [28478 28596] [28711 28823] [29311 29418] [31177 31402] [31462 32393] [34758 35017]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 252] [372 501] [633 677] [761 823] [879 917] [1085 1108] [1417 1418] [1590 1615] [9069 9072] [13790 13870] [17683 17753] [18321 18439] [20455 20470] [25842 25925] [29630 29634] [30929 31141]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[8174 8199] [10089 10090]")

for i in range(1436, 1537):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

DD_clip = fvf.ReplaceFrames(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\03_Gurren_Lagann_28383-28477.webp'), "[28383 28477]")

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