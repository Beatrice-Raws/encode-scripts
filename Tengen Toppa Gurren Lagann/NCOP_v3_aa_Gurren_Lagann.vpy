# fix for x265
from sys import path
path.append("./")

# load functions library for title
from ttgl_functions import *

# load source with the required properties
ncop_v3 = core.bs.VideoSource(r'00007.m2ts').std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1)
ncop_v3 = depth(ncop_v3,16)

ncop_AA = op_ed_AA_2(ncop_v3, credit_mask=False)
weak_eedi_AA = weak_eedi_AA(ncop_v3)
eedi_AA = eedi_AA(ncop_v3)
very_strong_AA = very_strong_AA(ncop_v3)
RealESRGAN_AA = RealESRGAN_AA(ncop_v3)

ncop_AA_clip = ncop_AA
ncop_AA_clip = fvf.rfs(ncop_AA_clip, weak_eedi_AA, mappings="[160 179] [1170 1208] [1255 1271] [1394 1417] [1628 1632] [1634 1637] 1639 1641 [1684 1748] [1856 1916]")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, eedi_AA, mappings="[123 133] [256 370] 637")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, RealESRGAN_AA, mappings="1542")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA_clip, eedi_AA, r'masks\17_Gurren_Lagann_191.webp'), "191")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA_clip, very_strong_AA, r'masks\17_Gurren_Lagann_190.webp'), "190")

for i in range(1423, 1542):
    mask_path = fr'masks\17_Gurren_Lagann_{i}.webp'
    ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(weak_eedi_AA, RealESRGAN_AA, mask_path, luma_only=False), str(i))

ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA, strong_AA(ncop_v3), r'masks\17_Gurren_Lagann_1916-1918.webp'), "1916")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA, very_strong_AA, r'masks\17_Gurren_Lagann_1916-1918.webp'), "1917 1918")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA, very_strong_AA, r'masks\17_Gurren_Lagann_1919-1921.webp'), "[1919 1921]")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA, very_strong_AA, r'masks\17_Gurren_Lagann_1922-1924.webp'), "[1922 1924]")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA, very_strong_AA, r'masks\17_Gurren_Lagann_1925-1927.webp'), "[1925 1927]")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA, very_strong_AA, r'masks\17_Gurren_Lagann_1928-1930.webp'), "[1928 1930]")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA, very_strong_AA, r'masks\17_Gurren_Lagann_1931-1933.webp'), "[1931 1933]")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA, very_strong_AA, r'masks\17_Gurren_Lagann_1934-1936.webp'), "[1934 1936]")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA, very_strong_AA, r'masks\17_Gurren_Lagann_1937-1939.webp'), "[1937 1939]")
ncop_AA_clip = fvf.rfs(ncop_AA_clip, ApplyImageMask(ncop_AA, very_strong_AA, r'masks\17_Gurren_Lagann_1940-1942.webp'), "[1940 1942]")

set_output(ncop_AA_clip)