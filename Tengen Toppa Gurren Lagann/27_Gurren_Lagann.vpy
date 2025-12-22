# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00004.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ep_ed_start = 28314
ep_ed_end = 30471

# descale/rescale & AA
ep_AA_clip = main_AA(src, credit_mask=False)

AA_clip = core.std.Trim(ep_AA_clip, 0, ep_ed_start-1) + core.std.Trim(op_ed_AA_2(src, credit_mask=True), ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

weak_eedi_AA = weak_eedi_AA(src)
eedi_AA = eedi_AA(src)
eedi_AA_YUV = eedi_AA_YUV(src)
strong_eedi_AA = strong_eedi_AA(src)
strongest_AA = strongest_AA(src)

AA_clip = fvf.rfs(AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(src), mappings="[3326 3367] [4514 4651] [15812 15854] [34546 34641]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA, mappings="[1985 1987] [2018 2028] [2515 2559] [3137 3137] [3747 3747] [6537 6537] [6543 6543] [9289 9293] [9321 9332] [10127 10127] [12811 12812] [14126 14128] [14849 14849] [16174 16175] [17784 17796] [18122 18335] [18375 18377] [18726 18755] [18804 18820] [18833 18849] [18859 18861] [18863 18863] [18865 18865] [18867 18867] [18870 18879] [18881 18881] [18883 18883] [18885 18893] [18896 18899] [18902 18902] [18910 18913] [18920 18922] [18924 18924] [18926 18926] [18928 18928] [18938 18938] [18940 18940] [18942 18942] [18954 18954] [18956 18956] [18967 18971] [18974 18974] [19044 19044] [19046 19046] [19455 19455] [19457 19457] [19459 19459] [19461 19500] [19532 19541] [20159 20159] [20983 21040] [21349 21354] [25172 25284] [25965 26138] [27328 27350] [31898 32040]")
AA_clip = fvf.rfs(AA_clip, eedi_AA, mappings="[3136 3136] [3748 3748] [7096 7096] [7098 7098] [7117 7117] [7119 7119] [9288 9288] [10129 10129] [12535 12545] [12809 12810] [12986 12987] [14855 14855] [15598 15639] [17773 17774] [17782 17783] [18336 18371] [18373 18374] [18654 18654] [18862 18862] [18864 18864] [18866 18866] [18880 18880] [18882 18882] [18884 18884] [18923 18923] [18925 18925] [18927 18927] [18939 18939] [18941 18941] [18955 18955] [18973 18973] [19043 19043] [19045 19045] [19454 19454] [19456 19456] [19458 19458] [19460 19460] [19529 19531] [20158 20158] [20980 20982] [21355 21358] [27923 27925]")
AA_clip = fvf.rfs(AA_clip, weak_sangnom_AA(src), mappings="[4210 4345] 12809 16173")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(src), mappings="4268 4270 4272 7117 9357 15855 16503 18114 18116")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="3748 12986 14855 17782 17783 [18336 18371] 18373 19529")
AA_clip = fvf.rfs(AA_clip, strong_AA(src), mappings="3368 3410 3749 [17763 17772] 18372 18972 19055 20157")
AA_clip = fvf.rfs(AA_clip, very_strong_eedi_AA(src), mappings="14854 17781")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(eedi_AA, very_strong_eedi_AA(strong_AA_YUV(sangnom_AA_YUV(eedi_AA_YUV))), r'masks\27_Gurren_Lagann_1988.webp', luma_only=False), "1988")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, RealESRGAN_AA(AA_clip), r'masks\27_Gurren_Lagann_1988-2.webp', luma_only=False), "1988")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(eedi_AA, very_strong_eedi_AA(strong_AA_YUV(sangnom_AA_YUV(eedi_AA_YUV))), r'masks\27_Gurren_Lagann_1989.webp', luma_only=False), "1989")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(weak_eedi_AA, strong_AA_YUV(sangnom_AA_YUV(eedi_AA_YUV)), r'masks\27_Gurren_Lagann_1990.webp', luma_only=False), "1990")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(very_strong_eedi_AA(src), strongest_AA, r'masks\27_Gurren_Lagann_3135.webp'), "3135")

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[8 11] [4908 5315] [7528 7582] [8776 8829] [9432 9458] [11016 11181] [11232 11332] [12118 12173] [13426 13527] [15812 15854] [18851 18854] [18915 18915] [20207 20231] [21953 22014] [23398 23624] [24068 24084] [28214 28276] [30244 30435] [30549 30563] [31898 32040]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[12 270] [3315 3324] [7586 7631] [10579 10620] [11011 11015] [11960 12117] [12174 12294] [12986 12991] [13641 13836] [18920 18920] [19512 19514] [19815 19836] [19897 20031] [20232 20378] [20691 20748] [21041 21051] [21804 21807] [22015 22288] [22683 22741] [22917 23095] [23625 23803] [24041 24067] [24117 24224] [30564 31829]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[2046 2046] [6844 6845] [7504 7510] [12546 12645] [14667 14734] [15432 15514] [17533 17580] [17939 18016] [18645 18647] [27685 27776]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[2047 2048] [7191 7191] [7195 7195] [8992 9105] [9486 9531] [12774 12775] [17776 17776] [17783 17938] [18076 18101] [18643 18644] [18648 18654] [18908 18908]")
DD_clip = fvf.rfs(DD_clip, very_strong_dd_grain, mappings="[1952 1952] [6726 6739] [7087 7121] [7147 7147] [7168 7169] [9125 9128] [9176 9198] [9282 9287] [9335 9340] [9356 9356] [9651 9670] [12346 12377] [12782 12785] [12796 12805] [14464 14666] [16318 16328] [18267 18335] [18623 18637] [18794 18801] [18886 18893] [18916 18919] [26240 26484] [27777 27850]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="[17763 17772]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(weak_denoise_deband, very_strong_denoise_deband, simple_darkmask), mappings="[7053 7086] [17616 17762] 17775 [18855 18858]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(core.neo_f3kdb.Deband(very_strong_denoise_deband)), simple_darkmask), mappings="[10247 10522] [11333 11415] [13331 13425] [13974 14031] [14038 14063] [14129 14142] [14178 14205] [14234 14237] [14274 14345]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, very_strong_dd_grain, simple_darkmask), mappings="[1934 1947] [18944 18951] [18976 19006] [22361 22517]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[3928 3957] [15432 15514]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip, y=128), mappings="[27685 27776]")

