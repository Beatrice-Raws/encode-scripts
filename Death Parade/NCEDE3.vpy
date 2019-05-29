from vapoursynth import core, GRAY
import kagefunc as kf
import insaneAA as Insane
import cooldegrain as cd

core.max_cache_size = 24000
nc = core.dgdecodenv.DGSource(r'.\..\index\NCEDE3.dgi')
aa = core.raws.Source(r'.\..\lossless\NCEDE3.aa.y4m')
mrgc = Insane.insaneAA(nc, ref=aa, inputMode=2, outputMode=0)

clipsrc = core.fmtc.bitdepth(mrgc, bits=16)
mask = kf.retinex_edgemask(clipsrc.std.ShufflePlanes(0, GRAY), sigma=1).std.Expr('x 2 *')
clip2 = cd.CoolDegrain(clipsrc, bits=16, thsad=48, thsadc=96, blksize=8, overlap=4)
clip2 = core.f3kdb.Deband(clip2, range=8, y=36, cb=28, cr=28, grainy=32, grainc=12, output_depth=16, keep_tv_range=True)
clip = core.std.MaskedMerge(clip2, clipsrc, mask, [0,1,2], first_plane=True)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()