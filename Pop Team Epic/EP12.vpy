from vapoursynth import core
import atomchtools as at
import cooldegrain as cd
import gradfun_amod as gf
import insaneAA
import HardAAp2
import finedehalo as fd
core.max_cache_size = 22000
clip = core.lsmas.LWLibavSource(r'.\..\m2ts\Vol3.m2ts')
clip = core.std.Trim(clip, 102306, 136389)
clip1 = insaneAA.insaneAA(clip, fasterAA=False, eedi3Mode=dict(mode='cpu'), nnedi3Mode=dict(mode='nnedi3'), descale_str=0.32, kernel='bilinear', descale_h=810)
clip = core.std.Expr([clip1, clip], ['x 0.6 * y 0.4 * +', 'x', 'x'])
clip = HardAAp2.HardAA(clip1,mthr=95)
clip = fd.fine_dehalo(clip, darkstr=0, brightstr=0.75, useMtEdge=True)
clip = cd.CoolDegrain(clip, tr=1, thsad=64, thsadc=32, bits=16, blksize=8, overlap=4)
clip = gf.GradFun3(clip, thr_det=3.5, smode=6, tv_range=True, detect_val=80, grainy=32, grainc=16,debug=0)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()
