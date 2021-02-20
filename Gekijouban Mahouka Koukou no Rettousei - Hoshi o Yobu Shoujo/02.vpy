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
def Mahouka_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bilinear', descale_height=810) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    hardaa = hiaa.HardAA(graydh, mask='simple', mthr=60, alpha=0.4, beta=0.25, gamma=20.0, nrad=3, mdis=40, useCL=True, sangnomPP=False)
    rescale1 = insaneAA.rescale(hardaa, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)
    rescale2 = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)
    rescale = core.std.Expr([rescale2, rescale1], 'x 0.60 * y 0.40 * +')   
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv 
 
core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'00000.dgi')
insaneaa = Mahouka_aa(episode)
Hard = hiaa.HardAA(insaneaa, mask=None, alpha=0.9, beta=0.1, gamma=200.0, nrad=3, mdis=40, useCL=True, sangnomPP=True)
Hard = hiaa.HardAA(Hard, mask=None, alpha=0.9, beta=0.1, gamma=200.0, nrad=3, mdis=40, useCL=True, sangnomPP=True)
Hard = hiaa.HardAA(Hard, mask=None, alpha=0.9, beta=0.1, gamma=200.0, nrad=3, mdis=40, useCL=True, sangnomPP=True)

mrgc = insaneaa.std.Trim(0, 5246) + episode.std.Trim(5247, 5495) + insaneaa.std.Trim(5496, 116263) + Hard.std.Trim(116264, 116335) + insaneaa.std.Trim(116336, 122777) + episode.std.Trim(122778, 128655) + insaneaa.std.Trim(128656, 129161) + episode.std.Trim(129162, 129335)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[102 197]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\02.png'), "[5759 5853]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\03.png'), "[8259 8392]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\04.png'), "[14623 14698]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\05.png'), "[16637 16725]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\06.png'), "[19377 19476]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\07.png'), "[21079 21180]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[60920 60996]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\09.png'), "[61030 61143]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10.png'), "[121376 121452]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11.png'), "[121690 121757]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\12.png'), "[122070 122170]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\13.png'), "[128704 128774]")

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\fix.png'), "[116264 116335]")

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\14.png'), "[563 679]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\15.png'), "[742 841]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\16.png'), "[963 1082]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\17.png'), "[1544 1663]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\18.png'), "[1747 1866]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\19.png'), "[2101 2206]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\20.png'), "[2341 2446]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\21.png'), "[2521 2635]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\22.png'), "[2686 2794]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\23.png'), "[2943 3042]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\24.png'), "[3076 3193]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\25.png'), "[3255 3352]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=26, thsadc=24, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=24, y=16, cb=8, cr=8, grainy=16, grainc=16, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()







