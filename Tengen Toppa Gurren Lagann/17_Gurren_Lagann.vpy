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

sangnom_AA = sangnom_AA(src)
strong_AA = strong_AA(src)
very_strong_AA = very_strong_AA(src)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA(src), mappings="[3635 3771] [3952 4277] [4669 4950] [6602 6661] [7017 7274] [7876 8127] [8361 8456] [10540 10602] [10607 10648] [12440 12442] [12807 13015] [13701 13843] [15572 15618] [17168 17199] [17351 17369] [17406 17428] [20711 21201] [21739 21960] [22720 22778] [22903 22945] [24664 24695] [26017 26159] [26406 26572] [27161 27261] [27380 27431] [27827 27963] [28461 28490] [28753 28960] [29269 29352] [29732 29964] [30300 30363] [31160 31224]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(src), mappings="26858 34894")
AA_clip = fvf.rfs(AA_clip, eedi_AA_YUV(src), mappings="[24508 24600] [24696 24816] [26911 26956] [26999 27036] [27617 27676] [30061 30095] [30149 30240] [30364 30704]")
AA_clip = fvf.rfs(AA_clip, sangnom_AA, mappings="[4590 4594] [10604 10606] [34892 34893]")
AA_clip = fvf.rfs(AA_clip, santiag(AA_clip, type='sangnom', aa=128), mappings="[30061 30063]")
AA_clip = fvf.rfs(AA_clip, strong_AA, mappings="12439")
AA_clip = fvf.rfs(AA_clip, very_strong_AA, mappings="10603 26910 34891")
AA_clip = fvf.rfs(AA_clip, strongest_AA(src), mappings="26909")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, eedi_AA_YUV(src), r'masks\17_Gurren_Lagann_26716-26756.webp'), "[26716 26756]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, santiag(AA_clip, type='eedi3'), r'masks\17_Gurren_Lagann_26716-26756.webp'), "[26716 26756]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, santiag(AA_clip, type='eedi3'), r'masks\17_Gurren_Lagann_26716-26756.webp'), "[26716 26756]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, santiag(AA_clip, type='eedi3'), r'masks\17_Gurren_Lagann_26716-26756.webp'), "[26716 26756]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, santiag(AA_clip, type='eedi3'), r'masks\17_Gurren_Lagann_26716-26756.webp'), "[26716 26756]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, santiag(AA_clip, type='sangnom'), r'masks\17_Gurren_Lagann_26716-26756.webp'), "[26716 26756]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, santiag(AA_clip, type='sangnom'), r'masks\17_Gurren_Lagann_26716-26756.webp'), "[26716 26756]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, santiag(AA_clip, type='sangnom'), r'masks\17_Gurren_Lagann_26716-26756.webp'), "[26716 26756]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\17_Gurren_Lagann_31160-31207.webp'), "[31160 31207]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, r'masks\17_Gurren_Lagann_31208-31224.webp'), "[31208 31224]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\17_Gurren_Lagann_4610-4628.webp'), "[4610 4628]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, strong_AA, r'masks\17_Gurren_Lagann_31160-31207v2.webp'), "[31160 31207]")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, very_strong_AA, r'masks\17_Gurren_Lagann_4606.webp'), "4606")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, very_strong_AA, r'masks\17_Gurren_Lagann_4607.webp'), "4607")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(src, AA_clip, r'masks\17_Gurren_Lagann_34891-35020.webp'), "[34891 35020]")
AA_clip = fvf.rfs(AA_clip, ApplyStab(AA_clip), mappings="[13016 13141] [21632 21738]")

AA_clip = fvf.rfs(AA_clip, main_AA(src, credit_mask=True), mappings="[2161 2255] [2265 2393] [32395 32490] [34673 34732]")

# denoise, deband & regrain

### mask for [19958 20023]
img_19958_20023 = core.imwri.Read(r'masks\17_Gurren_Lagann_19958-20023.webp').std.AddBorders(left=0, right=33, top=0, bottom=0, color=[0, 0, 0]).std.AssumeFPS(fpsnum=24000, fpsden=1001)

mask_19958_20023 = reduce(
    lambda x, y: x+y,
    [
        core.std.Crop(img_19958_20023, left=(0+t), right=(33-t))
        for t in range(1, 34)
    ]
).std.SelectEvery(cycle=2, offsets=[0, 0, 1, 1]).std.AssumeFPS(fpsnum=24000, fpsden=1001).fmtc.bitdepth(bits=16)
###

