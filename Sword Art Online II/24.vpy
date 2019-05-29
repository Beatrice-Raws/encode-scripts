from vapoursynth import core, VideoNode, GRAY
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import gradfun_amod as gfa
import insaneAA 
import cooldegrain
import HardAAp2 as hiaa
core.avs.LoadPlugin(r'C:\encoder\dgdecim\x64\DGDecodeIM.dll')  
def titles_mask(clip):
    rescaled = clip.resize.Spline36(1280, 720).resize.Spline36(1920, 1080)
    diff = core.std.MakeDiff(clip, rescaled, [0,1,2])
    mask = diff.std.Prewitt([0]).std.Expr('x 40 < 0 x ?').rgvs.RemoveGrain(2).std.Maximum().std.Minimum([0],60).std.Inflate()
    return mask
    
core.max_cache_size = 20000
episode = core.avs.DGSourceIM(r'25.dgi', engine=2)
ed_titles = core.std.Trim(episode, 28428, 30901)
nced = core.avs.DGSourceIM(r'NCED3_2.dgi').std.Trim(24, 2497)
nced_aa = core.raws.Source(r'NCED3_2.y4m').std.Trim(24, 2497)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(mode='cpu'), nnedi3Mode=dict(mode='nnedi3'), descale_str=0.28, kernel='bicubic', descale_h=720)
insaneaa2 = hiaa.HardAA(episode, mask='simplecmb', mthr=30)


mrgc = insaneaa.std.Trim(0, 28427)+ed+insaneaa.std.Trim(30902, 33948)+episode.std.Trim(33949, 34095)

mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, titles_mask(episode), planes=[0], first_plane=True), "[11 710]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, titles_mask(episode), planes=[0], first_plane=True), "[839 918]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, titles_mask(episode), planes=[0], first_plane=True), "[1238 1424]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, titles_mask(episode), planes=[0], first_plane=True), "[1686 1782]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, titles_mask(episode), planes=[0], first_plane=True), "[3052 3540]")

mrgc = fvf.rfs(mrgc, havsfunc.QTGMC(mrgc, InputType=1,SourceMatch=3), "[21646 21890]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
clip_y = mvf.GetPlane(clip16, 0)
pf = core.dfttest.DFTTest(clip_y, sigma=4, tbsize=3, opt=1)
den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=32, thsadc=32, bits=16, blksize=8, overlap=4, pf=pf)
filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(filtered, smode=6, thr_det=2, grainy=34, grainc=24,tv_range=True, planes=[0])
Mask = kg.retinex_edgemask(clip16, sigma=0.1, draft=False)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.40))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode3.set_output()

