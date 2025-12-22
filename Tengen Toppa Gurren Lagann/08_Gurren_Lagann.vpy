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

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1023 1051] [1085 1108] [1260 1276] [1545 1589] [14001 14071] [16211 16243] [18004 18068] [20328 20367] [22070 22085] [23017 23053] [23188 23250] [31071 31212] [32072 32113]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(layer_error_fix), mappings="[3496 3503] 16210 [17643 17697] [17700 17702] [18971 19167] [22116 22136] [22169 22185] [22508 22661] [24432 24467] [24527 24596] [28360 28442]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(layer_error_fix), mappings="[256 371] 2505 15074 17601 17699 [31067 31070]")
AA_clip = fvf.rfs(AA_clip, strong_AA(layer_error_fix), mappings="[15072 15073] 16209 17600 17698 [31063 31066]")

AA_clip = fvf.rfs(AA_clip, layer_error_fix, mappings="[32376 32489]")
AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[34909 35019]")

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
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [824 854] [1109 1139] [1191 1259] [1419 1422] [1888 1968] [2434 2463] [2591 2643] [2673 2720] [3147 3469] [3504 3568] [3713 5242] [5287 7395] [7881 8545] [8566 8643] [8722 8802] [8839 8889] [8959 8975] [9238 9776] [10152 10462] [10522 10575] [10642 11252] [12254 12306] [12809 12970] [13211 13270] [13402 13527] [13605 13759] [14238 14273] [14292 14522] [14550 14628] [14732 14814] [15185 15236] [15300 15451] [15508 15626] [15744 15876] [16578 16844] [17103 17130] [17600 17642] [17839 17919] [18004 18068] [18108 18240] [18372 18395] [18486 18644] [18864 18970] [19288 19478] [19580 19693] [19802 19831] [20328 20462] [20467 20467] [20473 20521] [21885 22136] [22426 22455] [22485 22507] [23751 23807] [24009 24062] [24468 24526] [24648 24823] [25203 25623] [25708 25807] [26034 26250] [26352 26422] [26815 26939] [27140 27434] [28443 28529] [29184 29400] [29552 29877] [29923 29927] [30071 30476] [31068 31326] [31776 31947] [32031 32071] [34856 34861]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 252] [372 501] [633 677] [761 823] [879 917] [1085 1108] [1417 1418] [1590 1615] [2220 2225] [2357 2413] [2505 2506] [14815 15131] [16052 16064] [16181 16210] [16527 16539] [20167 20327] [22662 22724] [28865 28866] [28868 29013] [30477 30528] [30640 30642] [30656 30657]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[2203 2219]")

for i in range(1436, 1537):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

for i in range(18855, 18864):
    mask_path = fr'masks\08_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_denoise_deband, mask_path), str(i))

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