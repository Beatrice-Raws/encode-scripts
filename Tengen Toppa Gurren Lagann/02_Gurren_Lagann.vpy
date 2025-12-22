# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# specifies the processor thread numbers to use
import psutil
p_handle = psutil.Process()
p_handle.cpu_affinity([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26])
core.num_threads = 14

# load source with the required properties
src = core.bs.VideoSource(r'00001.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
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

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1023 1051] [1085 1108] [1260 1276] [1545 1589] [5277 5278] [5563 5598] [12533 12586] [17498 17682] [19016 19085] [20892 20955] [22197 22241] [22749 22867] [27147 27201] [27225 27428] [34728 34789]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(layer_error_fix), mappings="22207 22209 [22969 22985] [24748 24787] 25626 [26503 26504] [26963 26982] [27058 27122] [28528 28574]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(layer_error_fix), mappings="[256 371] [4564 4565] 5119 5276 [6198 6225] 13115 17683 [19086 19150] [24291 24306] [24460 24461] 24747 25625 [26501 26502]")
AA_clip = fvf.rfs(AA_clip, strong_AA(layer_error_fix), mappings="2510 4566 5275 [18987 19009] [19151 19185] [24307 24312] 25624")
AA_clip = fvf.rfs(AA_clip, very_strong_AA(layer_error_fix), mappings="2509 [19186 19370]")

AA_clip = fvf.rfs(AA_clip, layer_error_fix, mappings="[2812 2925]")
AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[34886 35015]")

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[1023 1084] [1423 1435] 1544")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [824 854] [1109 1139] [1191 1259] [1419 1422] [1888 1968] [2390 2414] [2431 2495] [2600 2606] [2926 2990] [3890 3931] [4143 4330] [4353 4441] [5629 5673] [5721 5813] [7525 7753] [7813 8048] [8474 8570] [8673 8851] [8995 9113] [11903 12054] [12695 12861] [13115 14110] [14493 14599] [14761 15918] [16159 17159] [17321 17462] [17743 18986] [19371 19539] [19683 20238] [20394 20518] [21117 21269] [21331 21966] [22226 22240] [22281 22461] [22749 22867] [23035 23102] [23605 23766] [24531 24631] [25475 25534] [27442 27459] [27732 27735] [28464 28657] [30868 32151] [34856 34934]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 252] [372 501] [633 677] [761 823] [879 917] [1085 1108] [1417 1418] [1590 1615] [2371 2389] [2415 2430] [3687 3889] [4628 4719] [5243 5274] [5862 6094] [7127 7173] [7754 7812] [20271 20342] [20835 21015] [21270 21282] [22242 22280] [23514 23534] [23767 23969] [27147 27236] [27412 27428] [27460 27630] [28256 28331] [34755 34789]")

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