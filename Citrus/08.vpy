from vapoursynth import *
import vapoursynth as vs
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import fvsfunc as fvf
import kagefunc as kg
import mvsfunc as mvf
import insaneAA
import cooldegrain
import havsfunc as haf
core.set_max_cache_size(30000)

episode = core.dgdecodenv.DGSource(r'08.dgi')
op_titles = core.std.Trim(episode, 1155, 2408)
op_titles2 = core.std.Trim(episode, 2450, 3308)
ed_titles = core.std.Trim(episode, 31530, 33686)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(3, 1253)
ncop2 = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(1298, 2156)
nced = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(1, 2157)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(3, 1253)
ncop_aa2 = core.raws.Source(r'NCOP.y4m').std.Trim(1298, 2156)
nced_aa = core.raws.Source(r'NCED.y4m').std.Trim(1, 2157)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
op2 = atf.ApplyCredits(op_titles2, ncop2, ncop_aa2)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)

insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(mode='cpu'), nnedi3Mode=dict(mode='opencl', device=0), descale_str=0.28, kernel='bicubic', descale_h=720, outputMode=0)

mrgc = insaneaa.std.Trim(0, 1154)+op+insaneaa.std.Trim(2409, 2449)+op2+insaneaa.std.Trim(3309, 31529)+ed+insaneaa.std.Trim(33687, 34046)+episode.std.Trim(34047, 34070)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\0888.png'), "[2409 2449]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[3322 3462]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\088.png'), "[33945 34046]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
dn = cooldegrain.CoolDegrain(clip16, tr=1, thsad=48, thsadc=48, bits=16, blksize=8, overlap=4)
db = gfa.GradFun3(dn, smode=6, thr_det=2,tv_range=True, planes=[0])
Mask = kg.retinex_edgemask(clip16, sigma=0.6, draft=False)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered, bits=10)

episode3.set_output()


