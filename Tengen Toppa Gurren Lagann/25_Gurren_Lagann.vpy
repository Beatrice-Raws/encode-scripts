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
ep_ed_start = 32489
ep_ed_end = 34646

# descale/rescale & AA
ep_AA_clip = main_AA(src, credit_mask=False)

op_AA_clip = ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(0, 1422) + core.std.Trim(ncop_v3_aa, 1423, 1542) + ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(1543, 2158)

AA_clip = op_AA_clip + core.std.Trim(ep_AA_clip, 2159, ep_ed_start-1) + core.std.Trim(op_ed_AA_2(src, credit_mask=True), ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

AA_clip = fvf.rfs(AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(src), mappings="[2957 3094] [32393 32488]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src), mappings="[4480 4502] [4703 4809] [5741 5745] [6252 6259] [6503 6547] [6811 6813] [6987 7061] [12908 12966] [16872 16872] [17417 17475] [17655 17713] [17714 17772] [18524 18738] [20329 20782] [20882 20922] [21865 22078] [22210 22276] [22370 22702] [24438 24442] [25581 25921] [27339 27341] [27742 27787] [29844 30005] [30598 30680] [31143 31143] [31956 31957] [31985 31987] [32027 32029] [32033 32033] [32039 32039] [32045 32045] [32054 32054] [32063 32063]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src), mappings="[5700 5740] [5996 6013] [6233 6251] [12867 12868] [16706 16707] [16715 16716] [16724 16725] [16733 16734] [20923 20923] [24434 24437] [27337 27338] [31557 31558]")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="5700 5701 [5714 5716] 5741")

AA_clip = fvf.rfs(AA_clip, main_AA(src, credit_mask=True), mappings="[15840 16020] [31836 31926] [32070 32170] [34884 35018]")

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[2167 2170] [2756 2950] [3614 3868] [3976 4112] [4420 4479] [11024 11082] [12892 12907] [19642 19772] [20923 20970] [24279 24417] [24424 24433] [24767 24898] [28895 28953] [30436 30597]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30] [3377 3613] [4266 4336] [4480 4502] [7621 7776] [9219 9289] [9409 9593] [10959 11023] [14068 14252] [14535 14677] [16872 16966] [17655 17713] [18131 18195] [21107 21190] [23148 23169] [24975 25111] [25260 25546] [26291 26410] [27165 27265] [30269 30435] [31146 31169] [34731 34830]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] 1326 [5647 5699] [6466 6502] [7452 7457] [11206 11227] [15084 15190] [16967 17086] [17857 17939] [20971 20999] [22703 23109] [23141 23147] [23174 23179] [27858 27919] [28140 28180] [29892 30005]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[3095 3262] [4113 4195] [5575 5646] [7145 7228] [7430 7440] [7458 7560] [10177 10326] [11253 11260] [11265 11510] [12911 12934] [13606 13639] [17298 17416] [17746 17746] [17748 17748] [17750 17750] [17752 17752] [17754 17754] [17756 17756] [17758 17758] [17760 17760] [17762 17762] [17764 17764] [17766 17766] [17768 17768] [17770 17770] [17772 17772] [19808 20230] [22531 22650]")
DD_clip = fvf.rfs(DD_clip, very_strong_dd_grain, mappings="[25659 25730] [30681 30775]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(weak_denoise_deband, very_strong_denoise_deband, simple_darkmask), mappings="[15191 15298] [27266 27326] [29844 29891]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, very_strong_denoise_deband, simple_darkmask), mappings="[13657 13762] [14003 14058] [19151 19498] [24198 24212]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, core.neo_f3kdb.Deband(very_strong_denoise_deband), simple_darkmask), mappings="[11261 11264] [11705 11746] [11955 11958] [12319 12461]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, strongest_denoise_deband, simple_darkmask), mappings="[2714 2755]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, strongest_dd_grain, simple_darkmask), mappings="[24221 24260] [26411 26470] [26816 26876]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="[12908 12910]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914] [11253 11260] [11265 11510] [12908 12934][17298 17416] [19808 20230] [24481 24647]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(very_strong_denoise_deband), mappings="[27510 27627]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip, y=128), mappings="12909 12910 [22531 22650]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\25_Gurren_Lagann_14325-14474.webp'), "[14325 14474]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\25_Gurren_Lagann_14678-14695.webp'), "[14678 14695]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\25_Gurren_Lagann_14696-14719.webp'), "[14696 14719]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\25_Gurren_Lagann_14720-14743.webp'), "[14720 14743]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\25_Gurren_Lagann_14744-14940.webp'), "[14744 14940]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, core.neo_f3kdb.Deband(very_strong_denoise_deband), r'masks\25_Gurren_Lagann_24143-24177.webp'), "[24143 24177]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_dd_grain, r'masks\25_Gurren_Lagann_25112-25259.webp'), "[25112 25259]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, core.neo_f3kdb.Deband(very_strong_dd_grain), r'masks\25_Gurren_Lagann_26518-26624.webp'), "[26518 26624]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(strong_denoise_deband, strongest_denoise_deband, r'masks\25_Gurren_Lagann_23176.webp'), "23176")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(strong_denoise_deband, strongest_denoise_deband, r'masks\25_Gurren_Lagann_23177.webp'), "23177")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(strong_denoise_deband, strongest_denoise_deband, r'masks\25_Gurren_Lagann_29593-29843.webp'), "[29593 29843]")

