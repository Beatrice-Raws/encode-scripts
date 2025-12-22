# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
src = core.bs.VideoSource(r'00004.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
src = depth(src,16)

ep_ed_start = 32490
ep_ed_end = 34647

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

# descale/rescale & AA
op_ed_AA_clip = op_ed_AA(layer_error_fix)
ep_AA_clip = main_AA(layer_error_fix, credit_mask=False)

AA_clip = core.std.Trim(op_ed_AA_clip, 0, 2157) + core.std.Trim(ep_AA_clip, 2158, ep_ed_start-1) + core.std.Trim(op_ed_AA_clip, ep_ed_start, ep_ed_end) + core.std.Trim(ep_AA_clip, ep_ed_end+1, src.num_frames-1)

weak_eedi_AA = weak_eedi_AA(layer_error_fix)
eedi_AA = eedi_AA(layer_error_fix)
sangnom_AA = sangnom_AA(layer_error_fix)
very_strong_AA = very_strong_AA(layer_error_fix)

AA_clip = fvf.rfs(AA_clip, weak_eedi_AA, mappings="[1086 1109] [1260 1276] [1545 1598] 1749 [3588 3731] [5511 5677] [6834 7230] [7425 7483] [7488 7522] [7529 8143] [8356 8397] [13209 13304] [21825 21855] 26281 [27350 27359] [27873 27878] [27897 27926] [27946 28040]")
AA_clip = fvf.rfs(AA_clip, eedi_AA, mappings="[7231 7234] [7235 7365] [7484 7487] [7523 7528] [12148 12501] [22312 22527] [23755 23885] 24219 25649 26280 26870")
AA_clip = fvf.rfs(AA_clip, sangnom_AA, mappings="[256 371] 20565 25648 26869")
AA_clip = fvf.rfs(AA_clip, very_strong_AA, mappings="24218")

for i in range(3732, 3791):
    mask_path = fr'masks\10_Gurren_Lagann_{i}.webp'
    AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, weak_eedi_AA, mask_path), str(i))

AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, weak_eedi_AA, r'masks\10_Gurren_Lagann_3791-3793.webp'), "3791 3792 3793")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, weak_eedi_AA, r'masks\10_Gurren_Lagann_3794~3885.webp'), "3794 3797 3799 3800 3803 3804 3806 3809 3810 3812 3814 3815 3818 3819 3821 3824 3825 3828 3830 3831 3834 3835 3837 3838 3840 3842 3843 3846 3849 3851 3852 3854 3855 3858 3859 3862 3864 3865 3868 3869 3872 3873 3875 3878 3879 3882 3884 3885")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, weak_eedi_AA, r'masks\10_Gurren_Lagann_3795~3883.webp'), "3795 3796 3798 3801 3802 3805 3807 3808 3811 3813 3816 3817 3820 3822 3823 3826 3827 3829 3832 3833 3836 3839 3841 3844 3845 3847 3848 3850 3853 3856 3857 3860 3861 3863 3866 3867 3870 3871 3874 3876 3877 3880 3881 3883")
AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, very_strong_AA, r'masks\10_Gurren_Lagann_26279.webp'), "26279")

for i in range(27012, 27020):
    mask_path = fr'masks\10_Gurren_Lagann_{i}.webp'
    AA_clip = fvf.rfs(AA_clip, ApplyImageMask(AA_clip, very_strong_AA, mask_path), str(i))


AA_clip = fvf.rfs(AA_clip, main_AA(layer_error_fix, credit_mask=True), mappings="[763 879] [1110 1139] [3021 3206] [3320 3492] [4993 5135] [34916 35019]")

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

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weakest_denoise_deband, mappings="[1423 1435] [1536 1538] 1544 [1628 1674]")
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[54 139] [696 726] [826 879] [1110 1139] [1187 1259] [1319 1391] [1399 1416] [1419 1422] [1539 1583] [1616 1627] [1884 1916] [1939 1992] [2166 2175] [2522 2578] [2704 2749] [2954 3014] [3698 3977] [6062 6118] [13882 13976] [15662 15924] [19182 19241] [19758 19794] [23353 23443] [25064 25325] [25707 25821] [28156 28167] [28170 28188] [30896 31169] [34884 34899] [34916 34931] [34948 34963] [34988 35019]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[0 53] [185 501] [633 695] [763 825] [880 917] [1392 1398] [1417 1418] [1590 1615] [1675 1681] [2184 2307] [2349 2364] [2834 2953] [3314 3492] [5511 5677] [11290 11497] [11838 12005] [13209 13304] [14288 14609] [18298 18345] [22061 22142] [22165 22268] [23056 23091] [24220 24307] [24753 25063] [26339 26439] [27076 27086] [27088 27192] [27230 27244] [27296 27325] [27870 27884] [27948 27965] [28011 28046] [28098 28100] [29204 29439] [30356 30416] [30536 30698] [31241 31413] [31605 31886]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[5678 6061] [27894 27899]")

for i in range(1436, 1537):
    mask_path = fr'masks\01_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weakest_denoise_deband, strong_denoise_deband, mask_path), str(i))

for i in range(2327, 2333):
    mask_path = fr'masks\10_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(weak_denoise_deband, very_strong_denoise_deband, mask_path), str(i))

for i in range(2327, 2333):
    mask_path = fr'masks\10_Gurren_Lagann_{i}.webp'
    DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, very_strong_denoise_deband, mask_path), str(i))

DD_clip = fvf.rfs(DD_clip, ApplyImageMask(DD_clip, strong_denoise_deband, r'masks\10_Gurren_Lagann_13726-13881.webp'), "[13726 13881]")

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