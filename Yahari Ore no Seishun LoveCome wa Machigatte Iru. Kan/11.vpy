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
episode = core.dgdecodenv.DGSource(r'11.dgi')
insaneaa = oreigaru3_aa(episode)
stab0 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=1)
stab2 = havsfunc.QTGMC(stab, InputType=1, SourceMatch=2)
stab3 = havsfunc.QTGMC(stab2, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 15787)+stab0.std.Trim(15788, 15985)+insaneaa.std.Trim(15986, 16538)+stab0.std.Trim(16539, 16652)+insaneaa.std.Trim(16653, 17717)+stab3.std.Trim(17718, 17915)+insaneaa.std.Trim(17916, 32511)+episode.std.Trim(32512, 33949)+insaneaa.std.Trim(33950, 34597)+episode.std.Trim(34598, 34695)
 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\01.png'), "[1423 1530]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\02.png'), "[1635 1730]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\03.png'), "[1782 1877]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\04.png'), "[1878 1959]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\05.png'), "[1960 2079]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\06.png'), "[2151 2234]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\07.png'), "[2241 2324]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\08.png'), "[2351 2434]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\09.png'), "[2502 2585]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\10.png'), "[2624 2719]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\11.png'), "[2742 2855]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, episode, r'.\mask\11\12.png'), "[2949 3068]")

stab4 = havsfunc.QTGMC(mrgc, InputType=1, SourceMatch=1)
stab5 = havsfunc.QTGMC(stab4, InputType=1, SourceMatch=2)
stab6 = havsfunc.QTGMC(stab5, InputType=1, SourceMatch=3)

mrgc2 = mrgc.std.Trim(0, 2150)+stab6.std.Trim(2151, 2327)+mrgc.std.Trim(2328, 2501)+stab6.std.Trim(2502, 2697)+mrgc.std.Trim(2698, 34695)
 
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










