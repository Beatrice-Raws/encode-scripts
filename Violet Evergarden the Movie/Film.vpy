from vapoursynth import core, VideoNode, GRAY, YUV
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import GradFun3 as gfa
import insaneAA 
import cooldegrain
import finedehalo as fd
import HardAAp2 as hiaa
import descale as dsc
core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'00000.dgi')
episode = core.fmtc.bitdepth(episode, bits=16)
episode1 = core.std.Crop(episode, top=274, bottom=274)
graydh1 = core.warp.AWarpSharp2(episode1, type=1, depth=[5, 2, 2], thresh=64, cplace="mpeg2")
graydh2 = fd.fine_dehalo(graydh1, darkstr=0, brightstr=0.7, showmask=0, thmi=22, thma=100, rx=2.4, ry=2.4, useMtEdge=True)
graydh3 = core.std.AddBorders(graydh2, top=274, bottom=274)
mrgc = episode.std.Trim(0, 605)+graydh3.std.Trim(606, 1210)+episode.std.Trim(1211, 1547)+graydh3.std.Trim(1548, 14782)+episode.std.Trim(14783, 15198)+graydh3.std.Trim(15199, 190652)+episode.std.Trim(190653, 200716)+graydh3.std.Trim(200717, 201299)+episode.std.Trim(201300, 201527)
clip16 = mrgc
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=8, thsadc=4, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=12, y=12, cb=8, cr=8, grainy=14, grainc=14, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
mrgc1 = core.std.Crop(filtered2, top=274, bottom=274)
episode3 = core.fmtc.bitdepth(mrgc1, bits=10)
episode3.set_output()










