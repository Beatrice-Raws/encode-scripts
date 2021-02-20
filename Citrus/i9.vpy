from vapoursynth import *
import vapoursynth as vs
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import fvsfunc as fvf
import kagefunc as kg
import mvsfunc as mvf
import insaneAA
import cooldegrain
import havsfunc as haf
core.set_max_cache_size(30000)

episode = core.dgdecodenv.DGSource(r'00021.dgi')
deint = haf.QTGMC(episode,Preset="Slower", Sharpness=1.0, FPSDivisor=2,InputType=0,TFF=True)
clip16 = core.fmtc.bitdepth(deint, bits=16)
dn = cooldegrain.CoolDegrain(clip16, tr=1, thsad=48, thsadc=48, bits=16, blksize=8, overlap=4)
db = gfa.GradFun3(dn, smode=6, thr_det=2,tv_range=True, planes=[0])
Mask = kg.retinex_edgemask(clip16, sigma=0.6, draft=False)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered, bits=10)

episode3.set_output()