### mask for [20033 20154]
img_20033_20154 = core.imwri.Read(r'masks\17_Gurren_Lagann_20033-20154.webp').std.AddBorders(left=0, right=61, top=0, bottom=0, color=[0, 0, 0]).std.AssumeFPS(fpsnum=24000, fpsden=1001)

mask_20033_20154 = reduce(
    lambda x, y: x+y,
    [
        core.std.Crop(img_20033_20154, left=(0+t), right=(61-t))
        for t in range(1, 62)
    ]
).std.SelectEvery(cycle=2, offsets=[0, 0, 1, 1]).std.AssumeFPS(fpsnum=24000, fpsden=1001).fmtc.bitdepth(bits=16).std.Trim(0, 120)
###

### mask for [20538 20564]
mask_20538_20564 = core.imwri.Read(r'masks\17_Gurren_Lagann_20538.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_20564.webp')
mask_20538_20564 = ToRGB(mask_20538_20564, 1, 32)
mask_20538_20564 = core.rife.RIFE(mask_20538_20564, model=9, factor_num=26, factor_den=1)
mask_20538_20564 = core.std.Trim(mask_20538_20564, 0, 26).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [20565 20612]
mask_20565_20612 = core.imwri.Read(r'masks\17_Gurren_Lagann_20565.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_20612.webp')
mask_20565_20612 = ToRGB(mask_20565_20612, 1, 32)
mask_20565_20612 = core.rife.RIFE(mask_20565_20612, model=9, factor_num=47, factor_den=1)
mask_20565_20612 = core.std.Trim(mask_20565_20612, 0, 47).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [22740 22745]
mask_22740_22745 = core.imwri.Read(r'masks\17_Gurren_Lagann_22740.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_22745.webp')
mask_22740_22745 = ToRGB(mask_22740_22745, 1, 32)
mask_22740_22745 = core.rife.RIFE(mask_22740_22745, model=9, factor_num=5, factor_den=1)
mask_22740_22745 = core.std.Trim(mask_22740_22745, 0, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [22746 22749]
mask_22746_22749 = core.imwri.Read(r'masks\17_Gurren_Lagann_22745.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_22750.webp')
mask_22746_22749 = ToRGB(mask_22746_22749, 1, 32)
mask_22746_22749 = core.rife.RIFE(mask_22746_22749, model=9, factor_num=5, factor_den=1)
mask_22746_22749 = core.std.Trim(mask_22746_22749, 1, 4).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [22750 22778]
mask_22750_22778 = core.imwri.Read(r'masks\17_Gurren_Lagann_22750.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_22760.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_22770.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_22778.webp')
mask_22750_22778 = ToRGB(mask_22750_22778, 1, 32)
mask_22750_22778 = core.rife.RIFE(mask_22750_22778, model=9, factor_num=93, factor_den=10)
mask_22750_22778 = core.std.Trim(mask_22750_22778, 0, 28).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30149 30154]
mask_30149_30154 = core.imwri.Read(r'masks\17_Gurren_Lagann_30149.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30154.webp')
mask_30149_30154 = ToRGB(mask_30149_30154, 1, 32)
mask_30149_30154 = core.rife.RIFE(mask_30149_30154, model=9, factor_num=5, factor_den=1)
mask_30149_30154 = core.std.Trim(mask_30149_30154, 0, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30155 30159]
mask_30155_30159 = core.imwri.Read(r'masks\17_Gurren_Lagann_30154.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30159.webp')
mask_30155_30159 = ToRGB(mask_30155_30159, 1, 32)
mask_30155_30159 = core.rife.RIFE(mask_30155_30159, model=9, factor_num=5, factor_den=1)
mask_30155_30159 = core.std.Trim(mask_30155_30159, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30160 30164]
mask_30160_30164 = core.imwri.Read(r'masks\17_Gurren_Lagann_30159.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30164.webp')
mask_30160_30164 = ToRGB(mask_30160_30164, 1, 32)
mask_30160_30164 = core.rife.RIFE(mask_30160_30164, model=9, factor_num=5, factor_den=1)
mask_30160_30164 = core.std.Trim(mask_30160_30164, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30165 30169]
mask_30165_30169 = core.imwri.Read(r'masks\17_Gurren_Lagann_30164.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30169.webp')
mask_30165_30169 = ToRGB(mask_30165_30169, 1, 32)
mask_30165_30169 = core.rife.RIFE(mask_30165_30169, model=9, factor_num=5, factor_den=1)
mask_30165_30169 = core.std.Trim(mask_30165_30169, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30170 30174]
mask_30170_30174 = core.imwri.Read(r'masks\17_Gurren_Lagann_30169.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30174.webp')
mask_30170_30174 = ToRGB(mask_30170_30174, 1, 32)
mask_30170_30174 = core.rife.RIFE(mask_30170_30174, model=9, factor_num=5, factor_den=1)
mask_30170_30174 = core.std.Trim(mask_30170_30174, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30175 30179]
mask_30175_30179 = core.imwri.Read(r'masks\17_Gurren_Lagann_30174.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30179.webp')
mask_30175_30179 = ToRGB(mask_30175_30179, 1, 32)
mask_30175_30179 = core.rife.RIFE(mask_30175_30179, model=9, factor_num=5, factor_den=1)
mask_30175_30179 = core.std.Trim(mask_30175_30179, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30180 30184]
mask_30180_30184 = core.imwri.Read(r'masks\17_Gurren_Lagann_30179.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30184.webp')
mask_30180_30184 = ToRGB(mask_30180_30184, 1, 32)
mask_30180_30184 = core.rife.RIFE(mask_30180_30184, model=9, factor_num=5, factor_den=1)
mask_30180_30184 = core.std.Trim(mask_30180_30184, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30185 30189]
mask_30185_30189 = core.imwri.Read(r'masks\17_Gurren_Lagann_30184.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30189.webp')
mask_30185_30189 = ToRGB(mask_30185_30189, 1, 32)
mask_30185_30189 = core.rife.RIFE(mask_30185_30189, model=9, factor_num=5, factor_den=1)
mask_30185_30189 = core.std.Trim(mask_30185_30189, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30190 30194]
mask_30190_30194 = core.imwri.Read(r'masks\17_Gurren_Lagann_30189.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30194.webp')
mask_30190_30194 = ToRGB(mask_30190_30194, 1, 32)
mask_30190_30194 = core.rife.RIFE(mask_30190_30194, model=9, factor_num=5, factor_den=1)
mask_30190_30194 = core.std.Trim(mask_30190_30194, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30195 30199]
mask_30195_30199 = core.imwri.Read(r'masks\17_Gurren_Lagann_30194.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30199.webp')
mask_30195_30199 = ToRGB(mask_30195_30199, 1, 32)
mask_30195_30199 = core.rife.RIFE(mask_30195_30199, model=9, factor_num=5, factor_den=1)
mask_30195_30199 = core.std.Trim(mask_30195_30199, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30200 30204]
mask_30200_30204 = core.imwri.Read(r'masks\17_Gurren_Lagann_30199.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30204.webp')
mask_30200_30204 = ToRGB(mask_30200_30204, 1, 32)
mask_30200_30204 = core.rife.RIFE(mask_30200_30204, model=9, factor_num=5, factor_den=1)
mask_30200_30204 = core.std.Trim(mask_30200_30204, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30205 30209]
mask_30205_30209 = core.imwri.Read(r'masks\17_Gurren_Lagann_30204.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30209.webp')
mask_30205_30209 = ToRGB(mask_30205_30209, 1, 32)
mask_30205_30209 = core.rife.RIFE(mask_30205_30209, model=9, factor_num=5, factor_den=1)
mask_30205_30209 = core.std.Trim(mask_30205_30209, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30210 30214]
mask_30210_30214 = core.imwri.Read(r'masks\17_Gurren_Lagann_30209.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30214.webp')
mask_30210_30214 = ToRGB(mask_30210_30214, 1, 32)
mask_30210_30214 = core.rife.RIFE(mask_30210_30214, model=9, factor_num=5, factor_den=1)
mask_30210_30214 = core.std.Trim(mask_30210_30214, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30215 30219]
mask_30215_30219 = core.imwri.Read(r'masks\17_Gurren_Lagann_30214.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30219.webp')
mask_30215_30219 = ToRGB(mask_30215_30219, 1, 32)
mask_30215_30219 = core.rife.RIFE(mask_30215_30219, model=9, factor_num=5, factor_den=1)
mask_30215_30219 = core.std.Trim(mask_30215_30219, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30220 30224]
mask_30220_30224 = core.imwri.Read(r'masks\17_Gurren_Lagann_30219.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30224.webp')
mask_30220_30224 = ToRGB(mask_30220_30224, 1, 32)
mask_30220_30224 = core.rife.RIFE(mask_30220_30224, model=9, factor_num=5, factor_den=1)
mask_30220_30224 = core.std.Trim(mask_30220_30224, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30225 30229]
mask_30225_30229 = core.imwri.Read(r'masks\17_Gurren_Lagann_30224.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30229.webp')
mask_30225_30229 = ToRGB(mask_30225_30229, 1, 32)
mask_30225_30229 = core.rife.RIFE(mask_30225_30229, model=9, factor_num=5, factor_den=1)
mask_30225_30229 = core.std.Trim(mask_30225_30229, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
###

### mask for [30230 30234]
mask_30230_30234 = core.imwri.Read(r'masks\17_Gurren_Lagann_30229.webp') + core.imwri.Read(r'masks\17_Gurren_Lagann_30234.webp')
mask_30230_30234 = ToRGB(mask_30230_30234, 1, 32)
mask_30230_30234 = core.rife.RIFE(mask_30230_30234, model=9, factor_num=5, factor_den=1)
mask_30230_30234 = core.std.Trim(mask_30230_30234, 1, 5).fmtc.bitdepth(bits=16).std.AssumeFPS(fpsnum=24000, fpsden=1001)
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
strongest_denoise_deband = denoise_deband_strongest(AA_clip, thSAD=120, thr=12.0, sigma=2.0)

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="10958 [24879 24913] [27113 27160]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30] [2293 2709] [10959 10969] [17429 17458] [18568 18641] [20463 20528] [24874 24878] [27357 27379] [28702 28752] [29482 29533]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] [1326 1326] [4278 4335] [4383 4444] [4646 4668] [5540 5680] [12082 12218] [12290 12348] [18140 18180] [18701 18766] [18952 19034] [22946 22989] [24601 24663] [27380 27431] [28613 28635] [3141031544] [31770 31804]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[133 133] [151 159] [371 502] [1418 1423] [1540 1542] [1749 1914] [3312 3634] [3833 3951] [4575 4590] [5841 5849] [6224 6391] [8319 8360] [11032 11270] [11593 12081] [12219 12289] [12349 12438] [18135 18139] [18545 18567] [19035 19057] [22044 22078] [23095 23162] [25483 25544] [26858 26892] [27161 27261] [27964 28082] [31160 31224] [31545 31663]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="[21961 21966] [26406 26572] [29732 29964]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22499-22501.webp'), "[22499 22501] [22514 22516] [22529 22531] [22544 22546] [22559 22561] [22574 22576] [22589 22591] [22604 22606] [22619 22621] [22634 22636] [22649 22651] [22664 22666] [22679 22681]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22502-22504.webp'), "[22502 22504] [22517 22519] [22532 22534] [22547 22549] [22562 22564] [22577 22579] [22592 22594] [22607 22609] [22622 22624] [22637 22639] [22652 22654] [22667 22669] [22682 22684]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22505-22507.webp'), "[22505 22507] [22520 22522] [22535 22537] [22550 22552] [22565 22567] [22580 22582] [22595 22597] [22610 22612] [22625 22627] [22640 22642] [22655 22657] [22670 22672] [22685 22687]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22508-22510.webp'), "[22508 22510] [22523 22525] [22538 22540] [22553 22555] [22568 22570] [22583 22585] [22598 22600] [22613 22615] [22628 22630] [22643 22645] [22658 22660] [22673 22675] [22688 22690]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22511-22513.webp'), "[22511 22513] [22526 22528] [22541 22543] [22556 22558] [22571 22573] [22586 22588] [22601 22603] [22616 22618] [22631 22633] [22646 22648] [22661 22663] [22676 22678] [22691 22693]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22694-22696.webp'), "[22694 22696]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22697-22699.webp'), "[22697 22699]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22700-22702.webp'), "[22700 22702]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22703-22705.webp'), "[22703 22705]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22706-22708.webp'), "[22706 22708]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22709-22711.webp'), "[22709 22711]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22712-22714.webp'), "[22712 22714]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22715-22717.webp'), "[22715 22717]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, r'masks\17_Gurren_Lagann_22718-22719.webp'), "[22718 22719]")

