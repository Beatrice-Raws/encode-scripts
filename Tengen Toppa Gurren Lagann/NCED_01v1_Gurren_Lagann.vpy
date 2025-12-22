# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
nced_01v1 = core.bs.VideoSource(r'00007.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
nced_01v1 = depth(nced_01v1,16)

# descale/rescale & AA
AA_clip = DescaleTarget(width=1280, height=720, kernel=Bilinear, do_post_descale=dehalo, downscaler=Hermite(linear=True), credit_mask=False).get_upscaled(nced_01v1)

# denoise, deband & regrain
main_denoise_deband = denoise_deband(AA_clip, thSAD=65, thr=3.5, sigma=1.4)
noise1 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, True, luma_scaling=6).grain(main_denoise_deband)
noise2 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, False, luma_scaling=6).grain(main_denoise_deband)
main_denoise_deband = core.std.Expr([noise1, noise2], 'x {strength} * y 1 {strength} - * +'.format(strength=0.5))

DD_clip = main_denoise_deband

final = depth(DD_clip, 10)

set_output(final)