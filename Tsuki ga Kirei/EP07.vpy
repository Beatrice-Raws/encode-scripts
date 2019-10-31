from vapoursynth import *
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import insaneAA
import cooldegrain

core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
epis = core.avs.DGSource(r'.\index\EP07.dgi')
mrgc = insaneAA.insaneAA(epis, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.32, kernel='bicubic', descale_h=720, outputMode=0)
op_start = 3525
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\01.png'), "["+str(4+op_start)+" "+str(83+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\02.png'), "["+str(84+op_start)+" "+str(164+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\03.png'), "["+str(613+op_start)+" "+str(686+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\04.png'), "["+str(687+op_start)+" "+str(775+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\05.png'), "["+str(776+op_start)+" "+str(874+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\06.png'), "["+str(875+op_start)+" "+str(938+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\07.png'), "["+str(939+op_start)+" "+str(1024+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\08.png'), "["+str(1025+op_start)+" "+str(1145+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\09.png'), "["+str(1279+op_start)+" "+str(1429+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\10.png'), "["+str(1598+op_start)+" "+str(1699+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\11.png'), "["+str(1700+op_start)+" "+str(1761+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\12.png'), "["+str(1762+op_start)+" "+str(1838+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\13.png'), "["+str(1839+op_start)+" "+str(1957+op_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\07\14.png'), "["+str(2020+op_start)+" "+str(2117+op_start)+"]")
ed_start = 27715
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\01.png'), "["+str(3+ed_start)+" "+str(71+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\02.png'), "["+str(78+ed_start)+" "+str(149+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\03.png'), "["+str(156+ed_start)+" "+str(227+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\04.png'), "["+str(234+ed_start)+" "+str(305+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\05.png'), "["+str(312+ed_start)+" "+str(383+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\06.png'), "["+str(390+ed_start)+" "+str(461+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\07.png'), "["+str(468+ed_start)+" "+str(539+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\08.png'), "["+str(546+ed_start)+" "+str(617+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\09.png'), "["+str(624+ed_start)+" "+str(695+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\05\10.png'), "["+str(702+ed_start)+" "+str(773+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\11.png'), "["+str(781+ed_start)+" "+str(852+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\06\12.png'), "["+str(860+ed_start)+" "+str(931+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\03\13.png'), "["+str(1657+ed_start)+" "+str(1728+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\14.png'), "["+str(1735+ed_start)+" "+str(1806+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\15.png'), "["+str(1813+ed_start)+" "+str(1884+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\16.png'), "["+str(1891+ed_start)+" "+str(1962+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\07\17.png'), "["+str(1969+ed_start)+" "+str(2040+ed_start)+"]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\01\18.png'), "["+str(2047+ed_start)+" "+str(2158+ed_start)+"]")
clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=80, thsadc=80, bits=16, blksize=8, overlap=4)
clip = gfa.GradFun3(clip,thr_det=2.8,smode=6,tv_range=True,debug=0)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
