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
episode = core.dgdecodenv.DGSource(r'08.dgi')
op_titles = core.std.Trim(episode, 649, 1841)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(0, 1192)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(0, 1192)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
op_titles2 = core.std.Trim(episode, 1918, 2804)
ncop2 = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(1269, 2155)
ncop_aa2 = core.raws.Source(r'NCOP.y4m').std.Trim(1269, 2155)
op2 = atf.ApplyCredits(op_titles2, ncop2, ncop_aa2)
ed_titles = core.std.Trim(episode, 30692, 32847)
nced = core.raws.Source(r'NCED30.y4m').std.Trim(25, 2180)
nced_aa = core.raws.Source(r'NCED3.y4m').std.Trim(25, 2180)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Wotaku_aa(episode)
insaneaa1 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 648)+op+insaneaa.std.Trim(1842, 1917)+op2+insaneaa.std.Trim(2805, 5240)+insaneaa1.std.Trim(5241, 6158)+insaneaa.std.Trim(6159, 6224)+insaneaa1.std.Trim(6225, 6565)+insaneaa.std.Trim(6566, 8419)+insaneaa1.std.Trim(8420, 8526)+insaneaa.std.Trim(8527, 8610)+insaneaa1.std.Trim(8611, 8717)+insaneaa.std.Trim(8718, 10050)+insaneaa1.std.Trim(10051, 10965)+insaneaa.std.Trim(10966, 11078)+insaneaa1.std.Trim(11079, 11317)+insaneaa.std.Trim(11318, 13906)+insaneaa1.std.Trim(13907, 14293)+insaneaa.std.Trim(14294, 14485)+episode.std.Trim(14486, 14532)+insaneaa1.std.Trim(14533, 14979)+insaneaa.std.Trim(14980, 15171)+insaneaa1.std.Trim(15172, 15218)+insaneaa.std.Trim(15219, 15302)+episode.std.Trim(15303, 15369)+insaneaa1.std.Trim(15370, 15900)+insaneaa.std.Trim(15901, 17465)+insaneaa1.std.Trim(17466, 17644)+insaneaa.std.Trim(17645, 17810)+insaneaa1.std.Trim(17811, 18443)+insaneaa.std.Trim(18444, 18569)+insaneaa1.std.Trim(18570, 18630)+insaneaa.std.Trim(18631, 18805)+insaneaa1.std.Trim(18806, 18876)+insaneaa.std.Trim(18877, 21897)+insaneaa1.std.Trim(21898, 21980)+insaneaa.std.Trim(21981, 22261)+insaneaa1.std.Trim(22262, 22596)+insaneaa.std.Trim(22597, 22702)+insaneaa1.std.Trim(22703, 22797)+insaneaa.std.Trim(22798, 23593)+insaneaa1.std.Trim(23594, 23903)+insaneaa.std.Trim(23904, 23960)+insaneaa1.std.Trim(23961, 24431)+insaneaa.std.Trim(24432, 24652)+insaneaa1.std.Trim(24653, 24864)+insaneaa.std.Trim(24865, 25573)+insaneaa1.std.Trim(25574, 25692)+insaneaa.std.Trim(25693, 25851)+insaneaa1.std.Trim(25852, 26059)+insaneaa.std.Trim(26060, 27676)+insaneaa1.std.Trim(27677, 27897)+insaneaa.std.Trim(27898, 28723)+insaneaa1.std.Trim(28724, 28782)+insaneaa.std.Trim(28783, 30082)+insaneaa1.std.Trim(30083, 30691)+ed+episode.std.Trim(32848, 32871)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\2500.png'), "[1842 1892]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\2577.png'), "[13787 13906]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\25.png'), "[30571 30614]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\26.png'), "[30615 30690]")

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
mrgc2 = episode3.std.Trim(0, 11222)+episode4.std.Trim(11223, 11317)+episode3.std.Trim(11318, 11380)+episode4.std.Trim(11381, 11937)+episode3.std.Trim(11938, 12891)+episode4.std.Trim(12892, 13189)+episode3.std.Trim(13190, 32871)
mrgc2.set_output()
