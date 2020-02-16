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
source = core.dgdecodenv.DGSource(r'../index/EP04.dgi')

# AA block
clip_AA = source.main_aa()

hard_AA_list = [[505,788], [855,1092], [1389,1577], [3410,3450], [3612,3616], [4904,5034]]
credit_list = [[36,130], [5059,5142], [5159,5246], [5251,5318], [5323,5390], [5395,5483], [5488,5564], [5569,5640], [5683,5753]]

clip_AA = at.rfs(clip_AA, clip_AA.hard_aa(), hard_AA_list)

clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP04_47.png', credit_list[0])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP04_5100.png', credit_list[1])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP04_5209.png', credit_list[2])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP04_5284.png', credit_list[3])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP04_5369.png', credit_list[4])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP04_5426.png', credit_list[5])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP04_5520.png', credit_list[6])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP04_5599.png', credit_list[7])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP04_5717.png', credit_list[8])

# dehalo, denoise and deband block
clip_DH = clip_AA.main_dehalo()
clip_DD = clip_DH.denoise_deband()

# outputs block
clip_DD.set_output(0)
# source.set_output(9)
