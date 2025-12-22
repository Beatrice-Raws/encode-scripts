# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00004.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ncop_v3 = core.bs.VideoSource(r'00007.m2ts').std.Trim(0, 2158).std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
ncop_v3 = depth(ncop_v3,16)

ncop_v3_aa = core.raws.Source(r'NCOP_v3_aa.y4m').std.Trim(0, 2158).std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)

ep_op = core.std.Trim(src, 0, 2158)
ep_ed_start = 32489
ep_ed_end = 34646

# descale/rescale & AA
ep_AA_clip = main_AA(src, credit_mask=False)

op_AA_clip = ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(0, 1422) + core.std.Trim(ncop_v3_aa, 1423, 1542) + ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(1543, 2158)

AA_clip = op_AA_clip + core.std.Trim(ep_AA_clip, 2159, ep_ed_start-1) + core.std.Trim(op_ed_AA_2(src, credit_mask=True), ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

weak_eedi_AA = weak_eedi_AA(src)
eedi_AA_YUV = eedi_AA_YUV(AA_clip)

AA_clip = fvf.rfs(AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(src), mappings="[9007 9042]")
AA_clip = fvf.rfs(AA_clip, core.std.MaskedMerge(src, main_AA(src, credit_mask=False), core.fmtc.bitdepth(src, bits=8, dmode=9).std.Levels(min_in=0, max_in=80, min_out=0, max_out=255, planes=[0]).std.Invert().std.Levels(min_in=0, max_in=80, min_out=0, max_out=255, planes=[0]).std.Maximum().fmtc.bitdepth(bits=16)), mappings="[8769 8960]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA, mappings="[3867 3979] [4015 4187] [8222 8228] 17752 [29782 29851] [31072 31202] [31263 31365] [34861 34870]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src), mappings="17751 19233 19509 [27487 27513]")
AA_clip = fvf.rfs(AA_clip, eedi_AA_YUV, mappings="[2769 2786]")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="19257")
AA_clip = fvf.rfs(AA_clip, ApplyStab(AA_clip), mappings="[4194 4331]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(src, weak_eedi_AA, r'masks\21_Gurren_Lagann_34883-35018.webp'), "[34904 34920]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA(src), r'masks\21_Gurren_Lagann_20487.webp'), "20487")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(src, eedi_AA_YUV, r'masks\21_Gurren_Lagann_34883-35018.webp'), "[34890 34903]")

