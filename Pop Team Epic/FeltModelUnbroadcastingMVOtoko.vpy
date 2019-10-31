from vapoursynth import core
import atomchtools as at
import cooldegrain as cd
import gradfun_amod as gf
import insaneAA
import finedehalo as fd
core.max_cache_size = 22000
clip = core.lsmas.LWLibavSource(r'.\..\m2ts\FeltModelUnbroadcastingMVOtoko.m2ts')
clip = cd.CoolDegrain(clip, tr=1, thsad=64, thsadc=32, bits=16, blksize=8, overlap=4)
clip = gf.GradFun3(clip, thr_det=3.5, smode=6, tv_range=True, detect_val=80, grainy=32, grainc=16,debug=0)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
