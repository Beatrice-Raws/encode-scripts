import sys
from pathlib import Path
sys.path.append(str(Path(".").resolve()))
from nekofunc import core, MainAA, DenoiseDebandFades, DenoiseDebandMain, DealWithFades, at

core.max_cache_size = 18000

fades_string = "[0:35][234:239][282:287][1104:1151][1639:1644][1916:1934][2651:2710][3154:3159][3318:3365][4689:4694][6228:6263]" + \
    "[7182:7205][7899:7916][9477:9524][9528:9546][9933:9945][10568:10573][14226:14237][18328:18351][19033:19062][19896:19919][21018:21065]" + \
    "[23723:23777][27383:27412][28925:28948][30659:30670][30719:30730][31765:31800][32713:32724][33511:33540][33571:33582][35349:35402][37323:37370]"
source = core.dgdecodenv.DGSource(r'.\..\index\MAIN.dgi')
fades_fixer = DealWithFades(source)
source = core.rfmod.Replace(source, fades_fixer, fades_string)
aaclip = MainAA(source)
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\EP01NAME.png', preview=False), [[3372, 3431]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\EP02NAME.png', preview=False), [[10586, 10645]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\EP03NAME.png', preview=False), [[19075, 19134]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\EP04NAME.png', preview=False), [[27425, 27484]])
aaclip = at.rfs(aaclip, source, [[35253, 35348], [37263, 37382]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\OP\01.png', preview=False), [[1648, 1701]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\OP\02.png', preview=False), [[1708, 1786]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\OP\03.png', preview=False), [[1793, 1856]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\OP\04.png', preview=False), [[1943, 2057]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\OP\05.png', preview=False), [[2076, 2159]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\OP\06.png', preview=False), [[2865, 2954]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\OP\07.png', preview=False), [[3228, 3311]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\01.png', preview=False), [[37800, 37962]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\02.png', preview=False), [[37966, 38129]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\03.png', preview=False), [[38133, 38301]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\04.png', preview=False), [[38305, 38478]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\05.png', preview=False), [[38482, 38640]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\06.png', preview=False), [[38644, 38803]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\07.png', preview=False), [[38807, 38953]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\08.png', preview=False), [[38957, 39121]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\09.png', preview=False), [[39211, 39355]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\10.png', preview=False), [[39359, 39428]])
aaclip = at.rfs(aaclip, at.ApplyImageMask(aaclip, source, r'.\masks\MAIN\ED\11.png', preview=False), [[39432, 39542]])
clip = DenoiseDebandMain(aaclip)
clip_fades = DenoiseDebandFades(aaclip)
clip = core.rfmod.Replace(clip, clip_fades, fades_string)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()

