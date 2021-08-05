from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
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
import regress
p_handle = psutil.Process()
p_handle.cpu_affinity([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46])
core.num_threads = 24

def Demon_Slayer_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.48, kernel='bilinear', descale_height=855) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.6, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)   
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv

def Demon_Slayer_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.48, kernel='bilinear', descale_height=855) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.6, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)   
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30, useCL=True)
    return mixyuv

core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'00001.dgi')
#episode = core.fmtc.bitdepth(episode, bits=16)
insaneaa = Demon_Slayer_aa(episode)
insaneaa2 = Demon_Slayer_aa2(episode)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa2, InputType=1, SourceMatch=3)


mrgc = episode.std.Trim(0, 1033)+insaneaa.std.Trim(1034, 2228)+stab.std.Trim(2229, 2348)+insaneaa.std.Trim(2349, 3694)+episode.std.Trim(3695, 4180)+insaneaa.std.Trim(4181, 4432)+insaneaa2.std.Trim(4433, 4520)+insaneaa.std.Trim(4521, 7349)+stab.std.Trim(7350, 7883)+insaneaa.std.Trim(7884, 7946)+stab.std.Trim(7947, 8034)+insaneaa.std.Trim(8035, 25077)+stab.std.Trim(25078, 25443)+insaneaa.std.Trim(25444, 86558)+stab2.std.Trim(86559, 86640)+insaneaa.std.Trim(86641, 94152)+stab.std.Trim(94153, 94299)+insaneaa.std.Trim(94300, 102903)+stab.std.Trim(102904, 103024)+insaneaa.std.Trim(103025, 115324)+stab2.std.Trim(115325, 115440)+insaneaa.std.Trim(115441, 118352)+stab.std.Trim(118353, 118532)+insaneaa.std.Trim(118533, 120593)+stab.std.Trim(120594, 120772)+insaneaa.std.Trim(120773, 147903)+stab.std.Trim(147904, 148017)+insaneaa.std.Trim(148018, 152676)+stab.std.Trim(152677, 152784)+insaneaa.std.Trim(152785, 152952)+stab.std.Trim(152953, 153378)+insaneaa.std.Trim(153379, 161631)+episode.std.Trim(161632, 168023)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\01.png'), "[4237 4347]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\12.png'), "[4433 4520]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\02.png'), "[4529 4623]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\03.png'), "[4741 4847]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\04.png'), "[4949 5032]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\05.png'), "[5226 5354]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\06.png'), "[5605 5715]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\07.png'), "[6261 6382]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\08.png'), "[6493 6612]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\09.png'), "[7210 7324]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10.png'), "[7382 7511]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11.png'), "[7642 7883]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=24, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=30, y=12, cb=10, cr=10, grainy=14, grainc=14, output_depth=16, keep_tv_range=True)
db2 = core.f3kdb.Deband(den, range=31, y=32, cb=10, cr=10, grainy=28, grainc=28, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask2, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(db2, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
mrgc2 = episode3.std.Trim(0, 76937)+episode4.std.Trim(76938, 77111)+episode3.std.Trim(77112, 77357)+episode4.std.Trim(77358, 77494)+episode3.std.Trim(77495, 86039)+episode4.std.Trim(86040, 86297)+episode3.std.Trim(86298, 86745)+episode4.std.Trim(86746, 86784)+episode3.std.Trim(86785, 87717)+episode4.std.Trim(87718, 87881)+episode3.std.Trim(87882, 89783)+episode4.std.Trim(89784, 89856)+episode3.std.Trim(89857, 117953)+episode4.std.Trim(117954, 118049)+episode3.std.Trim(118050, 120383)+episode4.std.Trim(120384, 120593)+episode3.std.Trim(120594, 135602)+episode4.std.Trim(135603, 135756)+episode3.std.Trim(135757, 168023)
mrgc2.set_output()