for i in range(19525, 19542):
    mask_path = fr'masks\27_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, core.neo_f3kdb.Deband(strong_denoise_deband), mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strong_denoise_deband, r'masks\27_Gurren_Lagann_7488-7493.webp'), "[7488 7493]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strong_denoise_deband, r'masks\27_Gurren_Lagann_7494-7503.webp'), "[7494 7503]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32017.webp'), "1967")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\27_Gurren_Lagann_1968.webp'), "1968")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32019.webp'), "1969")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32020.webp'), "1970")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32028.webp'), "1971")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32029.webp'), "1972")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32030.webp'), "1973")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32031.webp'), "1974")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32036.webp'), "1979")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_dd_grain, r'masks\26_Gurren_Lagann_32037.webp'), "1980")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_dd_grain, r'masks\27_Gurren_Lagann_2252-2316.webp'), "[2252 2316]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_dd_grain, r'masks\27_Gurren_Lagann_15106-15219.webp'), "[15106 15219]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[12546 12645]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[15432 15514]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[27685 27776]")

### mask for [271 447]
mask_271_447 = core.imwri.Read(r'masks\27_Gurren_Lagann_271.webp') + core.imwri.Read(r'masks\27_Gurren_Lagann_447.webp')
mask_271_447 = ToRGB(mask_271_447, 1, 32)
mask_271_447 = core.rife.RIFE(mask_271_447, model=24, factor_num=176, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_271_447 = core.fmtc.bitdepth(mask_271_447, bits=16)
mask_271_447 = core.std.Trim(mask_271_447, 0, 175)
#
masked_271_447 = core.std.MaskedMerge(weak_denoise_deband.std.Trim(271, 447), strongest_denoise_deband.std.Trim(271, 447), mask_271_447, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 270) + masked_271_447 + core.std.Trim(DD_clip, 448, src.num_frames-1)

final = depth(DD_clip, 10)

set_output(final)