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
episode = core.avs.DGSourceIM(r'21.dgi', engine=2)
op_titles = core.std.Trim(episode, 1377, 3524)
ncop = core.avs.DGSourceIM(r'NCOP3.dgi').std.Trim(33, 2180)
ncop_aa = core.raws.Source(r'NCOP3.y4m').std.Trim(33, 2180)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 31769, 33926)
nced = core.avs.DGSourceIM(r'NCED3_1.dgi').std.Trim(24, 2181)
nced_aa = core.raws.Source(r'NCED3_1.y4m').std.Trim(24, 2181)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(mode='cpu'), nnedi3Mode=dict(mode='nnedi3'), descale_str=0.28, kernel='bicubic', descale_h=720)
insaneaa2 = hiaa.HardAA(episode, mask='simplecmb', mthr=30)
insaneaa3 = havsfunc.QTGMC(insaneaa2, InputType=1,SourceMatch=3)


mrgc = insaneaa.std.Trim(0, 1376)+op+insaneaa.std.Trim(3525, 10152)+insaneaa2.std.Trim(10153, 10241)+insaneaa.std.Trim(10242, 10319)+insaneaa2.std.Trim(10320, 10454)+insaneaa.std.Trim(10455, 17760)+insaneaa2.std.Trim(17761, 17873)+insaneaa.std.Trim(17874, 18197)+insaneaa2.std.Trim(18198, 18352)+insaneaa.std.Trim(18353, 18814)+insaneaa3.std.Trim(18815, 18873)+insaneaa.std.Trim(18874, 25921)+insaneaa2.std.Trim(25922, 26018)+insaneaa.std.Trim(26019, 26130)+insaneaa2.std.Trim(26131, 26202)+insaneaa.std.Trim(26203, 26487)+insaneaa2.std.Trim(26488, 26666)+insaneaa.std.Trim(26667, 26767)+insaneaa2.std.Trim(26768, 27151)+insaneaa.std.Trim(27152, 30277)+insaneaa3.std.Trim(30278, 30318)+insaneaa.std.Trim(30319, 31167)+insaneaa3.std.Trim(31168, 31217)+insaneaa.std.Trim(31218, 31244)+insaneaa3.std.Trim(31245, 31272)+insaneaa.std.Trim(31273, 31415)+insaneaa2.std.Trim(31416, 31474)+insaneaa.std.Trim(31475, 31768)+ed+insaneaa.std.Trim(33927, 34046)+episode.std.Trim(34047, 34095)

mrgc = fvf.rfs(mrgc, havsfunc.QTGMC(mrgc, InputType=1,SourceMatch=3), "[16530 16624]")
mrgc = fvf.rfs(mrgc, havsfunc.QTGMC(mrgc, InputType=1,SourceMatch=3), "[18990 19126]")
mrgc = fvf.rfs(mrgc, havsfunc.QTGMC(mrgc, InputType=1,SourceMatch=3), "[23009 23367]")
mrgc = fvf.rfs(mrgc, havsfunc.QTGMC(mrgc, InputType=1,SourceMatch=3), "[25328 25376]")
mrgc = fvf.rfs(mrgc, havsfunc.QTGMC(mrgc, InputType=1,SourceMatch=3), "[25637 25755]")

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
Mask = kg.retinex_edgemask(clip16, sigma=0.1, draft=False)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.14))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode3.set_output()

