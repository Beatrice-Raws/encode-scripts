# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00000.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ncop_v3 = core.bs.VideoSource(r'00007.m2ts').std.Trim(0, 2158).std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
ncop_v3 = depth(ncop_v3,16)

ncop_v3_aa = core.raws.Source(r'NCOP_v3_aa.y4m').std.Trim(0, 2158).std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)

ep_op = core.std.Trim(src, 0, 2158)
ep_ed_start = 32491
ep_ed_end = 34648

# descale/rescale & AA
ep_AA_clip = main_AA(src, credit_mask=False)

op_AA_clip = ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(0, 1422) + core.std.Trim(ncop_v3_aa, 1423, 1542) + ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(1543, 2158)

AA_clip = op_AA_clip + core.std.Trim(ep_AA_clip, 2159, ep_ed_start-1) + core.std.Trim(op_ed_AA_2(src, credit_mask=True), ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

eedi_AA_YUV = eedi_AA_YUV(AA_clip)
strong_eedi_AA = strong_eedi_AA(src)

AA_clip = fvf.rfs(AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(src), mappings="[3085 3120] [3306 3443] [18261 18353] [32395 32490]")
AA_clip = fvf.rfs(AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=True).get_upscaled(src), mappings="[3552 3601]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src), mappings="2521 [4188 4354] 5141 [6261 6310] [13070 13134] [13975 13987] [18615 18616] [22639 22644] [23966 23967] [23996 23997] [24664 24665] [24693 24694] [25508 25541] [25918 25920] [26499 26796] [28865 29116] [29741 29759] [34878 34879]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src), mappings="[5140 5140] [13963 13974] [18613 18614] [18649 18650] [18899 18899] [18901 18901] [18903 18903] [19058 19061] [19530 19555] [25916 25917]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src, credit_mask=True), mappings="[34880 34912] [34949 34975]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src, credit_mask=True), mappings="34948")
AA_clip = fvf.rfs(AA_clip, eedi_AA_YUV, mappings="[6311 6373] [6437 6455]")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="[13963 13974] 18613 18649 [25913 25915]")
AA_clip = fvf.rfs(AA_clip, strong_eedi_AA, mappings="2520 [6435 6436] 18648")

AA_clip = fvf.rfs(AA_clip, main_AA(src, credit_mask=True), mappings="[3447 3551] [8346 8470] [8534 8619] [34913 34947] [34976 35020]")

# denoise, deband & regrain

### mask for [3037 3084]
mask_3037_3084 = core.imwri.Read(r'masks\23_Gurren_Lagann_3037.webp') + core.imwri.Read(r'masks\23_Gurren_Lagann_3084.webp')
mask_3037_3084 = ToRGB(mask_3037_3084, 1, 32)
mask_3037_3084 = core.rife.RIFE(mask_3037_3084, model=24, factor_num=47, factor_den=1)
mask_3037_3084 = core.std.Trim(mask_3037_3084, 0, 47).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[2809 2817] [7456 7580] [9085 9323] [9389 9531] [11133 11188] [13204 13232] [15936 15959] [16789 16991] [23372 23598] [23656 23726] [24025 24293] [24723 24827] [27070 27200] [29945 30048] [30513 30719] [32203 32273]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30] [3444 3551] [4864 4930] [6478 6559] [7246 7413] [9839 9970] [11228 11242] [13233 13249] [13651 13667] [19248 19257] [19603 19634] [22365 22459] [22589 22684] [28069 28124] [28431 28532] [29248 29485] [34733 34790] [34803 34854]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] [1326 1326] [6046 6046] [17590 17648] [18648 18682] [19857 19858] [19903 19918] [19950 19985] [20139 20160] [21845 22012]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[22233 22364]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914]")

masked_3037_3084 = core.std.MaskedMerge(DD_clip.std.Trim(3037, 3084), AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(core.neo_f3kdb.Deband(very_strong_denoise_deband, y=128)).std.Trim(3037, 3084), mask_3037_3084, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 3036) + masked_3037_3084 + core.std.Trim(DD_clip, 3085, src.num_frames-1)

DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[17590 17648] [18648 18682] [19903 19918] [19950 19985] [20139 20160] [21845 22012]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542] [6005 6046] [25106 25218] [25250 25309]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942] [22233 22364]")

final = depth(DD_clip, 10)

set_output(final)