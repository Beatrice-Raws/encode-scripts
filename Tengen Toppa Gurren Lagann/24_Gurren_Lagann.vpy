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
ep_ed_start = 32489
ep_ed_end = 34646

# descale/rescale & AA
ep_AA_clip = main_AA(src, credit_mask=False)

op_AA_clip = ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(0, 1422) + core.std.Trim(ncop_v3_aa, 1423, 1542) + ApplyCredits(ep_op, ncop_v3, ncop_v3_aa).std.Trim(1543, 2158)

AA_clip = op_AA_clip + core.std.Trim(ep_AA_clip, 2159, ep_ed_start-1) + core.std.Trim(op_ed_AA_2(src, credit_mask=True), ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

eedi_AA_YUV = eedi_AA_YUV(AA_clip)
strong_eedi_AA = strong_eedi_AA(src)
very_strong_eedi_AA = very_strong_eedi_AA(src)

AA_clip = fvf.rfs(AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(src), mappings="[5109 5246] [32393 32488] [32393 32488]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src), mappings="[5570 5570] [7589 7589] [8160 8160] [12341 12347] [12971 13014] [13023 13036] [13042 13071] [13155 13214] [16963 16963] [17002 17002] [17446 17698] [18141 18585] [19456 19458] [19846 20318] [23345 23361] [26419 26506] [30505 30513] [30563 30571]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src), mappings="[3369 3515] 4889 5569 [6789 6791] 7588 8159 [9499 9534] [12935 12970] [15447 15448] 16962 19455 [22974 23050] [25259 25273] [30502 30504] [30550 30562] [30594 30599] [30775 30839]")
AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src, credit_mask=True), mappings="[17837 18134]")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="6789 8159 30500 30501")
AA_clip = fvf.rfs(AA_clip, strong_eedi_AA, mappings="[30496 30499]")
AA_clip = fvf.rfs(AA_clip, very_strong_eedi_AA, mappings="30495")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, very_strong_eedi_AA, r'masks\24_Gurren_Lagann_29235-29237.webp'), "[29235 29237]")

for i in range(29238, 29252):
    mask_path = fr'masks\24_Gurren_Lagann_{i}.webp'
    AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, very_strong_eedi_AA, mask_path), str(i))

AA_clip = fvf.rfs(AA_clip, main_AA(src, credit_mask=True), mappings="[2762 2870] [2992 3130] [4041 4132] [4338 4398] [17709 17787] [17800 17836] [34882 35018]")

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

simple_darkmask = core.fmtc.bitdepth(AA_clip, bits=8, dmode=9).std.Levels(min_in=0, max_in=40, min_out=0, max_out=255, planes=[0]).std.Invert().std.Levels(min_in=0, max_in=40, min_out=0, max_out=255, planes=[0]).std.Invert().fmtc.bitdepth(bits=16)

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[2167 2168] [3274 3368] [3776 3822] [5247 5247] [9519 9608] [10642 10904] [22056 22107] [22249 22320] [23861 24183]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30] [2169 2172] [5248 5249] [6036 6082] [9702 9814] [10403 10641] [12082 12152] [13086 13107] [13476 13498] [15079 15123] [16090 16400] [22321 22439] [23235 23298] [24330 24364] [26579 26673] [28931 28990] [29778 29860] [30840 31433] [31780 32004] [32047 32392]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] 1326 [2228 2259] [2287 2386] [4811 4827] [6363 6471] [7559 7564] [13215 13356] [19484 19524] [23394 23395] [30216 30242]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[2825 2870] [4828 4888] [6792 6811] [7565 7587] [19478 19483] [28200 28209] [28216 28235] [28242 28245] [28260 28269] [28272 28277] [28281 28282]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, strongest_denoise_deband, simple_darkmask), mappings="[29140 29234]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914] [2825 2870] [6792 6811] [19478 19483] [28200 28209] [28216 28235] [28242 28245] [28260 28269] [28272 28277] [28281 28282]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((10.0, 0), 0.85, Catrom, True, luma_scaling=1).grain(core.neo_f3kdb.Deband(denoise_deband_strongest(AA_clip, thSAD=120, thr=12.0, sigma=2.0))), mappings="[23299 23311] [23336 23353]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[2287 2386] [6363 6471] [19484 19524]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542] [2825 2870] [6792 6811] [19478 19483]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942] [28200 28209] [28216 28235] [28242 28245] [28260 28269] [28272 28277] [28281 28282]")

final = depth(DD_clip, 10)

set_output(final)