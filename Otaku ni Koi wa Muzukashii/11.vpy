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
episode = core.dgdecodenv.DGSource(r'11.dgi')
op_titles = core.std.Trim(episode, 2735, 3877)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(0, 1142)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(0, 1142)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
op_titles2 = core.std.Trim(episode, 4004, 4890)
ncop2 = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(1269, 2155)
ncop_aa2 = core.raws.Source(r'NCOP.y4m').std.Trim(1269, 2155)
op2 = atf.ApplyCredits(op_titles2, ncop2, ncop_aa2)
ed_titles = core.std.Trim(episode, 26686, 28843)
nced = core.raws.Source(r'NCED50.y4m').std.Trim(25, 2182)
nced_aa = core.raws.Source(r'NCED5.y4m').std.Trim(25, 2182)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Wotaku_aa(episode)
insaneaa1 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)

mrgc = insaneaa1.std.Trim(0, 71)+insaneaa.std.Trim(72, 1410)+insaneaa1.std.Trim(1411, 1487)+insaneaa.std.Trim(1488, 2734)+op+insaneaa.std.Trim(3878, 4003)+op2+insaneaa.std.Trim(4891, 5405)+insaneaa1.std.Trim(5406, 5635)+insaneaa.std.Trim(5636, 8603)+insaneaa1.std.Trim(8604, 8878)+insaneaa.std.Trim(8879, 9887)+insaneaa1.std.Trim(9888, 10071)+insaneaa.std.Trim(10072, 10967)+insaneaa1.std.Trim(10968, 11339)+insaneaa.std.Trim(11340, 11844)+episode.std.Trim(11845, 11964)+insaneaa.std.Trim(11965, 13461)+insaneaa1.std.Trim(13462, 13655)+insaneaa.std.Trim(13656, 14706)+insaneaa1.std.Trim(14707, 15700)+insaneaa.std.Trim(15701, 17390)+insaneaa1.std.Trim(17391, 17678)+insaneaa.std.Trim(17679, 21146)+insaneaa1.std.Trim(21147, 21263)+insaneaa.std.Trim(21264, 24188)+insaneaa1.std.Trim(24189, 24386)+insaneaa.std.Trim(24387, 26685)+ed+insaneaa1.std.Trim(28844, 29451)+insaneaa.std.Trim(29452, 30267)+insaneaa1.std.Trim(30268, 30548)+insaneaa.std.Trim(30549, 31590)+insaneaa1.std.Trim(31591, 31709)+insaneaa.std.Trim(31710, 32443)+insaneaa1.std.Trim(32444, 32840)+episode.std.Trim(32841, 32871)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\3100.png'), "[3881 3927]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\3200.png'), "[3928 3978]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\31.png'), "[5107 5177]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\32.png'), "[26559 26683]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\33.png'), "[32719 32837]")


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
mrgc2 = episode3.std.Trim(0, 7077)+episode4.std.Trim(7078, 7219)+episode3.std.Trim(7220, 7360)+episode4.std.Trim(7361, 7455)+episode3.std.Trim(7456, 9607)+episode4.std.Trim(9608, 9798)+episode3.std.Trim(9799, 15835)+episode4.std.Trim(15836, 15930)+episode3.std.Trim(15931, 26396)+episode4.std.Trim(26397, 26684)+episode3.std.Trim(26685, 32871)
mrgc2.set_output()
