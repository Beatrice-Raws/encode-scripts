from vapoursynth import *
import vapoursynth as vs
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import insaneAA
import cooldegrain
import HardAAp2 as hiaa
import havsfunc as haf
import kagefunc as kg
import vsTAAmbk as taa
core.set_max_cache_size(30000)

episode = core.dgdecodenv.DGSource(r'NCED.dgi')

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
  
ed = CitrusED(episode)
stab = haf.QTGMC(ed,InputType=1,SourceMatch=3)
clip16 = core.fmtc.bitdepth(stab, bits=16)
dn = cooldegrain.CoolDegrain(clip16, tr=1, thsad=48, thsadc=48, bits=16, blksize=8, overlap=4)
db = gfa.GradFun3(dn, smode=6, thr_det=2,tv_range=True, planes=[0])
Mask = kg.retinex_edgemask(clip16, sigma=0.6, draft=False)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered, bits=10)
episode3.set_output()



