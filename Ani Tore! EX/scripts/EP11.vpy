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
source = core.dgdecodenv.DGSource(r'../index/EP11.dgi')

# AA block
clip_AA = source.main_aa()

hard_AA_list = [[128,218], [291,410]]
credit_list = [[132,213], [4783,4842], [4871,4930], [4956,5015], [5044,5103], [5140,5199], [5311,5370], [5403,5462], [5484,5543], [5554,5613]]

clip_AA = at.rfs(clip_AA, clip_AA.hard_aa(), hard_AA_list)

clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP11_163.png', credit_list[0])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP11_4810.png', credit_list[1])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP11_4908.png', credit_list[2])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP11_4991.png', credit_list[3])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP11_5079.png', credit_list[4])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP11_5150.png', credit_list[5])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP11_5327.png', credit_list[6])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP11_5432.png', credit_list[7])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP11_5514.png', credit_list[8])
clip_AA = clip_AA.replace_by_mask(source, r'../masks/credits/EP11_5575.png', credit_list[9])

# dehalo, denoise and deband block
clip_DH = clip_AA.main_dehalo()
clip_DD = clip_DH.denoise_deband()

# outputs block
clip_DD.set_output(0)
# source.set_output(9)
