from vapoursynth import *
import vapoursynth as vs
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import insaneAA
import cooldegrain
import jensentools
import HardAA
import havsfunc
core.set_max_cache_size(30000)
core.avs.LoadPlugin(r'C:\Program Files (x86)\AviSynth+\plugins64\DGDecodeNV.dll')

episode = core.avs.DGSource(r'[anti-raws]Hataraku Maou-sama! ep.01[BDRemux].dgi')
op_titles = core.std.Trim(episode, 0, 751)
op_titles2 = core.std.Trim(episode, 758, 6168)
ncop = core.avs.DGSource(r'NCOPep1.dgi').std.Trim(0, 751)
ncop2 = core.avs.DGSource(r'NCOPep1.dgi').std.Trim(758, 6168)
ncop_aa = core.raws.Source(r'NCOPep1.y4m').std.Trim(0, 751)
ncop_aa2 = core.raws.Source(r'NCOPep1.y4m').std.Trim(758, 6168)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
op2 = atf.ApplyCredits(op_titles2, ncop2, ncop_aa2)


insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(first=dict(mode='cpu', device=0), second=dict(mode='cpu', device=0)), nnedi3Mode=dict(first=dict(mode='opencl', device=0), second=dict(mode='znedi3', device=0)), descale_str=0.28, kernel='bilinear', descale_h=720, outputMode=0)



mrgc = op + insaneaa.std.Trim(752, 757) + op2 + insaneaa.std.Trim(6169, 31766) + episode.std.Trim(31767, 33921) + insaneaa.std.Trim(33922, 34188)


mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-1.png'), "[752 757]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-2.png'), "[6332 6364]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-3.png'), "[6365 6382]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-4.png'), "[6383 6432]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-5.png'), "[6433 6479]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-6.png'), "[6480 6543]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-7.png'), "[6548 6571]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-8.png'), "[6572 6655]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-9.png'), "[6872 6953]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-10.png'), "[6992 7084]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-11.png'), "[7114 7142]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-12.png'), "[7143 7173]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-13.png'), "[7201 7257]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-14.png'), "[7353 7393]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-15.png'), "[7401 7462]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-16.png'), "[7573 7644]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-17.png'), "[7654 7694]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-18.png'), "[7876 7947]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-19.png'), "[7948 8032]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-20.png'), "[8033 8051]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-21.png'), "[8075 8202]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-22.png'), "[8530 8600]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-23.png'), "[8607 8682]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-24.png'), "[8683 8803]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-25.png'), "[8960 9035]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-26.png'), "[9042 9095]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-27.png'), "[10229 10327]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-28.png'), "[10407 10457]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-29.png'), "[10542 10561]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-30.png'), "[10643 10668]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-31.png'), "[10691 10710]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-32.png'), "[10770 10792]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-33.png'), "[10867 10894]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-34.png'), "[10901 10962]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-35.png'), "[11035 11194]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-36.png'), "[14718 14767]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-37.png'), "[15598 15630]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-38.png'), "[15631 15683]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-39.png'), "[15691 15821]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-40.png'), "[15848 15863]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-41.png'), "[15864 15919]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-42.png'), "[16262 16323]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-43.png'), "[16335 16380]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-44.png'), "[16381 16472]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-45.png'), "[16473 16517]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-46.png'), "[16605 16658]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-47.png'), "[16662 16749]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-48.png'), "[16750 16790]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-49.png'), "[16873 16914]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-50.png'), "[17027 17048]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep1-51.png'), "[17429 17462]")

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\partB.png'), "[19540 19611]")

stab1 = havsfunc.QTGMC(mrgc,InputType=1,SourceMatch=1)
stab2 = havsfunc.QTGMC(stab1,InputType=1,SourceMatch=2)
stab3 = havsfunc.QTGMC(stab2,InputType=1,SourceMatch=3)

mrgc = mrgc.std.Trim(0,130) + stab3.std.Trim(131, 782) + mrgc.std.Trim(783, 34188)


clip = jensentools.filterblock2_hataraku(mrgc)
#clip = core.fmtc.bitdepth(clip, bits=8)

clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()


#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()
#core.hist.Luma(clip).set_output()
#clip = core.std.SelectEvery(clip, cycle=int((clip.num_frames/100)*2), offsets=range(50))
#clip = core.std.AssumeFPS(clip, fpsnum=24000, fpsden=1001).set_output()





#clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=120, thsadc=120, bits=16, blksize=8, overlap=4)
#clip = atomchtools.JensenLineMask.gfa.GradFun3(clip,thr_det=2.4,smode=6,tv_range=True)