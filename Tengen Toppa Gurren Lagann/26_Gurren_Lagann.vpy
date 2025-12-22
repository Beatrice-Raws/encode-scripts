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
ep_ed_start = 32488
ep_ed_end = 34645

# descale/rescale & AA
ep_AA_clip = main_AA(src, credit_mask=False)

op_AA_clip = ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(0, 1422) + core.std.Trim(ncop_v3_aa, 1423, 1542) + ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(1543, 2158)

AA_clip = op_AA_clip + core.std.Trim(ep_AA_clip, 2159, ep_ed_start-1) + core.std.Trim(op_ed_AA_2(src, credit_mask=True), ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

strongest_AA = strongest_AA(src)

AA_clip = fvf.rfs(AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(src), mappings="[3797 3934] [11705 11787] [13298 13398] [32392 32487] [16957 17003] [17626 17721] [18284 18601] [19900 20115] [32392 32487]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src), mappings="[2167 2206] [2679 2685] [2710 2714] [4728 4728] [4828 4833] [6070 6254] [9241 9279] [10747 10747] [10956 10957] [11024 11025] [11350 11355] [11371 11398] [12397 12454] [17067 17067] [18935 19401] [20311 20334] [20395 20466] [21622 21701] [29282 29386] [32079 32080] [34786 34788]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src, credit_mask=True), mappings="[34984 35017]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src), mappings="3180 3186 3192 3198 3207 3216 3489 3588 4727 [6471 6643] 10746 [10954 10955] [11333 11349] [11788 11931] [12384 12396] [13508 13691] 17066 23408 23414 23420 32078 34739 34747 [34789 34790]")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="4727 [6471 6643] 10954 17066 34739 34747 34790")
AA_clip = fvf.rfs(AA_clip, strong_AA(src), mappings="4999 17065 23407 23413 23419 34791")
AA_clip = fvf.rfs(AA_clip, very_strong_eedi_AA(src), mappings="17064")
AA_clip = fvf.rfs(AA_clip, strongest_AA, mappings="3488 3587 17063")
### mask for [13761 13790]
a_13761_13790 = core.std.Trim(strongest_AA, 13761, 13790)
b_13761_13790 = core.std.Trim(src, 13761, 13790)
a_fade_b = crossfade(clipa=a_13761_13790, clipb=b_13761_13790, duration=29)
masked_13761_13790 = ApplyImageMask(AA_clip.std.Trim(13761, 13791), a_fade_b, r'masks\26_Gurren_Lagann_13692-13762.webp')
AA_clip = AA_clip.std.Trim(0, 13760) + masked_13761_13790.std.Trim(0, 28) + AA_clip.std.Trim(13790, src.num_frames-1)
###
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strongest_AA, r'masks\26_Gurren_Lagann_13692-13762.webp'), "[13692 13762]")

AA_clip = fvf.rfs(AA_clip, main_AA(src, credit_mask=True), mappings="[34902 34983]")

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[2167 2175] [2236 2334] [2577 2602] [17793 17839] [22420 22429] [22590 22738] [27994 28052] [34851 34865]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30] [2984 3078] [3109 3110] [3139 3140] [3695 3790] [4112 4265] [4527 4561] [4654 4698] [4856 4858] [5376 5404] [9741 9802] [11332 11390] [11788 11931] [13246 13398] [14810 14878] [15427 15569] [15953 16239] [16341 16409] [16416 16466] [16473 16508] [16515 17003] [17412 17721] [18312 18601] [18935 19401] [19900 20115] [21182 21259] [22407 22419] [22518 22589] [23271 23389] [24125 24160] [24465 24524] [24624 24731] [24926 24948] [25466 25643] [30216 30497]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] 1326 [4562 4602] [4864 4864] [4867 4867] [4870 4872] [4874 4891] [10089 10171] [13399 13473] [15645 15727] [20336 20340] [20342 20342] [20344 20348] [20350 20352] [20354 20354] [20356 20364] [20366 20394] [21949 22110] [22739 22797] [22822 22893] [23390 23609] [24161 24464] [27681 27727] [28148 28437] [34808 34816]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[18650 18792] [20116 20161] [20162 20215] [21702 21917] [34828 34829]")
DD_clip = fvf.rfs(DD_clip, very_strong_dd_grain, mappings="[2615 2674] [4762 4772] [4776 4781] [5412 5632] [7710 8498] [21510 21574] [22798 22821] [22986 23211] [23850 24124] [25184 25370] [25909 26151] [26216 26345] [27078 27172] [28522 28898] [32016 32031]")
# [15176 15311]
DD_clip_15176_15311 = core.std.Crop(very_strong_dd_grain, left=674, right=674)
DD_clip_15176_15311 = haf.Overlay(DD_clip, DD_clip_15176_15311, x=674)
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, DD_clip_15176_15311, simple_darkmask), mappings="[15176 15311]")
#
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, very_strong_dd_grain, simple_darkmask), mappings="[24732 24833] [31892 31913]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, strongest_denoise_deband, simple_darkmask), mappings="[17722 17792] [17982 18028] [18912 18934]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, strongest_dd_grain, simple_darkmask), mappings="[31940 31945]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914] [4266 4348] [4562 4602] [9623 9739] [21949 22110] [24161 24464]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip, y=96), mappings="[10089 10171] [20610 20733]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip, y=128), mappings="[18650 18792] [20116 20161]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, DD_clip, r'masks\26_Gurren_Lagann_34795.webp'), "34795")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, DD_clip, r'masks\26_Gurren_Lagann_34796-34797.webp'), "[34796 34797]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, DD_clip, r'masks\26_Gurren_Lagann_34798-34807.webp'), "[34798 34807]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strong_denoise_deband, r'masks\26_Gurren_Lagann_18793-18911.webp'), "[18793 18911]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(core.neo_f3kdb.Deband(very_strong_denoise_deband)), r'masks\26_Gurren_Lagann_4407-4526.webp'), "[4407 4526]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(core.neo_f3kdb.Deband(very_strong_denoise_deband, y=96)), r'masks\26_Gurren_Lagann_16240-16334.webp'), "[16240 16334]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(core.neo_f3kdb.Deband(very_strong_denoise_deband, y=96)), r'masks\26_Gurren_Lagann_5687-5830.webp'), "[5687 5830]")

for i in range(32014, 32032):
    mask_path = fr'masks\26_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32036.webp'), "32036")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32037.webp'), "32037")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, AddNoise.GAUSS((3.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(strongest_dd_grain), r'masks\26_Gurren_Lagann_11658-11704.webp'), "[11658 11704]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\26_Gurren_Lagann_14625-14809.webp'), "[14625 14809]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[3695 3790] [9623 9739] [10089 10171] [15645 15727] [23700 23849] [24161 24464] [25909 26151] [28148 28437]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542] [4562 4602] [26216 26345] [27078 27172] [28522 28898]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942]")

final = depth(DD_clip, 10)

set_output(final)