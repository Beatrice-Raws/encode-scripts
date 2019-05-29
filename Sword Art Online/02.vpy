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
episode = core.avs.DGSourceIM(r'02.dgi', engine=2)
op_titles = core.std.Trim(episode, 960, 3070)
ncop = core.avs.DGSourceIM(r'NCOP1.dgi').std.Trim(24, 2134)
ncop_aa = core.raws.Source(r'NCOP1.y4m').std.Trim(24, 2134)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 31768, 33925)
nced = core.avs.DGSourceIM(r'NCED1.dgi').std.Trim(24, 2181)
nced_aa = core.raws.Source(r'NCED1.y4m').std.Trim(24, 2181)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(mode='cpu'), nnedi3Mode=dict(mode='nnedi3'), descale_str=0.28, kernel='bicubic', descale_h=720)
insaneaa2 = hiaa.HardAA(episode, mask='simplecmb', mthr=30)


mrgc = insaneaa2.std.Trim(0, 237)+insaneaa.std.Trim(238, 959)+op+insaneaa.std.Trim(3071, 16055)+insaneaa2.std.Trim(16056, 16160)+insaneaa.std.Trim(16161, 16667)+insaneaa2.std.Trim(16668, 16738)+insaneaa.std.Trim(16739, 17273)+insaneaa2.std.Trim(17274, 17417)+insaneaa.std.Trim(17418, 17553)+insaneaa2.std.Trim(17554, 17594)+insaneaa.std.Trim(17595, 17994)+insaneaa2.std.Trim(17995, 18041)+insaneaa.std.Trim(18042, 18655)+insaneaa2.std.Trim(18656, 18779)+insaneaa.std.Trim(18780, 19042)+insaneaa2.std.Trim(19043, 19085)+insaneaa.std.Trim(19086, 22747)+insaneaa2.std.Trim(22748, 22850)+insaneaa.std.Trim(22851, 23139)+insaneaa2.std.Trim(23140, 23180)+insaneaa.std.Trim(23181, 23468)+insaneaa2.std.Trim(23469, 23521)+insaneaa.std.Trim(23522, 23793)+insaneaa2.std.Trim(23794, 23848)+insaneaa.std.Trim(23849, 31767)+ed+insaneaa.std.Trim(33926, 34045)+episode.std.Trim(34046, 34119)

mrgc = fvf.rfs(mrgc, havsfunc.QTGMC(mrgc, InputType=1,SourceMatch=3), "[1 237]")

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\05.png'), "[344 437]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\06.png'), "[14855 14950]")

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

