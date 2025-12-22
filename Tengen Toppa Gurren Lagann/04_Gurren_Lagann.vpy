# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00003.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ep_ed_start = 32486
ep_ed_end = 34643

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

strong_AA = strong_AA(layer_error_fix)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1023 1051] [1085 1108] [1260 1276] [1545 1589] [2600 2650] [2992 3014] [3071 3164] [9448 9539] [15072 15190] 19043 19086 [29453 29867]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(layer_error_fix), mappings="[8571 8714] [25877 25916] [29450 29452]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(layer_error_fix), mappings="[256 371] [3069 3070]")
AA_clip = fvf.rfs(AA_clip, very_strong_AA(layer_error_fix), mappings="3068")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9137-9139.webp'), "[9137 9139]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9140-9142.webp'), "[9140 9142]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9143-9145.webp'), "[9143 9145]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9149-9151.webp'), "[9149 9151]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9152.webp'), "9152")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9153-9154.webp'), "[9153 9154]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9155-9157.webp'), "[9155 9157]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9158-9160.webp'), "[9158 9160]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9161-9163.webp'), "[9161 9163]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9164-9166.webp'), "[9164 9166]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9167-9169.webp'), "[9167 9169]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9170.webp'), "9170")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9171-9172.webp'), "[9171 9172]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9173-9175.webp'), "[9173 9175]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9176-9178.webp'), "[9176 9178]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\04_Gurren_Lagann_9179-9181.webp'), "[9179 9181]")

AA_clip = fvf.rfs(AA_clip, layer_error_fix, mappings="[3173 3309]")
AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[34900 35015]")

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
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [824 854] [1109 1139] [1191 1259] [1419 1422] [1888 1968] [2325 2409] [2478 2599] [2731 2755] [2789 2816] [3311 3488] [3632 3722] [3876 3993] [4166 4212] [4516 4587] [4647 5873] [6277 6647] [6792 6926] [6960 7037] [7122 7307] [7449 7565] [7870 7911] [7979 8152] [8220 8404] [8935 8996] [9135 9311] [9668 9751] [10024 10279] [11085 11195] [12167 12824] [13898 13963] [14265 15190] [15215 15778] [16694 16967] [18369 18611] [18660 18790] [18796 18826] [18940 18999] [19036 19159] [19980 20126] [20171 20493] [20565 21095] [21168 21283] [21356 21851] [22450 22496] [22549 22739] [22859 22953] [23192 23381] [23568 23603] [24393 24622] [25308 25522] [26066 26196] [26406 26518] [26650 27280] [27725 27824] [27860 28291] [28427 29015] [29452 32378] [34728 34809] [34824 35015]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 252] [372 501] [633 677] [761 823] [879 917] [1085 1108] [1417 1418] [1590 1615] [3489 3631] [3821 3875] [4361 4515] [4588 4646] [7425 7448] [8584 8714] [8997 9043] [9384 9447] [9942 10023] [18119 18177] [18793 18795] [19497 19557] [25035 25104] [26010 26065]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[2704 2730]")

for i in range(1436, 1537):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

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