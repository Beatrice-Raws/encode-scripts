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
episode = core.avs.DGSourceIM(r'03.dgi', engine=2)
op_titles = core.std.Trim(episode, 651, 2805)
ncop = core.avs.DGSourceIM(r'NCOP1.dgi').std.Trim(27, 2181)
ncop_aa = core.raws.Source(r'NCOP1.y4m').std.Trim(27, 2181)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 31770, 33927)
nced = core.avs.DGSourceIM(r'NCED1.dgi').std.Trim(24, 2181)
nced_aa = core.raws.Source(r'NCED1.y4m').std.Trim(24, 2181)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(mode='cpu'), nnedi3Mode=dict(mode='nnedi3'), descale_str=0.28, kernel='bicubic', descale_h=720)
insaneaa2 = hiaa.HardAA(episode, mask='simplecmb', mthr=30)


mrgc = insaneaa.std.Trim(0, 650)+op+insaneaa.std.Trim(2806, 31769)+ed+insaneaa.std.Trim(33928, 34047)+episode.std.Trim(34048, 34095)


#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip = mrgc
inputY = core.std.ShufflePlanes(clip, 0, GRAY)
descaledY = insaneAA.revert_upscale(inputY, descale_str=0.35, kernel='bicubic', descale_h=720)
resizedY = core.resize.Bicubic(descaledY, 1280, 720)
resizedUV = core.resize.Bicubic(clip, 1280, 720,)
out = core.std.ShufflePlanes([resizedY,resizedUV,resizedUV], [0,1,2], clip.format.color_family)
clip16 = core.fmtc.bitdepth(out, bits=16)
clip_y = mvf.GetPlane(clip16, 0)
pf = core.dfttest.DFTTest(clip_y, sigma=4, tbsize=3, opt=1)
den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=28, thsadc=28, bits=16, blksize=8, overlap=4, pf=pf)
filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(filtered, smode=6, thr_det=2, grainy=32, grainc=22,tv_range=True, planes=[0])
harddb = core.f3kdb.Deband(filtered, range=8, y=64, cb=48, cr=48, grainy=160, grainc=120, output_depth=16, keep_tv_range=True)
Mask = kg.retinex_edgemask(clip16, sigma=0.1, draft=False)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(harddb, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.14))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
mrgc2 = episode3.std.Trim(0, 31673)+episode4.std.Trim(31674, 31769)+episode3.std.Trim(31770, 34095)
mrgc2.set_output()


