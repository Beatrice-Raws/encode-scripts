# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
AA_clip = core.raws.Source(r'NCOP_v3_aa.y4m').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)

# denoise, deband & regrain

weak_denoise_deband = denoise_deband(AA_clip, thSAD=65, thr=2.0, sigma=1.0)

main_denoise_deband = denoise_deband(AA_clip, thSAD=65, thr=3.5, sigma=1.4)
noise1 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, True, luma_scaling=6).grain(main_denoise_deband)
noise2 = AddNoise.GAUSS((0.4, 0), 0.85, Catrom, False, luma_scaling=6).grain(main_denoise_deband)
main_denoise_deband = core.std.Expr([noise1, noise2], 'x {strength} * y 1 {strength} - * +'.format(strength=0.5))

strong_denoise_deband = denoise_deband(AA_clip, thSAD=65, thr=5.0, sigma=1.6)
strong_denoise_deband = AddNoise.GAUSS((1.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(strong_denoise_deband)

very_strong_denoise_deband = denoise_deband_strong(AA_clip, thSAD=120, thr=8.0, sigma=2.0)

DD_clip = main_denoise_deband
DD_clip = fvf.rfs(DD_clip, weak_denoise_deband, mappings="[13 30]")
DD_clip = fvf.rfs(DD_clip, strong_denoise_deband, mappings="[141 150] [849 877] [1023 1151] [1326 1326]")
DD_clip = fvf.rfs(DD_clip, very_strong_denoise_deband, mappings="[133 133] [151 159] [371 502] [1418 1423] [1540 1542] [1749 1914]")
DD_clip = fvf.rfs(DD_clip, core.neo_f3kdb.Deband(DD_clip), mappings="[1749 1914]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((2.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1418 1542]")
DD_clip = fvf.rfs(DD_clip, AddNoise.GAUSS((5.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(DD_clip), mappings="[1749 1942]")

final = depth(DD_clip, 10)

set_output(final)