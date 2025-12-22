# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00001.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ncop_v3 = core.bs.VideoSource(r'00007.m2ts').std.Trim(0, 2158).std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
ncop_v3 = depth(ncop_v3,16)

ncop_v3_aa = core.raws.Source(r'NCOP_v3_aa.y4m').std.Trim(0, 2158).std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)

ep_op = core.std.Trim(src, 0, 2158)
ep_ed_start = 32490
ep_ed_end = 34647

# descale/rescale & AA
ep_AA_clip = main_AA(src, credit_mask=False)

op_AA_clip = ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(0, 1422) + core.std.Trim(ncop_v3_aa, 1423, 1542) + ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(1543, 2158)

AA_clip = op_AA_clip + core.std.Trim(ep_AA_clip, 2159, ep_ed_start-1) + core.std.Trim(op_ed_AA_2(src, credit_mask=True), ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src), mappings="[4311 4381] 16035 19808 [24814 24830] [24852 24871] [25290 25543] [25784 25881] [27242 27301] [29824 29899] [34924 34931]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src), mappings="19807 [27240 27241]")
AA_clip = fvf.rfs(AA_clip, eedi_AA_YUV(AA_clip), mappings="[2466 2486] [2507 2527] [2548 2568] [2617 2638] [2660 2758] [4783 4784] [21253 21351] [23751 23834] [23864 23968] [24055 24092] [25882 25967] [26268 26368] [26546 26621] [26955 27001] [27534 27589] [27592 27699] [28016 28043] [28129 28130]")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="[2617 2619] [2692 2694]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(src), mappings="4782 19806 [26544 26545] 27239 27534 34923")
AA_clip = fvf.rfs(AA_clip, sangnom_AA_YUV(src), mappings="27533 [28120 28128]")
AA_clip = fvf.rfs(AA_clip, strong_AA(src), mappings="19805 26543 [27237 27238]")
AA_clip = fvf.rfs(AA_clip, strong_AA_YUV(src), mappings="27532 27591")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(weakest_nneedi3_AA(src), AA_clip, r'masks\18_Gurren_Lagann_26076-26221.webp'), "[26076 26221]")
AA_clip = fvf.rfs(AA_clip, ApplyStab(AA_clip), mappings="[3367 3504] [15696 15815]")

filt_27590 = core.std.Trim(sangnom_AA_YUV(src), 27590, 27590)
filt_27590 = filt_27590.std.Crop(left=268, right=1268, top=650, bottom=72)
filt_27590 = haf.Overlay(AA_clip, filt_27590, x=268, y=650)
AA_clip = fvf.rfs(AA_clip, filt_27590, mappings="27590")

AA_clip = fvf.rfs(AA_clip, main_AA(src, credit_mask=True), mappings="[34880 35019]")

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[17425 17588] [24974 25287] [28472 28583]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30] [2167 2170] [2583 2616] [2642 2657] [2698 2758] [7068 7150] [10385 10473] [10869 11071] [12220 12494] [13283 13941] [16030 16033] [16947 17195] [17340 17424] [17589 18175] [19806 19863] [21599 21832] [24122 24192] [24428 24523] [25544 25783] [26076 26428] [26444 26542] [26547 26638] [27002 27201] [27238 27469] [27355 27531] [27592 27655] [27700 27759] [27820 27853] [28121 28130] [28190 28290] [28319 28453] [28584 29019] [29164 29200] [29512 29675] [29824 29899] [30564 30695] [31072 31239] [34772 34847] [34896 34922]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] [1326 1326] [5641 5815] [15877 15887] [15911 15911] [15948 16029] [23751 23834] [24833 24834] [24837 24847]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[133 133] [151 159] [371 502] [1418 1423] [1540 1542] [1749 1914] [3290 3360] [16295 16467] [34866 34883]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="2556 16035 [34732 34756]")

for i in range(2661, 2676):
    mask_path = fr'masks\18_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_denoise_deband, mask_path), str(i))

for i in range(15832, 15847):
    mask_path = fr'masks\18_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_denoise_deband, mask_path), str(i))

for i in range(15847, 15851):
    mask_path = fr'masks\18_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914] [22696 22778]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[27592 27699]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542] 2556 [11340 11398] [22696 22778] [34866 34883]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942] [34732 34756]")

final = depth(DD_clip, 10)

set_output(final)