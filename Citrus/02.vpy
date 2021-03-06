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

def CitrusED(clip):
  def aaFunc(video):
    aaclip = insaneAA.rescale(video, fasterAA=False, eedi3Mode=dict(first=dict(mode='cpu'), second=dict(mode='cpu')), nnedi3Mode=dict(first=dict(mode='opencl', device=0), second=dict(mode='opencl', device=0)), dx=video.width, dy=video.height)
    final = core.std.Expr([video, aaclip], 'x 0.4 * y 0.6 * +')
    return final
  clipY=clip.std.ShufflePlanes(0, GRAY)
  clipU=clip.std.ShufflePlanes(1, GRAY)
  clipV=clip.std.ShufflePlanes(2, GRAY)
  aaY = aaFunc(clipY)
  aaU = aaFunc(clipU)
  aaV = aaFunc(clipV)
  return core.std.ShufflePlanes([aaY,aaU,aaV], [0,0,0], clip.format.color_family)
  
core.set_max_cache_size(30000)

episode = core.dgdecodenv.DGSource(r'02.dgi')
op_titles = core.std.Trim(episode, 3, 2157)
ed_titles = core.std.Trim(episode, 31529, 32361)
ed_titles2 = core.std.Trim(episode, 32781, 33685)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(3, 2157)
nced = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(1, 833)
nced2 = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(1253, 2157)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(3, 2157)
nced_aa = core.raws.Source(r'NCED.y4m').std.Trim(1, 833)
nced_aa2 = core.raws.Source(r'NCED.y4m').std.Trim(1253, 2157)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
ed2 = atf.ApplyCredits(ed_titles2, nced2, nced_aa2)
ed3 = CitrusED(episode).std.Trim(32362, 32780)
stab = haf.QTGMC(ed3,InputType=1,SourceMatch=3)


insaneaa = insaneAA.insaneAA(episode, eedi3Mode=dict(mode='cpu'), nnedi3Mode=dict(mode='opencl', device=0), descale_str=0.28, kernel='bicubic', descale_h=720, outputMode=0)

mrgc = insaneaa.std.Trim(0, 2)+op+insaneaa.std.Trim(2158, 31528)+ed+stab+ed2+insaneaa.std.Trim(33686, 34045)+episode.std.Trim(34046, 34069)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\02.png'), "[2365 2475]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\002.png'), "[32389 32475]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\0002.png'), "[32490 32576]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\00002.png'), "[32589 32680]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\022.png'), "[33944 34045]")

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


