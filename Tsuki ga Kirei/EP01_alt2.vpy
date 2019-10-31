from vapoursynth import *
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import insaneAA
import cooldegrain
core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
epis = core.avs.DGSource(r'.\index\EP01.dgi')
#ncop = core.avs.DGSource(r'.\index\NCOP.dgi').std.Trim(24, 2183)
nced = core.avs.DGSource(r'.\index\NCED.dgi').std.Trim(24, 2179)
#opaa = core.raws.Source(r'.\lossless\NCOP.aa.y4m').std.Trim(24, 2183)
edaa = core.raws.Source(r'.\lossless\NCED.aa.y4m').std.Trim(24, 2179)
#op_t = core.std.Trim(epis,  2590,  4746)
ed_t = core.std.Trim(epis, 32873, 35028)
#op = atf.ApplyCredits(op_t, ncop, opaa)
ed = atf.ApplyCredits(ed_t, nced, edaa)
aaep = epis#insaneAA.insaneAA(epis, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.32, kernel='bicubic', descale_h=720, outputMode=0)
mrgc = aaep.std.Trim(0, 32872) + ed + aaep.std.Trim(35029, 35052)
#mrgc = aaep.std.Trim(0, 2589) + op + aaep.std.Trim(4747, 32872) + ed + aaep.std.Trim(35029, 35052)
#mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\EP04\Title.png'), "[4889 5007]")
#mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\Yokkoku.png'), "[33564 33641]")
#mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\EP04\Next.png'), "[33780 33923]")
#clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=120, thsadc=120, bits=16, blksize=8, overlap=4)
#clip = gfa.GradFun3(clip,thr_det=2.4,smode=6,tv_range=True)
#clip = core.fmtc.bitdepth(clip, bits=10)
#clip.set_output()

mrgc.set_output()
