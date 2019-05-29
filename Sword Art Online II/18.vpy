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
    rescaled = clip.resize.Spline36(1440, 810).resize.Spline36(1920, 1080)
    diff = core.std.MakeDiff(clip, rescaled, [0,1,2])
    mask = diff.std.Prewitt([0]).std.Expr('x 40 < 0 x ?').rgvs.RemoveGrain(2).std.Maximum().std.Minimum([0],60).std.Inflate()
    return mask
    
core.max_cache_size = 20000
episode = core.avs.DGSourceIM(r'19.dgi', engine=2)
op_titles = core.std.Trim(episode, 2095, 4244)
ncop = core.avs.DGSourceIM(r'NCOP3.dgi').std.Trim(33, 2182)
ncop_aa = core.raws.Source(r'NCOP3.y4m').std.Trim(33, 2182)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 31770, 33927)
nced = core.avs.DGSourceIM(r'NCED3_1.dgi').std.Trim(24, 2181)
nced_aa = core.raws.Source(r'NCED3_1.y4m').std.Trim(24, 2181)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(mode='cpu'), nnedi3Mode=dict(mode='nnedi3'), descale_str=0.28, kernel='bicubic', descale_h=720)
insaneaa2 = hiaa.HardAA(episode, mask='simplecmb', mthr=30)


mrgc = insaneaa.std.Trim(0, 2094)+op+insaneaa.std.Trim(4245, 31769)+ed+insaneaa.std.Trim(33928, 34047)+episode.std.Trim(34048, 34095)
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[1 120]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\09.png'), "[4348 4442]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10.png'), "[9535 9641]")

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

