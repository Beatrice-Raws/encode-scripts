# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00003.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ep_ed_start = 32487
ep_ed_end = 34644

# layer compositing errors fix
layer_error_fix = src.std.Trim(238, 238)
layer_error_fix = layer_error_fix.std.Crop(left=850, right=1020, top=580, bottom=450)
layer_error_fix = haf.Overlay(src, layer_error_fix, x=850, y=580)
layer_error_fix = fvf.rfs(src, layer_error_fix, mappings="[239 252]")

loaded_images = {}

ranges_to_load = [
    (639, 651),
    (661, 677),
    (687, 693)
]

for start, end in ranges_to_load:
    for i in range(start, end):
        path = rf'img_fix\09_Gurren_Lagann_{i}.webp'
        loaded_images[i] = core.imwri.Read(path)

for frame_num in loaded_images.keys():
    image_clip = loaded_images[frame_num]
    layer_error_fix = rfs_img(layer_error_fix, image_clip, [frame_num])

layer_error_fix2 = layer_error_fix.std.Trim(13460, 13460)
layer_error_fix2 = layer_error_fix2.std.Crop(left=140, right=1450, top=380, bottom=240)
layer_error_fix2 = haf.Overlay(layer_error_fix, layer_error_fix2, x=140, y=380)
layer_error_fix2 = fvf.rfs(layer_error_fix, layer_error_fix2, mappings="[13461 13490]")

layer_error_fix3 = layer_error_fix2.std.Trim(14786, 14786)
layer_error_fix3 = layer_error_fix3.std.Crop(left=60, right=1720, top=964, bottom=60)
layer_error_fix3 = haf.Overlay(layer_error_fix2, layer_error_fix3, x=60, y=964)
layer_error_fix3 = fvf.rfs(layer_error_fix2, layer_error_fix3, mappings="[14744 14785]")

layer_error_fix = layer_error_fix3

# descale/rescale & AA
op_ed_AA_clip = op_ed_AA(layer_error_fix)
ep_AA_clip = main_AA(layer_error_fix, credit_mask=False)

AA_clip = core.std.Trim(op_ed_AA_clip, 0, 2157) + core.std.Trim(ep_AA_clip, 2158, ep_ed_start-1) + core.std.Trim(op_ed_AA_clip, ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

weak_eedi_AA = weak_eedi_AA(layer_error_fix)
sangnom_AA = sangnom_AA(layer_error_fix)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA, mappings="[1086 1109] [1260 1276] [1545 1598] 1749 [7493 7499] 8271 8307 8309 [8930 9283] [12118 12272] [13834 13945] [14017 14039] [14203 14214] [14277 14278] [14303 14304] [14439 14636] [14881 14928] [15270 15298] [16975 16978] [17311 17412] [17579 17644] [18012 18044] [20269 20280] [24473 24486] [24997 25068] [26219 26289] [27321 27371] [28257 28412] [29049 29168] [31273 31319] [31646 31728]")
AA_clip = fvf.rfs(AA_clip, eedi_AA(layer_error_fix), mappings="7492 [14275 14276] [14300 14302] 23577 27822")
AA_clip = fvf.rfs(AA_clip, sangnom_AA, mappings="[256 371]")
AA_clip = fvf.rfs(AA_clip, strong_AA(layer_error_fix), mappings="14274 14299")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, weak_eedi_AA, r'masks\14_Gurren_Lagann_6986-7045.webp'), "[6986 7045]")

for i in range(13876, 13910):
    mask_path = fr'masks\14_Gurren_Lagann_{i}.webp'
    AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, sangnom_AA, mask_path), str(i))

AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[763 879] [1110 1139] [2171 2297] [4875 5071] [6849 6913] [11465 11541] [34870 35016]")

### mask for [17774 17869] start
### a ready-made solution from https://forum.doom9.org/showthread.php?p=1902940#post1902940 was used
white = core.std.BlankClip(width=1920, height=1080, length=96, fpsnum=2997, fpsden=125, color=[255, 255, 255])
black = core.std.BlankClip(width=210, height=248, length=96, fpsnum=2997, fpsden=125, color=[0, 0, 0])
fromx=1575
tox=1527
fromy=290
toy=290
before = haf.Overlay(white, black, fromx, fromy)
after = haf.Overlay(white, black, tox, toy)

def MoveOverlay(n, white, black, fromx, tox, fromy, toy, startframe, endframe):
    if n < startframe:
      return before
    elif n > endframe:
      return after
    else:
      return haf.Overlay(white, black, round(fromx + (tox - fromx)/(endframe - startframe) * (n - startframe)), round(fromy + (toy - fromy)/(endframe - startframe) * (n - startframe)))

mask_17774_17869 = core.std.FrameEval(white, functools.partial(MoveOverlay, white=white,black=black, fromx=fromx, tox=tox, fromy=fromy, toy=toy, startframe=0, endframe=95)).fmtc.bitdepth(bits=16)
mask_17774_17869 = core.std.MaskedMerge(DescaleTarget(width=1280, height=720, kernel=Lanczos(3), credit_mask=False).get_upscaled(layer_error_fix).std.Trim(17774, 17869), weak_eedi_AA.std.Trim(17774, 17869), mask_17774_17869, planes=[0,1,2], first_plane=True)
mask_17774_17869 = core.std.Trim(AA_clip, 0, 17773) + mask_17774_17869 + core.std.Trim(AA_clip, 17870, src.num_frames-1)
### mask for [17774 17869] end

# denoise, deband & regrain
weakest_denoise_deband = denoise_deband(mask_17774_17869, thSAD=32, thr=1.5, sigma=0.7)
weak_denoise_deband = denoise_deband(mask_17774_17869, thSAD=65, thr=2.0, sigma=1.0)

