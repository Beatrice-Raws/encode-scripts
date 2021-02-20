from vapoursynth import core, VideoNode, GRAY, YUV
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc
import mvsfunc as mvf
import GradFun3 as gfa
import insaneAA
import cooldegrain
import finedehalo as fd
import HardAAp2 as hiaa
import descale as dsc
import psutil
p_handle = psutil.Process()
p_handle.cpu_affinity([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46])
core.num_threads = 24
def DiffRescaleMask(clip: VideoNode, descale_h: int = 874, descale_w: int = None, kernel: str = 'bicubic', b=0.33, c=0.33, mthr: int = 165) -> VideoNode:
    ''' Builds mask from difference of original and re-upscales clips '''
    funcName = 'DiffRescaleMask'
    if not isinstance(clip, VideoNode):
        raise TypeError(funcName + ': \"clip\" must be a clip!')
    descale_w = havsfunc.m4((clip.width * descale_h) / clip.height) if descale_w == None else descale_w
    dclip = dsc.Descale(clip, descale_w, descale_h, kernel=kernel, b=b, c=c)
    uclip = core.fmtc.resample(dclip, clip.width, clip.height, kernel=kernel, a1=b, a2=c).fmtc.bitdepth(bits=8)
    uclip = core.std.ShufflePlanes(uclip, 0, GRAY)
    clip = core.std.ShufflePlanes(clip, 0, GRAY)
    diff = core.std.MakeDiff(clip, uclip)
    mask = diff.rgvs.RemoveGrain(2).rgvs.RemoveGrain(2).hist.Luma()
    mask = mask.std.Expr('x {thr} < 0 x ?'.format(thr=mthr))
    mask = mask.std.Prewitt().std.Maximum().std.Maximum().std.Deflate()
    return mask

def Wotaku_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=873, bicubic_b=0.33, bicubic_c=0.33)
    graydh = fd.fine_dehalo(desc, darkstr=0.2, brightstr=0.5, showmask=0, thmi=40, thma=60, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'04.dgi')
op_titles = core.std.Trim(episode, 1775, 3932)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(0, 2157)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(0, 2157)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 26782, 28940)
nced = core.raws.Source(r'NCED44.y4m').std.Trim(24, 2182)
nced_aa = core.raws.Source(r'NCED444.y4m').std.Trim(24, 2182)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Wotaku_aa(episode)
insaneaa1 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
mrgc = insaneaa.std.Trim(0, 938)+insaneaa1.std.Trim(939, 1706)+insaneaa.std.Trim(1707, 1774)+op+insaneaa1.std.Trim(3933, 4117)+insaneaa.std.Trim(4118, 6804)+insaneaa1.std.Trim(6805, 7644)+insaneaa.std.Trim(7645, 8975)+insaneaa1.std.Trim(8976, 9157)+insaneaa.std.Trim(9158, 9534)+insaneaa1.std.Trim(9535, 10042)+insaneaa.std.Trim(10043, 10162)+insaneaa1.std.Trim(10163, 10390)+insaneaa.std.Trim(10391, 10737)+insaneaa1.std.Trim(10738, 10832)+insaneaa.std.Trim(10833, 10966)+insaneaa1.std.Trim(10967, 11349)+insaneaa.std.Trim(11350, 12770)+insaneaa1.std.Trim(12771, 12960)+insaneaa.std.Trim(12961, 13461)+insaneaa1.std.Trim(13462, 13714)+insaneaa.std.Trim(13715, 14458)+episode.std.Trim(14459, 14578)+insaneaa1.std.Trim(14579, 14692)+insaneaa.std.Trim(14693, 15027)+insaneaa1.std.Trim(15028, 15470)+insaneaa.std.Trim(15471, 16867)+insaneaa1.std.Trim(16868, 17034)+insaneaa.std.Trim(17035, 17205)+insaneaa1.std.Trim(17206, 17480)+insaneaa.std.Trim(17481, 17748)+insaneaa1.std.Trim(17749, 18225)+insaneaa.std.Trim(18226, 21093)+insaneaa1.std.Trim(21094, 21439)+insaneaa.std.Trim(21440, 21863)+insaneaa1.std.Trim(21864, 21910)+insaneaa.std.Trim(21911, 22693)+insaneaa1.std.Trim(22694, 23243)+insaneaa.std.Trim(23244, 23506)+insaneaa1.std.Trim(23507, 24062)+insaneaa.std.Trim(24063, 24081)+episode.std.Trim(24082, 24202)+insaneaa1.std.Trim(24203, 24532)+insaneaa.std.Trim(24533, 24769)+insaneaa1.std.Trim(24770, 24966)+insaneaa.std.Trim(24967, 25335)+insaneaa1.std.Trim(25336, 25634)+insaneaa.std.Trim(25635, 26232)+insaneaa1.std.Trim(26233, 26781)+ed+insaneaa.std.Trim(28941, 31484)+insaneaa1.std.Trim(31485, 31908)+insaneaa.std.Trim(31909, 32846)+episode.std.Trim(32847, 32871)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\13.png'), "[5420 5496]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\14.png'), "[11386 11444]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\15.png'), "[12696 12770]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\16.png'), "[18339 18409]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\17.png'), "[18451 18515]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\18.png'), "[26706 26781]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
clip_y = mvf.GetPlane(clip16, 0)
pf = core.dfttest.DFTTest(clip_y, sigma=7, tbsize=3, opt=3)
den_y = cooldegrain.CoolDegrain(clip_y, tr=1, thsad=34, thsadc=34, bits=16, blksize=8, overlap=4, pf=pf)
filtered = core.std.ShufflePlanes([den_y, clip16, clip16], [0,1,2], colorfamily=clip16.format.color_family)
db = gfa.GradFun3(filtered, smode=6, thr_det=2, grainy=28, grainc=24,tv_range=True, planes=[0])
harddb = core.f3kdb.Deband(filtered, range=8, y=42, cb=26, cr=26, grainy=110, grainc=80, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, openCL=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(harddb, clip16, Mask2, planes=[0,1,2], first_plane=True)
filteredmix = core.std.Expr([filtered2, clip16], 'x {val} * y 1 {val} - * +'.format(val=0.26))
episode3 = core.fmtc.bitdepth(filteredmix, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
mrgc2 = episode3.std.Trim(0, 24698)+episode4.std.Trim(24699, 24769)+episode3.std.Trim(24770, 32871)
mrgc2.set_output()
