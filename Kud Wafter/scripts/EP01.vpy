# fix for vspipe
from sys import path
path.append("./")

# load functions library for title
from titleFunc import *

# enable augmentation by Endill
core.augment(locals())

# set cache size
core.set_max_cache_size(30000)

# load source
source = core.dgdecodenv.DGSource(r'../index/jp_ver.dgi')

# AA block
clip_AA = source.main_aa()
clip_hard_AA = clip_AA.hard_aa()
clip_multi_hard_AA = clip_hard_AA \
    .hard_aa() \
    .hard_aa() \
    .hard_aa()

true_hd_list = [(0,170), (1612,1803), (65328,73247)]
hard_AA_list = [
    (2047,2088), (16920,17230), (19766,19812), (48462,48820), (49239,49267), (49291,49355),
    (52818,52854), (53345,53399), (53466,53500), (53668,53690), (54078,54097), (54982,55106), (60489,60547)
]
multi_hard_AA_list = {'EP01_19766': (19766,19783), 'EP01_19793': (19793,19795)}

clip_AA = at.rfs(clip_AA, clip_hard_AA, hard_AA_list)

for key, frames_couple in multi_hard_AA_list.items():
    clip_AA = clip_AA.replace_by_mask(clip_multi_hard_AA, f'../masks/{key}.png', frames_couple)

# dehalo, denoise and deband block
clip_DH = clip_AA.main_dehalo()
clip_DD = clip_DH.denoise_deband()

clip_DD = at.rfs(clip_DD, source.fmtc.bitdepth(bits=16), true_hd_list)

# outputs block
clip_DD.set_output(0)
# source.set_output(9)
