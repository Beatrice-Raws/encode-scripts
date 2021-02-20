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
import psutil
p_handle = psutil.Process()
p_handle.cpu_affinity([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46])
core.num_threads = 24
def Mahouka_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bilinear', descale_height=720) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6) 
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv  

core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'10.dgi')
op_titles = core.std.Trim(episode, 1678, 3835)
ncop = core.dgdecodenv.DGSource(r'NCOP1.dgi').std.Trim(24, 2181)
ncop_aa = core.raws.Source(r'NCOP1.y4m').std.Trim(24, 2181)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 32331, 33949)
nced = core.dgdecodenv.DGSource(r'NCED2.dgi').std.Trim(566, 2184)
nced_aa = core.raws.Source(r'NCED2.y4m').std.Trim(566, 2184)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Mahouka_aa(episode)
st = havsfunc.QTGMC(episode, InputType=1, SourceMatch=3)
sta = Mahouka_aa(st)
stab = havsfunc.QTGMC(sta, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 1677)+op+insaneaa.std.Trim(3836, 32031)+episode.std.Trim(32032, 32330)+ed+stab.std.Trim(33950, 34093)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\ep2.png'), "[33950 34069]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=20, thsadc=28, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=20, cb=11, cr=11, grainy=20, grainc=20, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()

























