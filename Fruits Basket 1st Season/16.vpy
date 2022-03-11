from vapoursynth import core, VideoNode, GRAY8, YUV, GRAY
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
import psutil
import regress
p_handle = psutil.Process()
p_handle.cpu_affinity([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46])
core.num_threads = 24

def FruitsBasket_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='lanczos', descale_height=720) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=0.65, showmask=0, thmi=44, thma=100, rx=2.3, ry=2.3)
    return mixyuv

core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'16.dgi')
op_titles = core.std.Trim(episode, 1368, 3524)
ncop = core.dgdecodenv.DGSource(r'NCOP2.dgi').std.Trim(0, 2156)
ncop_aa = core.raws.Source(r'NCOP2.y4m').std.Trim(0, 2156)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 29755, 31911)
nced = core.dgdecodenv.DGSource(r'NCED2.dgi').std.Trim(0, 2156)
nced_aa = core.raws.Source(r'NCED2.y4m').std.Trim(0, 2156)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = FruitsBasket_aa(episode)

mrgc = insaneaa.std.Trim(0, 1367)+op+insaneaa.std.Trim(3525, 29754)+ed+insaneaa.std.Trim(31912, 34285)+episode.std.Trim(34286, 34335)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\40.png'), "[34166 34285]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=16, thsadc=10, bits=16, blksize=8, overlap=4, pf=pf)
db = core.placebo.Deband(den, planes = 1, threshold = 0.9, grain = 6, radius = 10)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()










