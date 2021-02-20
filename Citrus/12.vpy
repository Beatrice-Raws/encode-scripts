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

episode = core.dgdecodenv.DGSource(r'12.dgi')
op_titles = core.std.Trim(episode, 411, 1664)
op_titles2 = core.std.Trim(episode, 1706, 2565)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(3, 1256)
ncop2 = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(1298, 2157)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(3, 1253)
ncop_aa2 = core.raws.Source(r'NCOP.y4m').std.Trim(1298, 2157)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
op2 = atf.ApplyCredits(op_titles2, ncop2, ncop_aa2)

insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(mode='cpu'), nnedi3Mode=dict(mode='opencl', device=0), descale_str=0.28, kernel='bicubic', descale_h=720, outputMode=0)

mrgc = insaneaa.std.Trim(0, 410)+op+insaneaa.std.Trim(1665, 1705)+op2+insaneaa.std.Trim(2566, 33685)+episode.std.Trim(33686, 33709)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\12.png'), "[1665 1705]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\120.png'), "[2580 2704]")

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\121.png'), "[30507 30588]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\122.png'), "[30605 30684]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\123.png'), "[30700 30780]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\124.png'), "[31033 31116]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\125.png'), "[31201 31272]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\126.png'), "[31273 31344]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\127.png'), "[31345 31427]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\128.png'), "[31453 31524]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\129.png'), "[31525 31607]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\130.png'), "[31657 31751]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\131.png'), "[32119 32193]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\132.png'), "[32207 32280]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\133.png'), "[32341 32423]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\134.png'), "[32559 32665]")

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


