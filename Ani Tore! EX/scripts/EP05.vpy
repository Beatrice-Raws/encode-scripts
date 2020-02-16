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
source = core.dgdecodenv.DGSource(r'../index/EP05.dgi')

# AA block
clip_AA = source.main_aa()

hard_AA_list = [[1790,1978], [1979,2049], [3914,4056], [4315,4485]]
credit_list = [[316,411], [5045,5104], [5116,5175], [5187,5246], [5258,5317], [5329,5388], [5410,5469], [5492,5551], [5568,5635], [5683,5753]]

clip_AA = at.rfs(clip_AA, clip_AA.hard_aa(), hard_AA_list)

clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP05_370.png', credit_list[0])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP05_5075.png', credit_list[1])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP05_5150.png', credit_list[2])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP05_5220.png', credit_list[3])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP05_5285.png', credit_list[4])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP05_5360.png', credit_list[5])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP05_5440.png', credit_list[6])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP05_5510.png', credit_list[7])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP05_5595.png', credit_list[8])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP05_5700.png', credit_list[9])

# dehalo, denoise and deband block
clip_DH = clip_AA.main_dehalo()
clip_DD = clip_DH.denoise_deband()

# outputs block
clip_DD.set_output(0)
# source.set_output(9)
