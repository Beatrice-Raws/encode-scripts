from vapoursynth import core, VideoNode, GRAY8, YUV, GRAY
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

def oreigaru3_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=0.78, showmask=0, thmi=24, thma=100, rx=2.4, ry=2.4)
    return mixyuv
     
core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'10.dgi')
op_titles = core.std.Trim(episode, 1152, 3308)
ncop = core.dgdecodenv.DGSource(r'NCOP4.dgi').std.Trim(0, 2156)
ncop_aa = core.raws.Source(r'NCOP4.y4m').std.Trim(0, 2156)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
insaneaa = oreigaru3_aa(episode)
stab0 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=1)
stab2 = havsfunc.QTGMC(stab, InputType=1, SourceMatch=2)
stab3 = havsfunc.QTGMC(stab2, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 1151)+op+insaneaa.std.Trim(3309, 4621)+stab3.std.Trim(4622, 4819)+insaneaa.std.Trim(4820, 7158)+stab3.std.Trim(7159, 7332)+insaneaa.std.Trim(7333, 13811)+stab3.std.Trim(13812, 13940)+insaneaa.std.Trim(13941, 27357)+stab3.std.Trim(27358, 27531)+insaneaa.std.Trim(27532, 30594)+stab0.std.Trim(30595, 30714)+insaneaa.std.Trim(30715, 33829)+episode.std.Trim(33830, 33925)+insaneaa.std.Trim(33926, 34573)+episode.std.Trim(34574, 34671)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\01.png'), "[32095 32185]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\02.png'), "[32258 32363]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\03.png'), "[32376 32464]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\04.png'), "[32485 32577]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\05.png'), "[32599 32692]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\06.png'), "[32712 32805]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\07.png'), "[32825 32914]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\08.png'), "[33017 33104]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\09.png'), "[33131 33202]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\10.png'), "[33411 33498]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\11.png'), "[33511 33598]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\10\12.png'), "[33626 33721]")

stab4 = havsfunc.QTGMC(mrgc, InputType=1, SourceMatch=1)
stab5 = havsfunc.QTGMC(stab4, InputType=1, SourceMatch=2)
stab6 = havsfunc.QTGMC(stab5, InputType=1, SourceMatch=3)

mrgc2 = mrgc.std.Trim(0, 32087)+stab6.std.Trim(32088, 32195)+mrgc.std.Trim(32196, 34671)
  
#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc2, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=18, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=20, cb=10, cr=10, grainy=28, grainc=28, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()










