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
source = core.dgdecodenv.DGSource(r'../index/EP12.dgi')

# AA block
clip_AA = source.main_aa()

hard_AA_list = [[1190,1252], [2374,2417]]
credit_list = [[128,223], [4873,4935], [4947,5009], [5021,5083], [5095,5157], [5188,5250], [5270,5341], [5366,5437], [5462,5524], [5557,5627], [5680,5753]]

clip_AA = at.rfs(clip_AA, clip_AA.hard_aa(), hard_AA_list)

clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_138.png', credit_list[0])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_4896.png', credit_list[1])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_5009.png', credit_list[2])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_5063.png', credit_list[3])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_5110.png', credit_list[4])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_5249.png', credit_list[5])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_5307.png', credit_list[6])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_5437.png', credit_list[7])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_5466.png', credit_list[8])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_5579.png', credit_list[9])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP12_5753.png', credit_list[10])

# dehalo, denoise and deband block
clip_DH = clip_AA.main_dehalo()
clip_DD = clip_DH.denoise_deband()

# outputs block
clip_DD.set_output(0)
# source.set_output(9)
