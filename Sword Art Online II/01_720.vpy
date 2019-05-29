from vapoursynth import core, VideoNode, GRAY
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import gradfun_amod as gfa
import insaneAA 
import cooldegrain
core.avs.LoadPlugin(r'C:\encoder\dgdecim\x64\DGDecodeIM.dll')  
def titles_mask(clip):
    rescaled = clip.resize.Spline36(1280, 720).resize.Spline36(1920, 1080)
    diff = core.std.MakeDiff(clip, rescaled, [0,1,2])
    mask = diff.std.Prewitt([0]).std.Expr('x 40 < 0 x ?').rgvs.RemoveGrain(2).std.Maximum().std.Minimum([0],60).std.Inflate()
    return mask
    
core.max_cache_size = 20000
episode = core.avs.DGSourceIM(r'01.dgi', engine=2)
op_titles = core.std.Trim(episode, 31769, 33923)
ncop = core.avs.DGSourceIM(r'NCOP1.dgi').std.Trim(27, 2181)
ncop_aa = core.raws.Source(r'NCOP1.y4m').std.Trim(27, 2181)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(mode='cpu'), nnedi3Mode=dict(mode='nnedi3'), descale_str=0.28, kernel='bicubic', descale_h=720)


mrgc = insaneaa.std.Trim(0, 4698)+episode.std.Trim(4699, 4842)+insaneaa.std.Trim(4843, 31768)+op+insaneaa.std.Trim(33924, 34043)+episode.std.Trim(34044, 34091)

mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, titles_mask(episode), planes=[0], first_plane=True), "[228 931]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, titles_mask(episode), planes=[0], first_plane=True), "[2541 3016]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, titles_mask(episode), planes=[0], first_plane=True), "[3373 3884]")
mrgc = fvf.rfs(mrgc, core.std.MaskedMerge(mrgc, episode, titles_mask(episode), planes=[0], first_plane=True), "[4397 4647]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[12180 12243]")

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
Mask = kg.retinex_edgemask(clip16, sigma=0.1, draft=False)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.14))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode3.set_output()


