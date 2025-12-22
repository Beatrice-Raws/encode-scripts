# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00005.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
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

weak_eedi_AA = weak_eedi_AA(src)
eedi_AA_YUV = eedi_AA_YUV(AA_clip)
strong_eedi_AA = strong_eedi_AA(src)
very_strong_eedi_AA = very_strong_eedi_AA(src)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA, mappings="[3462 3484] [4751 4754] [5617 5618] [5692 5692] [5696 5696] [5698 5698] [5700 5700] [5702 5702] [5704 5704] [5706 5706] [5708 5708] [5710 5710] [7435 7466] [9554 9809] [9874 9874] [9903 9940] [10278 10311] [11915 11937] [13044 13114] [13553 13576] [14378 14410] [14584 14630] [16098 16130] [16251 16282] [16417 16510] [17469 17552] [22348 22359] [22712 22713] [22888 23249] [24370 24537] [25526 25644] [25647 25649] [25687 25745] [27147 27155] [27424 27482] [27987 27988] [28498 28568] [28677 28723]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src), mappings="3213 [3462 3484] 5619 5628 5630 5693 5695 5697 5699 5701 5703 5705 5707 5709 5711 5712 [5731 5753] [12648 12694] 13651 14411 16076 16078 16097 [22346 22347] 22711 [25645 25646] 27179 30805")
AA_clip = fvf.rfs(AA_clip, eedi_AA_YUV, mappings="[4608 4642] [4739 4741] [5409 5493] [10312 10406] [15043 15210] [15621 15646] [15847 15903] [16222 16245]")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="3213 13952 13953 16096 25645 27178")
AA_clip = fvf.rfs(AA_clip, strong_eedi_AA, mappings="12647 22345 22710")
AA_clip = fvf.rfs(AA_clip, very_strong_AA(src), mappings="[16093 16095]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_eedi_AA, r'masks\22_Gurren_Lagann_9872.webp'), "9872 9873")

AA_clip = fvf.rfs(AA_clip, main_AA(src, credit_mask=True), mappings="[34888 35020]")

for i in range(9810, 9872):
    mask_path = fr'masks\22_Gurren_Lagann_{i}.webp'
    AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, very_strong_eedi_AA, mask_path), str(i))

for i in range(15449, 15561):
    mask_path = fr'masks\22_Gurren_Lagann_{i}.webp'
    AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, eedi_AA_YUV, mask_path, luma_only=False), str(i))

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[3510 3513] [4935 5162] [8184 8326] [14584 14630] [17721 17856] [18425 18520] [26567 26567] [26801 26802] [26805 26805] [27483 27625] [30953 30972] [34900 34937]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30] [4204 4303] [4585 4607] [7693 7720] [7926 7953] [8707 8810] [9903 9940] [10263 10311] [10353 10406] [12695 12764] [13652 13705] [14631 14678] [14966 15287] [17553 17720] [21361 21422] [22293 22344] [24479 24541] [26563 26566] [26979 26980] [27097 27107] [27901 27978] [28498 28568] [30952 30952] [31901 32111]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] [1326 1326] [4898 4926] [5644 5645] [7834 7839] [8659 8706] [8818 8820] [13624 13627] [14258 14259] [15956 16023] [22688 22709] [23805 24158] [26839 26882] [27172 27177] [28926 29032]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[3462 3484] [5635 5638] [16081 16092] [19673 20156] [23779 23804] [25854 26056] [26449 26495] [26983 27072] [29045 29140] [29280 29303] [30383 30460] [30669 30804]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, strong_denoise_deband, simple_darkmask), mappings="[12022 12046]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, core.neo_f3kdb.Deband(very_strong_denoise_deband), simple_darkmask), mappings="[22345 22431] [27424 27482]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="[3188 3188]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914] [3462 3484]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_dd_grain, r'masks\22_Gurren_Lagann_6104-6174.webp'), "[6104 6174]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[13830 13951] [22345 22431] [22524 22570] [22688 22709] [22782 22887] [23627 24158] [25854 26056] [26983 27072] [28926 29032]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542] [19673 20156] [26449 26495] [29045 29140] [29280 29303] [30383 30460]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942] [3462 3484]")

final = depth(DD_clip, 10)

set_output(final)