from vapoursynth import *
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import insaneAA
import cooldegrain

core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
epis = core.avs.DGSource(r'.\index\EP09.dgi')
mrgc = insaneAA.insaneAA(epis, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.32, kernel='bicubic', descale_h=720, outputMode=0)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\09\01.png'), "[32 119]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\09\02.png'), "[189 270]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\09\03.png'), "[274 358]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\09\04.png'), "[362 446]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\09\05.png'), "[450 534]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\09\06.png'), "[634 693]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\09\07.png'), "[694 761]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\09\08.png'), "[765 815]")
ed_start = 31768
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\01.png'), "["+str(3+ed_start)+" "+str(71+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\02.png'), "["+str(78+ed_start)+" "+str(149+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\03.png'), "["+str(156+ed_start)+" "+str(227+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\04.png'), "["+str(234+ed_start)+" "+str(305+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\05.png'), "["+str(312+ed_start)+" "+str(383+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\06.png'), "["+str(390+ed_start)+" "+str(461+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\07.png'), "["+str(468+ed_start)+" "+str(539+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\08.png'), "["+str(546+ed_start)+" "+str(617+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\09.png'), "["+str(624+ed_start)+" "+str(695+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\08\10.png'), "["+str(702+ed_start)+" "+str(773+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\11.png'), "["+str(781+ed_start)+" "+str(852+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\12.png'), "["+str(860+ed_start)+" "+str(931+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\03\13.png'), "["+str(1657+ed_start)+" "+str(1728+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\14.png'), "["+str(1735+ed_start)+" "+str(1806+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\15.png'), "["+str(1813+ed_start)+" "+str(1884+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\16.png'), "["+str(1891+ed_start)+" "+str(1962+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\09\17.png'), "["+str(1969+ed_start)+" "+str(2040+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\18.png'), "["+str(2047+ed_start)+" "+str(2158+ed_start)+"]")
clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=80, thsadc=80, bits=16, blksize=8, overlap=4)
clip = gfa.GradFun3(clip,thr_det=2.8,smode=6,tv_range=True,debug=0)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