for i in range(22720, 22740):
    mask_path = fr'masks\17_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_denoise_deband, mask_path), str(i))

for i in range(28461, 28491):
    mask_path = fr'masks\17_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_denoise_deband, mask_path), str(i))

for i in range(30461, 30512):
    mask_path = fr'masks\17_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, strongest_denoise_deband, r'masks\17_Gurren_Lagann_29269-29352.webp'), "[29269 29352]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(strong_denoise_deband, strongest_denoise_deband, r'masks\17_Gurren_Lagann_20529-20531.webp'), "[20529 20531]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(strong_denoise_deband, strongest_denoise_deband, r'masks\17_Gurren_Lagann_20532-20534.webp'), "[20532 20534]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(strong_denoise_deband, strongest_denoise_deband, r'masks\17_Gurren_Lagann_20535-20537.webp'), "[20535 20537]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_denoise_deband, r'masks\17_Gurren_Lagann_19241-19294.webp'), "[19241 19294]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_denoise_deband, r'masks\17_Gurren_Lagann_20024-20026.webp'), "[20024 20026]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_denoise_deband, r'masks\17_Gurren_Lagann_20027-20029.webp'), "[20027 20029]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_denoise_deband, r'masks\17_Gurren_Lagann_20030-20032.webp'), "[20030 20032]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_denoise_deband, r'masks\17_Gurren_Lagann_21967-21968.webp'), "[21967 21968]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_denoise_deband, r'masks\17_Gurren_Lagann_21969-21970.webp'), "[21969 21970]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strongest_denoise_deband, r'masks\17_Gurren_Lagann_28202-28315.webp'), "[28202 28315]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, DD_clip, r'masks\17_Gurren_Lagann_30234.webp'), "[30235 30240]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(very_strong_denoise_deband, strongest_denoise_deband, r'masks\17_Gurren_Lagann_22779-22902.webp'), "[22779 22902]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914] [22044 22078] [25483 25544] [26968 26998] [28202 28315]")

