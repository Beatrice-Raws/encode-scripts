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

episode = core.dgdecodenv.DGSource(r'00000.dgi')
episode = core.fmtc.bitdepth(episode, bits=16)
episode = core.std.Crop(episode, top=138, bottom=138)
graydh = fd.fine_dehalo(episode, darkstr=0, brightstr=0.8, showmask=0, thmi=30, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
mrgc = episode.std.Trim(0, 605)+graydh.std.Trim(606, 1210)+episode.std.Trim(1211, 1547)+graydh.std.Trim(1548, 14782)+episode.std.Trim(14783, 15198)+graydh.std.Trim(15199, 190652)+episode.std.Trim(190653, 200716)+graydh.std.Trim(200717, 201299)+episode.std.Trim(201300, 201551)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[189788 190022]")
clip16 = mrgc
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=21, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=16, cb=8, cr=8, grainy=18, grainc=18, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()













