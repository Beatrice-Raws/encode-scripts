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

core.set_max_cache_size(30000)
core.avs.LoadPlugin(r'C:\Program Files (x86)\AviSynth+\plugins64\DGDecodeNV.dll')

episode = core.avs.DGSource(r'ep10.dgi')


clip16 = core.fmtc.bitdepth(episode, bits=16)
denoised = core.knlm.KNLMeansCL(clip16, h=0.5, s=1, channels="Y")
denoised2 = core.knlm.KNLMeansCL(denoised, h=2, s=2, channels="UV")
#clip_y = mvf.GetPlane(clip16, 0)
#clip_u = mvf.GetPlane(clip16, 1)
#clip_v = mvf.GetPlane(clip16, 2)
#denoised_y = mvf.BM3D(clip_y, sigma=2.0, profile1="fast", matrix=1)
#denoised_u = core.dfttest.DFTTest(clip_u, sigma=2, tbsize=3)
#denoised_v = core.dfttest.DFTTest(clip_v, sigma=2, tbsize=3)
#filtered = core.std.ShufflePlanes([denoised_y,denoised_u,denoised_v], [0,0,0], YUV)
#grain = core.grain.Add(denoised2, var=0.5, uvar=0, seed=46353532353452543, constant=True)
deband = gfa.GradFun3(denoised2, smode=6, thr_det=1, planes=[0])

#clip = core.fmtc.bitdepth(deband, bits=8)

clip = core.fmtc.bitdepth(deband, bits=10)
clip.set_output()


#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()
#core.hist.Luma(clip).set_output()
#clip = core.std.SelectEvery(clip, cycle=int((clip.num_frames/100)*2), offsets=range(50))
#clip = core.std.AssumeFPS(clip, fpsnum=24000, fpsden=1001).set_output()





#clip = cooldegrain.CoolDegrain(mrgc, tr=1, thsad=120, thsadc=120, bits=16, blksize=8, overlap=4)
#clip = atomchtools.JensenLineMask.gfa.GradFun3(clip,thr_det=2.4,smode=6,tv_range=True)