masked_19958_20023 = core.std.MaskedMerge(DD_clip.std.Trim(19958, 20023), strongest_denoise_deband.std.Trim(19958, 20023), mask_19958_20023, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 19957) + masked_19958_20023 + core.std.Trim(DD_clip, 20024, src.num_frames-1)

masked_20033_20154 = core.std.MaskedMerge(DD_clip.std.Trim(20033, 20154), strongest_denoise_deband.std.Trim(20033, 20154), mask_20033_20154, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 20032) + masked_20033_20154 + core.std.Trim(DD_clip, 20155, src.num_frames-1)

masked_20538_20564 = core.std.MaskedMerge(strong_denoise_deband.std.Trim(20538, 20564), strongest_denoise_deband.std.Trim(20538, 20564), mask_20538_20564, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 20537) + masked_20538_20564 + core.std.Trim(DD_clip, 20565, src.num_frames-1)

masked_20565_20612 = core.std.MaskedMerge(DD_clip.std.Trim(20565, 20612), strongest_denoise_deband.std.Trim(20565, 20612), mask_20565_20612, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 20564) + masked_20565_20612 + core.std.Trim(DD_clip, 20613, src.num_frames-1)

masked_22740_22745 = core.std.MaskedMerge(weak_denoise_deband.std.Trim(22740, 22745), very_strong_denoise_deband.std.Trim(22740, 22745), mask_22740_22745, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 22739) + masked_22740_22745 + core.std.Trim(DD_clip, 22746, src.num_frames-1)

