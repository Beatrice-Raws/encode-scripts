from vapoursynth import *
import gradfun_amod as gfa
import cooldegrain

core.avs.LoadPlugin(r'C:\encoder\dgdecnv\x64 Binaries\DGDecodeNV.dll')
epis = core.avs.DGSource(r'.\..\..\index\EXTRA\ACCAKUNCOURSE04-07.dgi')
mrgc = core.std.Trim(epis, 3316, 5267)
clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=120, thsadc=0, bits=16, blksize=8, overlap=4)
clip = gfa.GradFun3(clip,thr_det=2.5,smode=6,tv_range=True)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
