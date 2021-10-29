from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import GradFun3 as gfa
import insaneAA 
import finesharp
import cooldegrain
import finedehalo as fd
import HardAAp2 as hiaa
import descale as dsc
import psutil
import regress
p_handle = psutil.Process()
p_handle.cpu_affinity([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46])
core.num_threads = 24
  

core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'12.dgi')
graydh = fd.fine_dehalo(episode, darkstr=0, brightstr=0.7, showmask=0, thmi=40, thma=100, rx=2.4, ry=2.4, useMtEdge=True)
aa = hiaa.HardAA(episode, mask='simple', mthr=30, useCL=True)
aa = fd.fine_dehalo(aa, darkstr=0, brightstr=0.7, showmask=0, thmi=40, thma=100, rx=2.4, ry=2.4, useMtEdge=True)
mrgc = graydh.std.Trim(0, 14313)+episode.std.Trim(14314, 14529)+graydh.std.Trim(14530, 18153)+aa.std.Trim(18154, 18363)+graydh.std.Trim(18364, 33326)+episode.std.Trim(33327, 33539)+graydh.std.Trim(33540, 33935)+episode.std.Trim(33936, 34166)+graydh.std.Trim(34167, 34319)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, graydh, r'.\mask\02.png'), "[18154 18363]")
clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=2, tbsize=3, opt=3, planes=[0,1,2])
pf2 = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=32, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
den2 = cooldegrain.CoolDegrain(clip16, tr=1, thsad=22, thsadc=10, bits=16, blksize=8, overlap=4, pf=pf2)
db = core.f3kdb.Deband(den, range=31, y=30, cb=10, cr=10, grainy=20, grainc=20, output_depth=16, keep_tv_range=True)
db2 = core.f3kdb.Deband(den2, range=31, y=36, cb=10, cr=10, grainy=21, grainc=21, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
filtered3 = core.std.MaskedMerge(db2, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
mrgc2 = episode3.std.Trim(0, 33935)+episode4.std.Trim(33936, 34319)
mrgc2.set_output()