main_denoise_deband = denoise_deband(mask_17774_17869, thSAD=65, thr=3.5, sigma=1.4)
noise1 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, True, luma_scaling=6).grain(main_denoise_deband)
noise2 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, False, luma_scaling=6).grain(main_denoise_deband)
main_denoise_deband = core.std.Expr([noise1, noise2], 'x {strength} * y 1 {strength} - * +'.format(strength=0.5))

strong_denoise_deband = denoise_deband(mask_17774_17869, thSAD=65, thr=5.0, sigma=1.6)
strong_denoise_deband = AddNoise.GAUSS((1.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(strong_denoise_deband)

very_strong_denoise_deband = denoise_deband_strong(mask_17774_17869, thSAD=120, thr=8.0, sigma=2.0)
strongest_denoise_deband = denoise_deband_strongest(mask_17774_17869, thSAD=120, thr=12.0, sigma=2.0)

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[1423 1435] [1536 1538] 1544 [1628 1674] [23470 23528] [28623 28642] [28745 28798]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [696 726] [826 879] [1110 1139] [1187 1259] [1319 1391] [1399 1416] [1419 1422] [1539 1583] [1616 1627] [1884 1916] [1939 1992] [2302 2308] [7492 7555] [11080 11245] [11542 11697] [11856 11986] [15740 15822] [17311 17412] [17774 17964] [18575 18760] [20447 20494] [21104 21139] [21313 21467] [21765 21859] [22643 22701] [22761 22850] [23470 23528] [23683 24055] [24569 24633] [25539 25567] [26219 26468] [27793 27821] [28051 28051] [28413 28518] [30974 31152] [31273 31319] [31559 31586] [34879 34892]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 501] [633 695] [763 825] [880 917] [1392 1398] [1417 1418] [1590 1615] [1675 1681] [5370 5812] [7141 7366] [8314 8325] [9792 9821] [10117 10136] 10637 10638 10641 [12283 12288] [12315 12320] [12398 12424] [13946 13968] [14637 14743] [15496 15572] [16528 16581] [16755 16813] [16856 16974] [17046 17243] [18054 18080] [18086 18105] [18324 18574] [19200 19202] [19219 19269] [20287 20322] [20518 20596] [23173 23303] [23529 23576] [24056 24233] [25130 25235] [25272 25408] [25511 25538] [25883 25908] [26923 27029] [27321 27482] [27912 27971] [28643 28673] [28799 28857] [29592 29700] [29902 29936] [30260 30366] [30461 30937] [31646 31728] [31985 32044] [34904 34918] [34929 34942]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="10639 10640 10643 [19197 19199] [20425 20427] [20599 20601] [23101 23172] [23304 23410] [24634 24692] [28224 28412] [28519 28602] [29299 29340]")
DD_clip = fvf.rfs(DD_clip, strongest_denoise_deband, mappings="10642 [13702 13705] [20597 20598]")
DD_clip = fvf.rfs(DD_clip, denoise_deband_strongest(DD_clip, thSAD=120, thr=4.0, y=32, sigma=2.0), mappings="[13706 13833]")

for i in range(1436, 1535):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, r'masks\09_Gurren_Lagann_1535.webp'), "1535")

for i in range(27822, 27912):
    mask_path = fr'masks\14_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

for i in range(28603, 28623):
    mask_path = fr'masks\14_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

for i in range(29204, 29299):
    mask_path = fr'masks\14_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

### mask for [1421 1526]
mask_1421_1526 = core.imwri.Read(r'masks\02_Gurren_Lagann_1421.webp') + core.imwri.Read(r'masks\09_Gurren_Lagann_1526.webp')
mask_1421_1526 = ToRGB(mask_1421_1526, 1, 32)
mask_1421_1526 = core.rife.RIFE(mask_1421_1526, model=24, factor_num=105, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_1421_1526 = core.fmtc.bitdepth(mask_1421_1526, bits=16)
mask_1421_1526 = core.std.Trim(mask_1421_1526, 0, 104)
#
masked_1421_1526 = core.std.MaskedMerge(DD_clip.std.Trim(1421, 1526), main_denoise_deband.std.Trim(1421, 1526), mask_1421_1526, planes=[0,1,2], first_plane=True)

DD_clip = core.std.Trim(DD_clip, 0, 1420) + masked_1421_1526 + core.std.Trim(DD_clip, 1527, src.num_frames-1)

### mask for [1527 1535]
mask_1527_1535 = core.imwri.Read(r'masks\09_Gurren_Lagann_1527.webp') + core.imwri.Read(r'masks\10_Gurren_Lagann_1535.webp')
mask_1527_1535 = ToRGB(mask_1527_1535, 1, 32)
mask_1527_1535 = core.rife.RIFE(mask_1527_1535, model=24, factor_num=8, factor_den=1).std.AssumeFPS(fpsnum=24000, fpsden=1001)
mask_1527_1535 = core.fmtc.bitdepth(mask_1527_1535, bits=16)
mask_1527_1535 = core.std.Trim(mask_1527_1535, 0, 7)
#
masked_1527_1535 = core.std.MaskedMerge(DD_clip.std.Trim(1527, 1535), main_denoise_deband.std.Trim(1527, 1535), mask_1527_1535, planes=[0,1,2], first_plane=True)

DD_clip = core.std.Trim(DD_clip, 0, 1526) + masked_1527_1535 + core.std.Trim(DD_clip, 1536, src.num_frames-1)

final = depth(DD_clip, 10)

set_output(final)