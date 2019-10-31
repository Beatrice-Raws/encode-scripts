from vapoursynth import *
import vapoursynth as vs
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import insaneAA
import cooldegrain

core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
epis = core.avs.DGSource(r'.\index\EP05.dgi')
aaep = insaneAA.insaneAA(epis, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.32, kernel='bicubic', descale_h=720, outputMode=0)
mrgc = aaep
ed_start = 30761
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\01.png'), "["+str(3+ed_start)+" "+str(71+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\02.png'), "["+str(78+ed_start)+" "+str(149+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\03.png'), "["+str(156+ed_start)+" "+str(227+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\04.png'), "["+str(234+ed_start)+" "+str(305+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\05.png'), "["+str(312+ed_start)+" "+str(383+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\06.png'), "["+str(390+ed_start)+" "+str(461+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\07.png'), "["+str(468+ed_start)+" "+str(539+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\08.png'), "["+str(546+ed_start)+" "+str(617+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\09.png'), "["+str(624+ed_start)+" "+str(695+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\10.png'), "["+str(702+ed_start)+" "+str(773+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\11.png'), "["+str(781+ed_start)+" "+str(852+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\04\12.png'), "["+str(860+ed_start)+" "+str(931+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\03\13.png'), "["+str(1657+ed_start)+" "+str(1728+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\14.png'), "["+str(1735+ed_start)+" "+str(1806+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\15.png'), "["+str(1813+ed_start)+" "+str(1884+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\16.png'), "["+str(1891+ed_start)+" "+str(1962+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\17.png'), "["+str(1969+ed_start)+" "+str(2040+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\18.png'), "["+str(2047+ed_start)+" "+str(2158+ed_start)+"]")
clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=80, thsadc=80, bits=16, blksize=8, overlap=4)
clip = gfa.GradFun3(clip,thr_det=2.8,smode=6,tv_range=True,debug=0)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
