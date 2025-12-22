# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00005.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)

ep_ed_start = 32487
ep_ed_end = 34645

ep_ed = core.std.Trim(src, ep_ed_start, ep_ed_end)

src = depth(src,16)

nced = core.bs.VideoSource(r'00008.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1).std.Trim(24, 2182)

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

layer_error_fix2 = layer_error_fix.std.Trim(34250, 34250)
layer_error_fix2 = layer_error_fix2.std.Crop(left=100, right=1720, top=0, bottom=1048)
layer_error_fix2 = haf.Overlay(layer_error_fix, layer_error_fix2, x=0, y=0)
layer_error_fix2 = fvf.rfs(layer_error_fix, layer_error_fix2, mappings="[33785 33791]")

layer_error_fix3 = layer_error_fix2.std.Trim(34250, 34250)
layer_error_fix3 = layer_error_fix3.std.Crop(left=720, right=1000, top=0, bottom=1020)
layer_error_fix3 = haf.Overlay(layer_error_fix2, layer_error_fix3, x=0, y=0)
layer_error_fix3 = fvf.rfs(layer_error_fix2, layer_error_fix3, mappings="[34251 34277]")

layer_error_fix4 = layer_error_fix3.std.Trim(34250, 34250)
layer_error_fix4 = layer_error_fix4.std.Crop(left=720, right=1000, top=0, bottom=1020)
layer_error_fix4 = haf.Overlay(layer_error_fix3, layer_error_fix4, x=1720, y=0)
layer_error_fix4 = fvf.rfs(layer_error_fix3, layer_error_fix4, mappings="[34251 34277]")

layer_error_fix5 = layer_error_fix4.std.Trim(34264, 34264)
layer_error_fix5 = layer_error_fix5.std.Crop(left=0, right=0, top=1044, bottom=0)
layer_error_fix5 = haf.Overlay(layer_error_fix4, layer_error_fix5, x=0, y=1044)
layer_error_fix5 = fvf.rfs(layer_error_fix4, layer_error_fix5, mappings="[34265 34272]")

layer_error_fix6 = layer_error_fix5.std.Trim(34272, 34272)
layer_error_fix6 = layer_error_fix6.std.Crop(left=0, right=0, top=1010, bottom=0)
layer_error_fix6 = haf.Overlay(layer_error_fix5, layer_error_fix6, x=0, y=1010)
layer_error_fix6 = fvf.rfs(layer_error_fix5, layer_error_fix6, mappings="[34273 34277]")

layer_error_fix = layer_error_fix6

# descale/rescale & AA
op_ed_AA_clip = op_ed_AA(layer_error_fix)
ep_AA_clip = main_AA(layer_error_fix, credit_mask=False)

AA_clip = core.std.Trim(op_ed_AA_clip, 0, 2157) + core.std.Trim(ep_AA_clip, 2158, src.num_frames-1)

weakest_nneedi3_AA = weakest_nneedi3_AA(layer_error_fix)
weak_sangnom_sd_AA = DescaleTarget(width=854, height=480, kernel=Lanczos(3), do_post_descale=dehalo, do_post_double=sangnom, downscaler=Hermite(linear=True), credit_mask=False).get_upscaled(layer_error_fix)
eedi_sd_AA = DescaleTarget(width=854, height=480, kernel=Lanczos(3), do_post_descale=eedi, downscaler=Hermite(linear=True), credit_mask=False).get_upscaled(layer_error_fix)

AA_clip = fvf.rfs(AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(layer_error_fix), mappings="[3233 3370] [32573 32603] [32661 32688] [33714 33791]")
AA_clip = fvf.rfs(AA_clip, weakest_nnedi3_AA(layer_error_fix), mappings="[32573 32603] [33038 33442] [33497 33535] [33571 33713] [33792 33903] [34039 34147] [34226 34384] [34437 34645]")
AA_clip = fvf.rfs(AA_clip, weakest_nneedi3_AA, mappings="[32880 32940] [33010 33037] [33904 33923] [33981 34038] [34148 34225] [34385 34436]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(layer_error_fix), mappings="[1086 1109] [1260 1276] [1545 1583] [5209 5275] 5804 [6472 6491] [8001 8002] [8495 8513] [11134 11166] [13895 13932] [14445 14499] [14501 14504] [16195 16224] [24696 24697] [25114 25143] [26125 26241] 26787 [27027 27064] [32522 32539] [32556 32572] [32865 32879] [32941 32964]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(layer_error_fix), mappings="5803 [7063 7064] 8000 [8266 8396] 8531 8825 [9054 9203] 11498 11761 [11768 11775] [27502 27566] [28442 28449] [30987 31130] [32519 32521] [32540 32555] [32843 32864] [34783 34801]")
AA_clip = fvf.rfs(AA_clip, eedi_sd_AA, mappings="[32814 32842]")
AA_clip = fvf.rfs(AA_clip, weak_sangnom_AA(layer_error_fix), mappings="[32965 33009] [33443 33496]")
AA_clip = fvf.rfs(AA_clip, weak_sangnom_sd_AA, mappings="[32500 32518] [32604 32660]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(layer_error_fix), mappings="[256 371] [2158 3226] [3495 3555] [3651 3711] [3767 3826] [3906 3966] [4135 4194] [4376 4435] [4608 4667] [4804 4863] [5149 5208] [5453 5512] [5661 5720] [6030 6089] [6341 6446] [6509 6530] [7062 7062] [7507 7565] [7663 7722] [7999 7999] [8203 8265] [8423 8482] [9295 9354] [10037 10096] [12035 12094] [12245 12304] [13678 13737] [13796 13855] [14500 14500] [14639 14699] [15888 15947] [17639 17699] [18157 18216] [18312 18371] [18604 18663] [19174 19234] [19815 19874] [20657 20716] [21006 21065] [21863 21922] [22505 22564] [22986 23045] [23340 23399] [24911 24970] [25359 25419] [25717 25776] [25954 26013] [26580 26639] [28653 28712] [29512 29571] [31526 31585] [31728 31787] [31994 32053] [32270 32329] [32406 32486]")
AA_clip = fvf.rfs(AA_clip, strong_AA(layer_error_fix), mappings="14402 26786 34782")
AA_clip = fvf.rfs(AA_clip, very_strong_AA(layer_error_fix), mappings="7061 34781")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(layer_error_fix, weakest_nneedi3_AA, r'masks\16_Gurren_Lagann_33924-33980.webp'), "[33924 33980]")

AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[763 879] [1110 1139] [34882 35017]")

ed_credit_mask = DiffCreditlessMask(ep_ed, nced)
ed_credit_mask = depth(ed_credit_mask,16)
ed_AA_clip = core.std.MaskedMerge(core.std.Trim(src, ep_ed_start, ep_ed_end), core.std.Trim(AA_clip, ep_ed_start, ep_ed_end), ed_credit_mask)
AA_clip = core.std.Trim(AA_clip, 0, ep_ed_start-1) + ed_AA_clip + core.std.Trim(AA_clip, ep_ed_end+1, src.num_frames-1)

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[1423 1435] [1536 1538] 1544 [1628 1674] [13590 13677] [13905 13906] [22102 22205] [27568 27570]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [696 726] [826 879] [1110 1139] [1187 1259] [1319 1391] [1399 1416] [1419 1422] [1539 1583] [1616 1627] [1884 1916] [1939 1992] [2302 2308] [7492 7555] [11080 11245] [11542 11697] [11856 11986] [15740 15822] [17311 17412] [17774 17964] [18575 18760] [20447 20494] [21104 21139] [21313 21467] [21765 21859] [22643 22701] [22761 22850] [23470 23528] [23683 24055] [24569 24633] [25539 25567] [26219 26468] [27793 27821] [28051 28051] [28413 28518] [30974 31152] [31273 31319] [31559 31586] [34879 34892]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 501] [633 695] [763 825] [880 917] [1392 1398] [1417 1418] [1590 1615] [1675 1681] [5370 5812] [7141 7366] [8314 8325] [9792 9821] [10117 10136] [12283 12288] [12315 12320] [12398 12424] [13946 13968] [14637 14743] [15496 15572] [16528 16581] [16755 16813] [16856 16974] [17046 17243] [18054 18080] [18086 18105] [18324 18574] [19200 19202] [19219 19269] [20287 20322] [20518 20596] [23173 23303] [23529 23576] [24056 24233] [25130 25235] [25272 25408] [25511 25538] [25883 25908] [26923 27029] [27321 27482] [27912 27971] [28643 28673] [28799 28857] [29592 29700] [29902 29936] [30260 30366] [30461 30937] [31646 31728] [31985 32044] [34904 34918] [34929 34942]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[10637 10641] 10643 [19197 19199] [20425 20427] [20599 20601] [23101 23172] [23304 23410] [24634 24692] [28224 28412] [28519 28602] [29299 29340]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="10642 [13702 13705] [20597 20598]")
DD_clip = fvf.rfs(DD_clip, denoise_deband_strongest(DD_clip, thSAD=120, thr=4.0, y=32, sigma=2.0), mappings="[13706 13833]")

for i in range(1436, 1535):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, r'masks\09_Gurren_Lagann_1535.webp'), "1535")

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