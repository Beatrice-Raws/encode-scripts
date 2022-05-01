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

def Vivy_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='lanczos', descale_height=864, lanczos_taps = 1)
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=10, thma=60, thlimi=10, thlima=60, rx=2.3, ry=2.3, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'12.dgi')
op_titles = core.std.Trim(episode, 624, 2781)
ncop = core.dgdecodenv.DGSource(r'NCOP6.dgi').std.Trim(0, 2157)
ncop_aa = core.raws.Source(r'NCOP6.y4m').std.Trim(0, 2157)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 31530, 33687)
nced = core.dgdecodenv.DGSource(r'NCED3.dgi').std.Trim(24, 2181)
nced_aa = core.raws.Source(r'NCED3.y4m').std.Trim(24, 2181)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Vivy_aa(episode)
stab0 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=1)
stab2 = havsfunc.QTGMC(stab, InputType=1, SourceMatch=2)
stab3 = havsfunc.QTGMC(stab2, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 623)+op+insaneaa.std.Trim(2782, 9177)+stab3.std.Trim(9178, 9354)+insaneaa.std.Trim(9355, 9666)+stab3.std.Trim(9667, 9882)+insaneaa.std.Trim(9883, 12521)+stab3.std.Trim(12522, 12617)+insaneaa.std.Trim(12618, 13788)+stab3.std.Trim(13789, 13884)+insaneaa.std.Trim(13885, 14514)+stab3.std.Trim(14515, 14579)+insaneaa.std.Trim(14580, 20825)+stab3.std.Trim(20826, 20909)+insaneaa.std.Trim(20910, 25673)+stab3.std.Trim(25674, 25871)+insaneaa.std.Trim(25872, 27573)+stab3.std.Trim(27574, 27687)+insaneaa.std.Trim(27688, 29165)+stab3.std.Trim(29166, 29222)+insaneaa.std.Trim(29223, 31529)+ed+insaneaa.std.Trim(33688, 34047)+episode.std.Trim(34048, 34071)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\105.png'), "[4203 4322]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\106.png'), "[33952 34047]")

#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()
#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=14, thsadc=10, bits=16, blksize=8, overlap=4, pf=pf)
db = core.placebo.Deband(den, planes = 1, threshold = 0.8, grain = 6.2, radius = 10)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()







