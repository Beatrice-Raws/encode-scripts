# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00004.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ep_ed_start = 32487
ep_ed_end = 34644

# descale/rescale & AA
op_ed_AA_clip = op_ed_AA(src)
ep_AA_clip = main_AA(src, credit_mask=False)

AA_clip = core.std.Trim(ep_AA_clip, 0, ep_ed_start-1) + core.std.Trim(op_ed_AA_clip, ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

weak_eedi_AA = weak_eedi_AA(src)
very_strong_AA = very_strong_AA(src)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA, mappings="[97 120] [796 865] [3482 3633] [3986 4009] [5092 5143] [5274 5428] [5578 5990] [6263 6367] [7762 8033] [12059 12135] [16304 16357] [16393 16451] [16849 16943] [18004 18026] [18852 18898] [19601 19675] [20432 20495] [20866 20909] [21140 21159] [24248 24253] [26751 26780]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src), mappings="[4397 4419] 5233 8995 [14468 14470] 24255 [28529 28672] [34731 34733]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA(src), mappings="[4520 4524] 34730")
AA_clip = fvf.rfs(AA_clip, strong_AA(src), mappings="25084 34729")
AA_clip = fvf.rfs(AA_clip, very_strong_AA, mappings="5232 8994 18029 25025 25113")
AA_clip = fvf.rfs(AA_clip, strongest_AA(src), mappings="24254")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, very_strong_AA, r'masks\15_Gurren_Lagann_4500.webp'), "4500")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, weak_eedi_AA, r'masks\15_Gurren_Lagann_4628-4668.webp'), "[4628 4668]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(src), r'masks\15_Gurren_Lagann_4628-4668_dt.webp'), "[4628 4668]")

AA_clip = fvf.rfs(AA_clip, main_AA(AA_clip, credit_mask=True), mappings="[34941 35016]")

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
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="4500 [22616 22622]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[8 9] [175 298] [1027 1151] [2220 2254] [2492 2707] [3096 3356] [3492 3655] [3931 3986] [4488 4499] [4628 4668] [4788 4827] [5274 5428] [5495 6367] [6775 6869] [6912 6988] [8154 8243] [8296 8378] [9864 10001] [11288 11441] [11532 12007] [12405 12464] [12558 12592] [12872 13002] [13063 13134] [14050 14096] [14829 14899] [17899 17979] [19197 19245] [19329 19392] [19429 19457] [21160 21242] [22614 22615] [23587 23603] [24148 24206] [27275 27309] [27568 27728] [28308 28366] [29068 29155] [29215 29301] [29832 30272] [30492 30857] [30920 31079]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[3756 3779] [3839 3873] [4520 4627] [8379 8418] [9285 9339] [9347 9416] [10477 10511] [10580 10594] [10850 10891] [12534 12557] [13295 13382] [13661 13703] [13661 13704] [13750 13809] [14308 14395] [15567 15795] [16128 16199] [16992 17254] [18447 18511] [18534 18921] [19128 19196] [19785 19910] [20028 20207] [20527 20530] [20536 20537] [20833 20927] [21310 21515] [21587 21693] [21917 22191] [22305 22363] [22609 22613] [22670 22704] [22762 22796] [22868 22949] [23022 23056] [23080 23511] [24088 24147] [24207 24637] [26727 26809] [29161 29214]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[72 150] [3464 3481] [4241 4377] [4984 5016] [6989 7059] [8419 8895] [9340 9346] [10542 10579] [10658 10800] [10948 11055] [11176 11222] [12232 12314] [13571 13660] [14396 14467] [14503 14543] [14698 14740] [15184 15207] [15796 15867] [15915 15985] [17386 17478] [18127 18209] [19512 19628] [19676 19699] [19934 19954] [19783 19784] [19911 19980] [20237 20495] [20531 20532] [21116 21139] [22192 22263] [22382 22422] [23923 24087] [24728 24831] [24952 25024] [25114 25266] [29156 29160]")
DD_clip = fvf.rfs(DD_clip, core.std.MaskedMerge(DD_clip, very_strong_denoise_deband, simple_darkmask), mappings="[19700 19757]")
DD_clip = fvf.rfs(DD_clip, denoise_deblock(AA_clip), mappings="[20496 20526] [20538 20593]")
DD_clip = fvf.rfs(DD_clip, denoise_deband(DD_clip, thSAD=65, thr=3.5, sigma=1.4), mappings="[20496 20526] [20538 20593]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="[16281 16357] [26248 26288]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, r'masks\15_Gurren_Lagann_13003-13062.webp'), "[13003 13062]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, very_strong_denoise_deband, r'masks\15_Gurren_Lagann_19079-19127.webp'), "[19079 19127]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, very_strong_denoise_deband, r'masks\15_Gurren_Lagann_19393-19420.webp'), "[19393 19420]")

for i in range(19421, 19428):
    mask_path = fr'masks\15_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, very_strong_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, very_strong_denoise_deband, r'masks\15_Gurren_Lagann_20533.webp'), "20533")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, very_strong_denoise_deband, r'masks\15_Gurren_Lagann_20534.webp'), "20534")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, very_strong_denoise_deband, r'masks\15_Gurren_Lagann_20535.webp'), "20535")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(strong_denoise_deband, weak_denoise_deband, r'masks\13_Gurren_Lagann_31272-31631.webp'), "[4570 4625] 4627")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_denoise_deband, r'masks\15_Gurren_Lagann_31508-31639.webp'), "[31508 31639]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, r'masks\15_Gurren_Lagann_3656-3702.webp'), "[3656 3702]")

for i in range(4503, 4520):
    mask_path = fr'masks\15_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, r'masks\15_Gurren_Lagann_4626.webp'), "4626")

for i in range(4669, 4723):
    mask_path = fr'masks\15_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, r'masks\15_Gurren_Lagann_28529.webp'), "28529")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, r'masks\15_Gurren_Lagann_28530.webp'), "28530")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[72 150]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[3656 3702] [4501 4519] [4669 4722] [4984 5016] [8419 8856] [10542 10579] [10658 10800] [10948 11055] [12232 12314] [14698 14740] [15796 15867] [16281 16357] [19512 19675] [19864 19980] [20496 20627] [22192 22263] [23923 24064] [24728 24831] [24952 25025] 25084 [25114 25266] [26248 26288]")

final = depth(DD_clip, 10)

set_output(final)