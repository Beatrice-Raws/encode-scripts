from vapoursynth import core, VideoNode, GRAY, YUV
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import GradFun3 as gfa
import insaneAA 
import descale as dsc


core.set_max_cache_size(60000)
episode = core.dgdecodenv.DGSource(r'NCOP1.dgi')
clip = core.std.ShufflePlanes (episode, 0, GRAY)
clip = core.resize.Spline36(clip, 1280, 720)
clip = core.eedi3m.EEDI3CL(clip, field=1, dh=True, gamma=1000.0, vcheck=3, sclip=core.nnedi3cl.NNEDI3CL(clip, field=1, dh=True, nsize=0, nns=4, pscrn=1))
clip = core.std.Transpose(clip)
clip = core.eedi3m.EEDI3CL(clip, field=1, dh=True, gamma=1000.0, vcheck=3, sclip=core.nnedi3cl.NNEDI3CL(clip, field=1, dh=True, nsize=0, nns=4, pscrn=1))
clip = core.std.Transpose(clip)

clip.set_output()



