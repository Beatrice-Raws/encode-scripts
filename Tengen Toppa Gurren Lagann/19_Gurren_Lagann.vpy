# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00002.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
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

eedi_AA = eedi_AA(src)

AA_clip = fvf.rfs(AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(src), mappings="[9459 9506] [10075 10749] [10803 11267] [28137 28303]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src), mappings="[9430 9458] [9596 9597] [9654 9667] [14155 14261] [18068 18114] [18420 18514] [18655 18718] [18776 18836] [18939 19014] [19909 20039] [22474 22677] [22752 22838] [22952 23034] [23163 23243] [23575 23626] 25130 [25422 25453] [27523 27531] [30086 30126] 30966")
AA_clip = fvf.rfs(AA_clip, eedi_AA, mappings="[22145 22234] [23148 23162] 25132 25134 [26798 26892] 30965")
AA_clip = fvf.rfs(AA_clip, eedi_AA_YUV(AA_clip), mappings="[2312 2346] [2487 2566] [2753 2775] [9537 9538] [9588 9594] [9598 9653] [16943 16976] [22001 22030] [22095 22132] [23530 23573] [24772 24794] [24919 24990] [25184 25198] [25624 25718] [25924 26104] [27809 27832] [27923 27994] [34823 34858]")
AA_clip = fvf.rfs(AA_clip, strong_AA(src), mappings="24136")
AA_clip = fvf.rfs(AA_clip, strong_AA_YUV(src), mappings="[2750 2752] 9536 9595]")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="9536 9595")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='eedi3'), mappings="23148 25837")
AA_clip = fvf.rfs(AA_clip, RealESRGAN_AA(src), mappings="[25837 25923]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(santiag(AA_clip, type='nnedi3'), sangnom_AA_YUV(src), r'masks\19_Gurren_Lagann_13224-13306.webp'), "[13224 13306]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, eedi_AA, r'masks\19_Gurren_Lagann_22367-22473.webp'), "[22367 22473]")

AA_clip = fvf.rfs(AA_clip, main_AA(src, credit_mask=True), mappings="[31683 31832] [31862 32023] [34889 35018]")

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
strongest_dd_grain = AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(strongest_denoise_deband)

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[5459 5459] [5516 5516] [7938 7938] [17723 17771] [23684 23749] [25138 25138] [25251 25274] [26527 26819] [27239 27309] [27429 27502] [28304 28440] [28722 28850] [30127 30276] [30484 30560]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30] [2167 2170] [2167 2218] [2260 2274] [2347 2442] [2718 2863] [3822 3976] [5452 5458] [5517 5519] [7679 7830] [7919 7937] [11268 11293] [11768 11970] [12895 13066] [17772 17781] [21431 21550] [21599 21670] [22752 22951] 23629 [23750 23898] [25275 25304] [26448 26526] [26820 26821] [27154 27178] [27310 27428] [28137 28303] [29471 29552] [29640 29758] [29906 30085] [30277 30335] [30390 30424] [30561 30631] [30739 30952] [30968 31017] [31201 32023] [34870 34884] [34987 35018]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] [1326 1326] [3448 3654] [6120 6161] [6276 6544] [6604 6675] [7095 7345] [7831 7914] [11339 11410] [12668 12835] [14262 14368] [15371 15624] [15756 15929] [19015 19109] [19145 19203] [23570 23573] [24294 24371] [24374 24418] [24469 24582] 26397 [29553 29600] [30959 30964] [32161 32238]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[133 133] [151 159] [371 502] [1418 1423] [1540 1542] [1749 1914] [2624 2649] [5029 5112] [5587 6119] [6162 6275] [6545 6603] [6766 7094] [7346 7678] [12566 12642] [14053 14261] [14369 14906] [16037 16131] [16451 16465] [18837 18938] [19110 19144] [29329 29423] [29601 29639]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="[18719 18775] [23574 23574]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914] [5029 5112]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, r'masks\19_Gurren_Lagann_11971-12222.webp'), "[11971 12222]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, r'masks\19_Gurren_Lagann_12223-12302.webp'), "[12223 12302]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, r'masks\19_Gurren_Lagann_12303-12434.webp'), "[12303 12434]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[5029 5112]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542] [5029 5112] [5587 7678] [14053 14906] [16037 16131] [16451 16465] [17399 17722] [18837 18938] [19110 19144] [30425 30483]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942] [5029 5112] [18719 18775] [25837 25923]")

final = depth(DD_clip, 10)

set_output(final)