masked_22746_22749 = core.std.MaskedMerge(weak_denoise_deband.std.Trim(22746, 22749), very_strong_denoise_deband.std.Trim(22746, 22749), mask_22746_22749, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 22745) + masked_22746_22749 + core.std.Trim(DD_clip, 22750, src.num_frames-1)

masked_22750_22778 = core.std.MaskedMerge(weak_denoise_deband.std.Trim(22750, 22778), very_strong_denoise_deband.std.Trim(22750, 22778), mask_22750_22778, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 22749) + masked_22750_22778 + core.std.Trim(DD_clip, 22779, src.num_frames-1)

masked_30149_30154 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30149, 30154), DD_clip.std.Trim(30149, 30154), mask_30149_30154, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30148) + masked_30149_30154 + core.std.Trim(DD_clip, 30155, src.num_frames-1)

masked_30155_30159 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30155, 30159), DD_clip.std.Trim(30155, 30159), mask_30155_30159, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30154) + masked_30155_30159 + core.std.Trim(DD_clip, 30160, src.num_frames-1)

masked_30160_30164 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30160, 30164), DD_clip.std.Trim(30160, 30164), mask_30160_30164, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30159) + masked_30160_30164 + core.std.Trim(DD_clip, 30165, src.num_frames-1)

masked_30165_30169 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30165, 30169), DD_clip.std.Trim(30165, 30169), mask_30165_30169, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30164) + masked_30165_30169 + core.std.Trim(DD_clip, 30170, src.num_frames-1)

