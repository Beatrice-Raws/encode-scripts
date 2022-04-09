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

def Tawawa_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='lanczos', descale_height=720)
    graydh = fd.fine_dehalo(desc, darkstr=0.4, brightstr=0.8, showmask=0, thmi=10, thma=80, thlimi=10, thlima=80, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, depth=[6, 4, 4], thresh=64, cplace="mpeg2")
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=0.7, showmask=0, thmi=10, thma=80, thlimi=10, thlima=80, rx=2.4, ry=2.4, useMtEdge=True)
    return mixyuv

core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'14.dgi')
ed_titles = core.std.Trim(episode, 7068, 8579)
nced = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(12, 1523)
nced_aa = core.raws.Source(r'NCED.y4m').std.Trim(12, 1523)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Tawawa_aa(episode)

mrgc = insaneaa.std.Trim(0, 7067)+ed+episode.std.Trim(8580, 8603)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\13.png'), "[828 971]")

#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=18, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.placebo.Deband(den, planes = 1, threshold = 0.8, grain = 6, radius = 10)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()







