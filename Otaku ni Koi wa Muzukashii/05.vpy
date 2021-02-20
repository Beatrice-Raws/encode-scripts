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

def Wotaku_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=873, bicubic_b=0.33, bicubic_c=0.33)
    graydh = fd.fine_dehalo(desc, darkstr=0.2, brightstr=0.5, showmask=0, thmi=40, thma=60, useMtEdge=True)
    hardaa = hiaa.HardAA(graydh, mask='simple', mthr=80)
    rescale = insaneAA.rescale(hardaa, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'05.dgi')
op_titles = core.std.Trim(episode, 2471, 3663)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(0, 1192)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(0, 1192)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
op_titles2 = core.std.Trim(episode, 3740, 4626)
ncop2 = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(1269, 2155)
ncop_aa2 = core.raws.Source(r'NCOP.y4m').std.Trim(1269, 2155)
op2 = atf.ApplyCredits(op_titles2, ncop2, ncop_aa2)
ed_titles = core.std.Trim(episode, 29514, 31671)
nced = core.raws.Source(r'NCED55.y4m').std.Trim(25, 2182)
nced_aa = core.raws.Source(r'NCED555.y4m').std.Trim(25, 2182)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = Wotaku_aa(episode)
insaneaa2 = Wotaku_aa2(episode)
insaneaa1 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 543)+insaneaa1.std.Trim(544, 653)+insaneaa.std.Trim(654, 1381)+insaneaa1.std.Trim(1382, 1620)+insaneaa.std.Trim(1621, 1685)+insaneaa2.std.Trim(1686, 2044)+insaneaa1.std.Trim(2045, 2199)+insaneaa.std.Trim(2200, 2470)+op+insaneaa.std.Trim(3664, 3739)+op2+insaneaa1.std.Trim(4627, 4706)+insaneaa.std.Trim(4707, 4972)+insaneaa1.std.Trim(4973, 5184)+insaneaa.std.Trim(5185, 5293)+insaneaa1.std.Trim(5294, 5388)+insaneaa.std.Trim(5389, 5620)+insaneaa1.std.Trim(5621, 5714)+insaneaa.std.Trim(5715, 5941)+insaneaa1.std.Trim(5942, 6459)+insaneaa.std.Trim(6460, 7029)+insaneaa1.std.Trim(7030, 7387)+insaneaa.std.Trim(7388, 7621)+insaneaa2.std.Trim(7622, 7758)+insaneaa.std.Trim(7759, 8618)+insaneaa1.std.Trim(8619, 8691)+insaneaa.std.Trim(8692, 9015)+insaneaa1.std.Trim(9016, 9134)+insaneaa.std.Trim(9135, 9468)+insaneaa1.std.Trim(9469, 9525)+insaneaa.std.Trim(9526, 9957)+insaneaa1.std.Trim(9958, 10244)+insaneaa.std.Trim(10245, 10499)+insaneaa1.std.Trim(10500, 10805)+insaneaa.std.Trim(10806, 11128)+insaneaa1.std.Trim(11129, 11462)+insaneaa.std.Trim(11463, 11665)+insaneaa1.std.Trim(11666, 12722)+insaneaa.std.Trim(12723, 12847)+insaneaa1.std.Trim(12848, 13012)+insaneaa.std.Trim(13013, 13248)+insaneaa1.std.Trim(13249, 13331)+insaneaa.std.Trim(13332, 13834)+insaneaa1.std.Trim(13835, 13953)+insaneaa.std.Trim(13954, 14282)+insaneaa1.std.Trim(14283, 14674)+insaneaa.std.Trim(14675, 15607)+episode.std.Trim(15608, 15727)+insaneaa.std.Trim(15728, 16283)+insaneaa1.std.Trim(16284, 16628)+insaneaa.std.Trim(16629, 17278)+insaneaa1.std.Trim(17279, 17604)+insaneaa.std.Trim(17605, 17729)+insaneaa1.std.Trim(17730, 18147)+insaneaa.std.Trim(18148, 18314)+insaneaa1.std.Trim(18315, 18828)+insaneaa.std.Trim(18829, 18899)+insaneaa1.std.Trim(18900, 19459)+insaneaa.std.Trim(19460, 20394)+insaneaa1.std.Trim(20395, 20693)+insaneaa.std.Trim(20694, 22367)+insaneaa1.std.Trim(22368, 22642)+insaneaa.std.Trim(22643, 22856)+insaneaa1.std.Trim(22857, 23578)+insaneaa.std.Trim(23579, 24654)+insaneaa1.std.Trim(24655, 24827)+insaneaa.std.Trim(24828, 25207)+insaneaa1.std.Trim(25208, 25815)+insaneaa.std.Trim(25816, 26631)+insaneaa1.std.Trim(26632, 27161)+insaneaa.std.Trim(27162, 27855)+insaneaa1.std.Trim(27856, 28554)+insaneaa.std.Trim(28555, 28719)+insaneaa1.std.Trim(28720, 28939)+insaneaa.std.Trim(28940, 29029)+insaneaa1.std.Trim(29030, 29100)+insaneaa.std.Trim(29101, 29513)+ed+insaneaa.std.Trim(31672, 32005)+insaneaa1.std.Trim(32006, 32124)+insaneaa.std.Trim(32125, 32210)+insaneaa1.std.Trim(32211, 32845)+episode.std.Trim(32846, 32871)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\1090.png'), "[3664 3714]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\1091.png'), "[28972 29029]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\19.png'), "[29434 29512]")


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
mrgc2 = episode3.std.Trim(0, 32871)
mrgc2.set_output()
