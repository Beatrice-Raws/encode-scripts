from vapoursynth import *
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import nnedi3_resample as nn3res
import eedi3_resample as ee3res
import cooldegrain

core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
nc = core.avs.DGSource(r'.\index\NCOP.dgi')
aa = core.raws.Source(r'.\lossless\NCOP.aa.y4m')
clip = atf.CopyColors(aa, nc)
clip = cooldegrain.CoolDegrain(clip, tr=1, thsad=80, thsadc=80, bits=16, blksize=8, overlap=4)
clip = gfa.GradFun3(clip,thr_det=2.8,smode=6,tv_range=True,debug=0)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
