# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00003.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
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

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src), mappings="[2393 2406] [2597 2631] [4312 4790] [5150 5382] [5831 5997] [6148 6171] [6475 6475] [6517 6517] [7396 7396] [7472 7472] [19863 20071] [20240 20292] [22338 22713] [29434 29486]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src), mappings="8776 [23192 23194]")
AA_clip = fvf.rfs(AA_clip, eedi_AA_YUV(AA_clip), mappings="[2391 2392] [21655 21678]")
AA_clip = fvf.rfs(AA_clip, strong_AA(src), mappings="8775")
AA_clip = fvf.rfs(AA_clip, strong_AA_YUV(src), mappings="2390")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="6516")
AA_clip = fvf.rfs(AA_clip, ApplyStab(AA_clip), mappings="[3960 4097]")

AA_clip = fvf.rfs(AA_clip, main_AA(src, credit_mask=True), mappings="[34899 35019]")

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
very_strong_dd_grain = AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(very_strong_denoise_deband)

strongest_denoise_deband = denoise_deband_strongest(AA_clip, thSAD=120, thr=12.0, sigma=2.0)
strongest_dd_grain = AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(strongest_denoise_deband)

simple_darkmask = core.fmtc.bitdepth(AA_clip, bits=8, dmode=9).std.Levels(min_in=0, max_in=40, min_out=0, max_out=255, planes=[0]).std.Invert().std.Levels(min_in=0, max_in=40, min_out=0, max_out=255, planes=[0]).std.Invert().fmtc.bitdepth(bits=16)

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[2167 2209] [2290 2318] [3368 3370] [11443 11461] [18680 18774] [20490 20548] [24120 24178] [26451 26497] [30273 30343] [30964 31005]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30] [2407 2469] [3371 3378] [4193 4311] [5150 5550] [11175 11237] [11462 11466] [11995 12089] [12173 12478] [13200 13270] [16875 16919] [19157 19334] [22005 22051] [23193 23433] [23919 23941] [23968 23976] [24681 24763] [26498 26616] [27622 27704] [31006 31040] [31364 31930]")
DD_clip = fvf.rfs(DD_clip, denoise_deband(AA_clip, thSAD=65, thr=3.0, sigma=1.0), mappings="[14351 14366] [14378 14393]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] [1326 1326] [2732 2829] [4875 5149] [7339 7354] [10687 10717] [15104 15175] [15619 15828] [19086 19156] [21751 21807] [24084 24119] [25757 25760]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[133 133] [151 159] [371 502] [1418 1423] [1540 1542] [1749 1914] [2523 2558] [2920 3115] [5688 5830] [6172 6218] [9542 9598] [10826 10832] [18512 18679] [19418 19551] [22088 22254] [25963 26048] [31931 32002]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, core.neo_f3kdb.Deband(strong_denoise_deband), simple_darkmask), mappings="[21679 21725]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, very_strong_denoise_deband, simple_darkmask), mappings="[5998 6171]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(weakest_denoise_deband, strongest_denoise_deband, simple_darkmask), mappings="[5831 5997]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(weakest_denoise_deband, core.neo_f3kdb.Deband(DD_clip, y=128), simple_darkmask), mappings="[5831 5997]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, AddNoise.GAUSS((8.0, 0), 0.85, Catrom, True, luma_scaling=0).grain(DD_clip), simple_darkmask), mappings="[5831 5997] [5998 6084]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="[8412 8513]")
DD_clip = fvf.rfs(DD_clip, core.neo_dfttest.DFTTest(DD_clip, sigma=8.0, planes=[0]), mappings="[16373 16487] [27551 27621]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip, y=32, cb=0, cr=0), mappings="[16875 16919]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914] [16373 16487] [18512 18679] [21751 21807] [22088 22254] [25963 26048] [27551 27621]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip, y=96), mappings="[6172 6218]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip, y=128), mappings="[2920 3115] [25963 26048]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_7603-7737.webp'), "[7603 7737]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(strong_denoise_deband, strongest_dd_grain, r'masks\20_Gurren_Lagann_3586-3668.webp'), "[3586 3668]")

for i in range(6518, 6562):
    mask_path = fr'masks\20_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_dd_grain, mask_path), str(i))

for i in range(8911, 8920):
    mask_path = fr'masks\20_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_9398-9399.webp'), "9398 9399")

for i in range(9454, 9470):
    mask_path = fr'masks\20_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_9470-9475.webp'), "[9470 9475]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_9476-9478.webp'), "[9476 9478]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_9479-9481.webp'), "[9479 9481]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_9482-9484.webp'), "[9482 9484]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_9485-9487.webp'), "[9485 9487]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_9488-9490.webp'), "[9488 9490]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_9491-9493.webp'), "[9491 9493]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_9494-9517.webp'), "[9494 9517]")

for i in range(9518, 9542):
    mask_path = fr'masks\20_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, mask_path), str(i))

for i in range(11238, 11334):
    mask_path = fr'masks\20_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_dd_grain, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_dd_grain, r'masks\20_Gurren_Lagann_11334-11440.webp'), "[11334 11440]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_11334_11440.webp'), "[11334 11440]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_12544-12711.webp'), "[12544 12711]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_12712-12713.webp'), "[12712 12713]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_12714-12715.webp'), "[12714 12715]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_12716-12729.webp'), "[12716 12729]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_16022-16075.webp'), "[16022 16075]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_16076-16078.webp'), "[16076 16078]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_16079-16081.webp'), "[16079 16081]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_16082-16084.webp'), "[16082 16084]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_16085-16171.webp'), "[16085 16171]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_16172-16174.webp'), "[16172 16174]")

for i in range(16175, 16190):
    mask_path = fr'masks\20_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\20_Gurren_Lagann_16190-16230.webp'), "[16190 16230]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(strong_denoise_deband, strongest_denoise_deband, r'masks\20_Gurren_Lagann_21749.webp'), "21749")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[12090 12172] [14293 14350] [16875 16919] [19086 19156] [21679 21725] [22088 22254]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542] [3740 3810] [10687 10717] [10826 10832] [27551 27621] [2920 3115]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942] [5688 5830] [6085 6171] [6172 6218] [8412 8513] [9542 9598] [25963 26048]")

final = depth(DD_clip, 10)

set_output(final)