### mask for [22151 22355]
mask_22151_22355 = core.imwri.Read(r'masks\21_Gurren_Lagann_22151.webp') + core.imwri.Read(r'masks\21_Gurren_Lagann_22355.webp')
mask_22151_22355 = ToRGB(mask_22151_22355, 1, 32)
mask_22151_22355 = core.rife.RIFE(mask_22151_22355, model=24, factor_num=204, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_22151_22355 = core.fmtc.bitdepth(mask_22151_22355, bits=16)
mask_22151_22355 = core.std.Trim(mask_22151_22355, 0, 203)
#
masked_22151_22355 = core.std.MaskedMerge(src.std.Trim(22151, 22355), AA_clip.std.Trim(22151, 22355), mask_22151_22355, planes=[0,1,2], first_plane=True)

AA_clip = core.std.Trim(AA_clip, 0, 22150) + masked_22151_22355 + core.std.Trim(AA_clip, 22356, src.num_frames-1)

AA_clip = fvf.rfs(AA_clip, main_AA(src, credit_mask=True), mappings="[4338 4396] [34883 34889] [34921 35018]")

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[2167 2185] [3068 3216] [3275 3376] [3497 3722] [6544 7322] [7412 7821] [9375 9570] [10842 10882] [11167 11441] [14981 15123] [16191 16435] [18247 18430] [19337 19356] [20024 20154] [20349 20402] [23805 23971] [24328 24374] [28793 28866]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30] [2374 2430] [2822 2854] [3867 3979] [4486 4926] [4987 5051] [5966 6083] [6294 6543] [8144 8221] [8341 8399] [9779 9957] [10059 10302] [11056 11166] [13263 13471] [13670 13899] [14455 14598] [14694 14980] [15124 16190] [16436 16566] [17332 17552] [18690 18838] [19357 19380] [19517 19649] [19672 19894] [21803 21871] [24280 24327] [24387 24445] [25299 25621] [25985 26079] [26942 27369] [27430 27485] [29035 29382] [29579 29685] [30155 30477] [31072 31202] [31263 31365] [31389 31489] [31621 31774] [32218 32392]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] [1326 1326] [2324 2346] [5675 5728] [5776 5799] [18530 18554] [18951 19019] [19895 19940] [20463 20486] [20671 20710] [23484 23506]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[133 133] [151 159] [371 502] [1418 1423] [1540 1542] [1749 1914] [2527 2556] [18480 18491] [18839 18903] [20834 20863] [26731 26764] [28161 28423]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(weakest_denoise_deband, very_strong_denoise_deband, simple_darkmask), mappings="[2787 2821] [18583 18618]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="[18555 18582] 34879")
DD_clip = fvf.rfs(DD_clip, core.neo_dfttest.DFTTest(DD_clip, sigma=8.0, planes=[0]), mappings="[2674 2729]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip, y=32, cb=0, cr=0), mappings="[3252 3274]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914] [2458 2526] [2674 2729] [3377 3430]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, core.neo_f3kdb.Deband(very_strong_denoise_deband, y=128), r'masks\21_Gurren_Lagann_12300-12412.webp'), "[12300 12412]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_dd_grain, r'masks\21_Gurren_Lagann_20157-20158.webp'), "[20157 20158]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_dd_grain, r'masks\21_Gurren_Lagann_20159-20160.webp'), "[20159 20160]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_dd_grain, r'masks\21_Gurren_Lagann_20161-20163.webp'), "[20161 20163]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_dd_grain, r'masks\21_Gurren_Lagann_20164-20165.webp'), "[20164 20165]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_dd_grain, r'masks\21_Gurren_Lagann_20166-20168.webp'), "[20166 20168]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_dd_grain, r'masks\21_Gurren_Lagann_20169-20171.webp'), "[20169 20171]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_dd_grain, r'masks\21_Gurren_Lagann_20172-20174.webp'), "[20172 20174]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_dd_grain, r'masks\21_Gurren_Lagann_20175-20187.webp'), "[20175 20187]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, AddNoise.GAUSS((4.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(core.neo_f3kdb.Deband(strongest_denoise_deband, y=128)), r'masks\21_Gurren_Lagann_25622-25740.webp'), "[25622 25740]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[2787 2821] [2855 2901] [3051 3067] [3217 3274] [8341 8399] [14599 14693] [18583 18618] [19895 19940] [26873 26941]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542] [12300 12412] [20834 20863]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942] [28161 28423]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((10.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[18555 18582]")

### mask for [30799 30858]
mask_30799_30858 = core.imwri.Read(r'masks\21_Gurren_Lagann_30799.webp') + core.imwri.Read(r'masks\21_Gurren_Lagann_30858.webp')
mask_30799_30858 = ToRGB(mask_30799_30858, 1, 32)
mask_30799_30858 = core.rife.RIFE(mask_30799_30858, model=24, factor_num=59, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_30799_30858 = core.fmtc.bitdepth(mask_30799_30858, bits=16)
mask_30799_30858 = core.std.Trim(mask_30799_30858, 0, 58)
#
masked_30799_30858 = core.std.MaskedMerge(DD_clip.std.Trim(30799, 30858), AddNoise.GAUSS((4.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(core.neo_f3kdb.Deband(strongest_denoise_deband, y=128)).std.Trim(30799, 30858), mask_30799_30858, planes=[0,1,2], first_plane=True)

DD_clip = core.std.Trim(DD_clip, 0, 30798) + masked_30799_30858 + core.std.Trim(DD_clip, 30859, src.num_frames-1)

final = depth(DD_clip, 10)

set_output(final)