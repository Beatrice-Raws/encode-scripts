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

episode = core.avs.DGSource(r'NCOPep1.dgi')


insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(first=dict(mode='cpu', device=0), second=dict(mode='cpu', device=0)), nnedi3Mode=dict(first=dict(mode='opencl', device=0), second=dict(mode='znedi3', device=0)), descale_str=0.28, kernel='bilinear', descale_h=720, outputMode=0)


#mrgc = insaneaa.std.Trim(0, 130) + stab3.std.Trim(131, 782) + insaneaa.std.Trim(783, 1244) + stab3.std.Trim(1245, 1588) + insaneaa.std.Trim(1589, 6273)

#clip = jensentools.filterblock2_hataraku(episode)
#clip = core.fmtc.bitdepth(clip, bits=8)

#clip = core.fmtc.bitdepth(clip, bits=10)
insaneaa.set_output()


#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()
#core.hist.Luma(clip).set_output()
#clip = core.std.SelectEvery(clip, cycle=int((clip.num_frames/100)*2), offsets=range(50))
#clip = core.std.AssumeFPS(clip, fpsnum=24000, fpsden=1001).set_output()





#clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=120, thsadc=120, bits=16, blksize=8, overlap=4)
#clip = atomchtools.JensenLineMask.gfa.GradFun3(clip,thr_det=2.4,smode=6,tv_range=True)