for i in range(23180, 23184):
    mask_path = fr'masks\25_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(strong_denoise_deband, strongest_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(strongest_denoise_deband), r'masks\25_Gurren_Lagann_23785-23999.webp'), "[23785 23999]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(strongest_denoise_deband), r'masks\25_Gurren_Lagann_21334-21446.webp'), "[21334 21446]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[11206 11227] [11705 11746] [11955 11958] [13606 13639] [17298 17416] [17857 17939] [20329 20782] [27510 27627] [29593 29843]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542] [11253 11510] [13657 13762] [19151 19498]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942] [3095 3262] [4113 4195] [5575 5646] [7145 7228] [7430 7440] [7452 7560] [10177 10326] [12319 12461] [12908 12934] 17746 17748 17750 17752 17754 17756 17758 17760 17762 17764 17766 17768 17770 17772 [19808 20230] [22531 22650] [24198 24212]")

### mask for [17417 17446]
mask_17417_17446 = core.imwri.Read(r'masks\25_Gurren_Lagann_17417.webp') + core.imwri.Read(r'masks\25_Gurren_Lagann_17446.webp')
mask_17417_17446 = ToRGB(mask_17417_17446, 1, 32)
mask_17417_17446 = core.rife.RIFE(mask_17417_17446, model=24, factor_num=29, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_17417_17446 = core.fmtc.bitdepth(mask_17417_17446, bits=16)
mask_17417_17446 = core.std.Trim(mask_17417_17446, 0, 28)
#
masked_17417_17446 = core.std.MaskedMerge(DD_clip.std.Trim(17417, 17446), strongest_denoise_deband.std.Trim(17417, 17446), mask_17417_17446, planes=[0,1,2], first_plane=True)

DD_clip = core.std.Trim(DD_clip, 0, 17416) + masked_17417_17446 + core.std.Trim(DD_clip, 17447, src.num_frames-1)

### mask for [17447 17475]
mask_17447_17475 = core.imwri.Read(r'masks\25_Gurren_Lagann_17447.webp') + core.imwri.Read(r'masks\25_Gurren_Lagann_17475.webp')
mask_17447_17475 = ToRGB(mask_17447_17475, 1, 32)
mask_17447_17475 = core.rife.RIFE(mask_17447_17475, model=24, factor_num=28, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_17447_17475 = core.fmtc.bitdepth(mask_17447_17475, bits=16)
mask_17447_17475 = core.std.Trim(mask_17447_17475, 0, 27)
#
masked_17447_17475 = core.std.MaskedMerge(DD_clip.std.Trim(17447, 17475), strongest_denoise_deband.std.Trim(17447, 17475), mask_17447_17475, planes=[0,1,2], first_plane=True)

DD_clip = core.std.Trim(DD_clip, 0, 17446) + masked_17447_17475 + core.std.Trim(DD_clip, 17476, src.num_frames-1)

### mask for [29844 29891]
mask_29844_29891 = core.imwri.Read(r'masks\25_Gurren_Lagann_29844.webp') + core.imwri.Read(r'masks\25_Gurren_Lagann_29891.webp')
mask_29844_29891 = ToRGB(mask_29844_29891, 1, 32)
mask_29844_29891 = core.rife.RIFE(mask_29844_29891, model=24, factor_num=47, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_29844_29891 = core.fmtc.bitdepth(mask_29844_29891, bits=16)
mask_29844_29891 = core.std.Trim(mask_29844_29891, 0, 46)
#
masked_29844_29891 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(29844, 29891), strongest_denoise_deband.std.Trim(29844, 29891), mask_29844_29891, planes=[0,1,2], first_plane=True)

DD_clip = core.std.Trim(DD_clip, 0, 29843) + masked_29844_29891 + core.std.Trim(DD_clip, 29892, src.num_frames-1)

final = depth(DD_clip, 10)

set_output(final)