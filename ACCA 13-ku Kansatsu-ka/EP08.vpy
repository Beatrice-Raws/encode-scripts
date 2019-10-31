from vapoursynth import *
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import insaneAA
import cooldegrain

core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
ed_start = 32250
next_start = 34407
epis = core.avs.DGSource(r'.\..\index\EP08.dgi')
nced = core.avs.DGSource(r'.\..\index\NCED.dgi').std.Trim(24, 2180)
edaa = core.raws.Source(r'.\..\lossless\NCED.aa.y4m').std.Trim(24, 2180)
ed_t = core.std.Trim(epis, ed_start, int(next_start-1))
ed = atf.ApplyCredits(ed_t, nced, edaa)
aaep = insaneAA.insaneAA(epis, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.33, kernel='bicubic', descale_h=720)
mrgc = aaep.std.Trim(0, int(ed_start-1)) + ed + aaep.std.Trim(next_start, int(epis.num_frames-1))
clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=120, thsadc=0, bits=16, blksize=8, overlap=4)
clip = gfa.GradFun3(clip,thr_det=2.5,smode=6,tv_range=True)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
