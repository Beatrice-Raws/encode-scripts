from vapoursynth import *
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import insaneAA
import cooldegrain

core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
epis = core.avs.DGSource(r'.\index\EXSP.dgi')
mrgc = insaneAA.insaneAA(epis, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.32, kernel='bicubic', descale_h=720, outputMode=0)
mrgc = fvf.rfs(mrgc, epis, "[22200 22439]")
clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=80, thsadc=80, bits=16, blksize=8, overlap=4)
clip = gfa.GradFun3(clip,thr_det=2.8,smode=6,tv_range=True,debug=0)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
