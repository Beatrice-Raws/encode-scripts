# fix for vspipe
from sys import path
path.append("./")

# load functions library for title
from titleFunc import *

# enable augmentation by Endill
core.augment(locals())

# set cache size
core.set_max_cache_size(25000)

# load source
source = core.dgdecodenv.DGSource(r'../index/SP07.dgi')

# AA block
clip_AA = source.main_aa()

# dehalo, denoise and deband block
clip_DH = clip_AA.main_dehalo()
clip_DD = clip_DH.denoise_deband()

# outputs block
clip_DD.set_output(0)
# source.set_output(9)
