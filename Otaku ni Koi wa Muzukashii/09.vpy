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
episode = core.dgdecodenv.DGSource(r'09.dgi')
op_titles = core.std.Trim(episode, 5012, 6204)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(0, 1192)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(0, 1192)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
op_titles2 = core.std.Trim(episode, 6281, 7167)
ncop2 = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(1269, 2155)
ncop_aa2 = core.raws.Source(r'NCOP.y4m').std.Trim(1269, 2155)
op2 = atf.ApplyCredits(op_titles2, ncop2, ncop_aa2)
insaneaa = Wotaku_aa(episode)
insaneaa1 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 215)+insaneaa1.std.Trim(216, 299)+insaneaa.std.Trim(300, 507)+insaneaa1.std.Trim(508, 746)+insaneaa.std.Trim(747, 1527)+insaneaa1.std.Trim(1528, 1647)+insaneaa.std.Trim(1648, 3278)+insaneaa1.std.Trim(3279, 3794)+insaneaa.std.Trim(3795, 4196)+insaneaa1.std.Trim(4197, 4291)+insaneaa.std.Trim(4292, 5011)+op+insaneaa.std.Trim(6205, 6280)+op2+insaneaa.std.Trim(7168, 8202)+insaneaa1.std.Trim(8203, 8543)+insaneaa.std.Trim(8544, 14408)+insaneaa.std.Trim(14409, 15827)+insaneaa1.std.Trim(15828, 16133)+insaneaa.std.Trim(16134, 19331)+insaneaa1.std.Trim(19332, 19631)+insaneaa.std.Trim(19632, 22468)+insaneaa1.std.Trim(22469, 22599)+insaneaa.std.Trim(22600, 24376)+insaneaa1.std.Trim(24377, 24628)+insaneaa.std.Trim(24629, 25634)+insaneaa1.std.Trim(25635, 26327)+insaneaa.std.Trim(26328, 27811)+insaneaa1.std.Trim(27812, 28021)+insaneaa.std.Trim(28022, 28329)+insaneaa1.std.Trim(28330, 28484)+insaneaa.std.Trim(28485, 28651)+insaneaa1.std.Trim(28652, 28837)+insaneaa.std.Trim(28838, 28888)+insaneaa1.std.Trim(28889, 29723)+insaneaa.std.Trim(29724, 30841)+episode.std.Trim(30842, 32693)+insaneaa.std.Trim(32694, 32869)+episode.std.Trim(32870, 32895)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\2700.png'), "[6205 6255]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\Mask\27.png'), "[30466 30544]")

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
mrgc2 = episode3.std.Trim(0, 12000)+episode4.std.Trim(12001, 12048)+episode3.std.Trim(12049, 12652)+episode4.std.Trim(12653, 13183)+episode3.std.Trim(13184, 13278)+episode4.std.Trim(13279, 13525)+episode3.std.Trim(13526, 13770)+episode4.std.Trim(13771, 13901)+episode3.std.Trim(13902, 15374)+episode4.std.Trim(15375, 15607)+episode3.std.Trim(15608, 17218)+episode4.std.Trim(17219, 17374)+episode3.std.Trim(17375, 17715)+episode4.std.Trim(17716, 17894)+episode3.std.Trim(17895, 18168)+episode4.std.Trim(18169, 18644)+episode3.std.Trim(18645, 22252)+episode4.std.Trim(22253, 22347)+episode3.std.Trim(22348, 32895)
mrgc2.set_output()
