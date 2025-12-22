# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00000.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ep_ed_start = 32489
ep_ed_end = 34646

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

eedi_AA = eedi_AA(layer_error_fix)
sangnom_AA = sangnom_AA(layer_error_fix)
strong_AA = strong_AA(layer_error_fix)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1023 1051] [1085 1108] [1260 1276] [1545 1589] [9349 9467] [17794 17798] 22186 26548 [31061 31078] [31484 31493] [31538 31554]")
AA_clip = fvf.rfs(AA_clip, eedi_AA, mappings="2379 [4822 5048] 6673 [30111 30114] [30863 31005] [34866 34882]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA, mappings="[256 371] [8780 8782]")
AA_clip = fvf.rfs(AA_clip, strong_AA, mappings="[8776 8779]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\06_Gurren_Lagann_22177-22179.webp'), "[22177 22179]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\06_Gurren_Lagann_22180.webp'), "22180")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\06_Gurren_Lagann_22181.webp'), "22181")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\06_Gurren_Lagann_26543.webp'), "26543")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\06_Gurren_Lagann_26544.webp'), "26544")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\06_Gurren_Lagann_26545.webp'), "26545")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\06_Gurren_Lagann_26546.webp'), "26546")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\06_Gurren_Lagann_22182.webp'), "22182")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\06_Gurren_Lagann_22183.webp'), "22183")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\06_Gurren_Lagann_22184.webp'), "22184")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\06_Gurren_Lagann_26547.webp'), "26547")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, eedi_AA, r'masks\06_Gurren_Lagann_22185.webp'), "22185")

AA_clip = fvf.rfs(AA_clip, layer_error_fix, mappings="[2725 2862]")
AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[34883 35018]")

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
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [824 854] [1109 1139] [1191 1259] [1419 1422] [1888 1968] [2284 2378] [2608 2618] [2863 3397] [4776 5048] [5320 5480] [5541 5660] [5714 5749] [5821 5952] [6172 6254] [6530 6905] [6966 8775] [8860 8965] [9599 10105] [10728 11314] [12742 13210] [14063 14118] [14236 14977] [14985 15283] [15291 15496] [15504 15635] [15693 15842] [16555 17793] [17847 18026] [18587 19683] [19900 20904] [20942 21378] [21736 21842] [22016 22134] [23563 23783] [23804 23849] [23885 23943] [24265 24292] [24307 24329] [24390 24406] [24410 24426] [24475 24519] [24661 24683] [25168 25213] [25426 25533] [26083 26457] [27007 27172] [27431 27655] [28225 28260] [28477 28517] [28827 28850] [30001 30075] [30724 30791] [31154 31184] [31666 31702] [31845 31902]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 252] [372 501] [633 677] [761 823] [879 917] [1085 1108] [1417 1418] [1590 1615] [2394 2425] [4626 4642] [31271 31447] [31903 32010]")

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