masked_30170_30174 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30170, 30174), DD_clip.std.Trim(30170, 30174), mask_30170_30174, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30169) + masked_30170_30174 + core.std.Trim(DD_clip, 30175, src.num_frames-1)

masked_30175_30179 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30175, 30179), DD_clip.std.Trim(30175, 30179), mask_30175_30179, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30174) + masked_30175_30179 + core.std.Trim(DD_clip, 30180, src.num_frames-1)

masked_30180_30184 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30180, 30184), DD_clip.std.Trim(30180, 30184), mask_30180_30184, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30179) + masked_30180_30184 + core.std.Trim(DD_clip, 30185, src.num_frames-1)

masked_30185_30189 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30185, 30189), DD_clip.std.Trim(30185, 30189), mask_30185_30189, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30184) + masked_30185_30189 + core.std.Trim(DD_clip, 30190, src.num_frames-1)

masked_30190_30194 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30190, 30194), DD_clip.std.Trim(30190, 30194), mask_30190_30194, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30189) + masked_30190_30194 + core.std.Trim(DD_clip, 30195, src.num_frames-1)

masked_30195_30199 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30195, 30199), DD_clip.std.Trim(30195, 30199), mask_30195_30199, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30194) + masked_30195_30199 + core.std.Trim(DD_clip, 30200, src.num_frames-1)

masked_30200_30204 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30200, 30204), DD_clip.std.Trim(30200, 30204), mask_30200_30204, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30199) + masked_30200_30204 + core.std.Trim(DD_clip, 30205, src.num_frames-1)

masked_30205_30209 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30205, 30209), DD_clip.std.Trim(30205, 30209), mask_30205_30209, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30204) + masked_30205_30209 + core.std.Trim(DD_clip, 30210, src.num_frames-1)

masked_30210_30214 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30210, 30214), DD_clip.std.Trim(30210, 30214), mask_30210_30214, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30209) + masked_30210_30214 + core.std.Trim(DD_clip, 30215, src.num_frames-1)

masked_30215_30219 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30215, 30219), DD_clip.std.Trim(30215, 30219), mask_30215_30219, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30214) + masked_30215_30219 + core.std.Trim(DD_clip, 30220, src.num_frames-1)

masked_30220_30224 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30220, 30224), DD_clip.std.Trim(30220, 30224), mask_30220_30224, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30219) + masked_30220_30224 + core.std.Trim(DD_clip, 30225, src.num_frames-1)

masked_30225_30229 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30225, 30229), DD_clip.std.Trim(30225, 30229), mask_30225_30229, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30224) + masked_30225_30229 + core.std.Trim(DD_clip, 30230, src.num_frames-1)

masked_30230_30234 = core.std.MaskedMerge(weakest_denoise_deband.std.Trim(30230, 30234), DD_clip.std.Trim(30230, 30234), mask_30230_30234, planes=[0,1,2], first_plane=True)
DD_clip = core.std.Trim(DD_clip, 0, 30229) + masked_30230_30234 + core.std.Trim(DD_clip, 30235, src.num_frames-1)

DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((1.5, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[22694 22778]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542] [21961 21966] [23095 23162] [26968 26998]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942] [22044 22078] [25483 25544] [26406 26572] [29732 29964]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), r'masks\17_Gurren_Lagann_21967-21968.webp'), "[21967 21968]")
DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), r'masks\17_Gurren_Lagann_21969-21970.webp'), "[21969 21970]")

final = depth(DD_clip, 10)

set_output(final)