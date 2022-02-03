from vapoursynth import core, VideoNode, GRAY, YUV, GRAYS, GRAY8
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

def oreigaru3_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=0.78, showmask=0, thmi=24, thma=100, rx=2.4, ry=2.4)
    mixyuv = hiaa.HardAA(mixyuv, mask=None, useCL=False)
    return mixyuv
    
def oreigaru3_aa3(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080)
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=0.78, showmask=0, thmi=24, thma=100, rx=2.4, ry=2.4)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=40, useCL=False)
    return mixyuv    
    
def oreigaru3_aa2_5(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    clip1 = dsc.Descale(gray, 1136, 640, kernel="bilinear")
    clip1 = hiaa.HardAA(clip1, mask=None, alpha=0.9, beta=0.1, gamma=15.0, mdis=30)
    clip1 = insaneAA.rescale(clip1, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, pscrn=0, alpha=0.9, beta=0.1, gamma=10.0, mdis=30)
    mixyuv = core.std.ShufflePlanes([clip1, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, cplace="mpeg2", blur=40)
    mixyuv = hiaa.HardAA(mixyuv, mask=None, alpha=0.9, beta=0.1, gamma=15.0, mdis=30, useCL=False)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    return mixyuv    
    
def oreigaru3_aa2_6(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    clip1 = dsc.Descale(gray, 1136, 640, kernel="bilinear")
    clip1 = hiaa.HardAA(clip1, mask=None, alpha=0.9, beta=0.1, gamma=15.0, mdis=30)
    clip1 = insaneAA.rescale(clip1, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, pscrn=0, alpha=0.9, beta=0.1, gamma=10.0, mdis=30)
    mixyuv = core.std.ShufflePlanes([clip1, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = core.warp.AWarpSharp2(mixyuv, type=1, cplace="mpeg2", blur=60)
    mixyuv = hiaa.HardAA(mixyuv, mask=None, useCL=False)
    mixyuv = fd.fine_dehalo(mixyuv, darkstr=0, brightstr=1, showmask=0, thmi=42, thma=100, rx=2.4, ry=2.4)
    return mixyuv
          
def oreigaru3_aa2_7(clip):
    clip = clip
    clip = hiaa.HardAA(clip, mask='simple', mthr=40, useCL=False)
    return clip 
     
core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'05.dgi')
op_titles = core.std.Trim(episode, 3381, 5538)
ncop = core.dgdecodenv.DGSource(r'NCOP3.dgi').std.Trim(0, 2157)
ncop_aa = core.raws.Source(r'NCOP3.y4m').std.Trim(0, 2157)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 29732, 31888)
nced = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(0, 2156)
nced_aa = core.raws.Source(r'NCED.y4m').std.Trim(0, 2156)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = oreigaru3_aa(episode)
insaneaa2 = oreigaru3_aa2(episode)
insaneaa4 = oreigaru3_aa2_6(episode)
insaneaa6 = oreigaru3_aa2_5(episode)
insaneaa7 = oreigaru3_aa3(episode)
stab0 = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=1)
stab2 = havsfunc.QTGMC(stab, InputType=1, SourceMatch=2)
stab3 = havsfunc.QTGMC(stab2, InputType=1, SourceMatch=3)
stab7 = oreigaru3_aa2_7(stab3)
mask_clip = core.raws.Source(r'mask.yuv').std.Trim(39, 159).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final = core.std.MaskedMerge(insaneaa4.std.Trim(737, 857), insaneaa.std.Trim(737, 857), mask_clip, planes=[0], first_plane=True)
mask_clip2 = core.raws.Source(r'mask.yuv').std.Trim(182, 345).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final2 = core.std.MaskedMerge(insaneaa4.std.Trim(1652, 1815), insaneaa.std.Trim(1652, 1815), mask_clip2, planes=[0], first_plane=True)
mask_clip3 = core.raws.Source(r'mask.yuv').std.Trim(368, 631).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final3 = core.std.MaskedMerge(insaneaa6.std.Trim(2149, 2412), insaneaa.std.Trim(2149, 2412), mask_clip3, planes=[0], first_plane=True)
mask_clip4 = core.raws.Source(r'mask.yuv').std.Trim(714, 801).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final4 = core.std.MaskedMerge(insaneaa4.std.Trim(7464, 7551), insaneaa.std.Trim(7464, 7551), mask_clip4, planes=[0], first_plane=True)
mask_clip5 = core.raws.Source(r'mask.yuv').std.Trim(851, 1049).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final5 = core.std.MaskedMerge(insaneaa4.std.Trim(8143, 8341), insaneaa.std.Trim(8143, 8341), mask_clip5, planes=[0], first_plane=True)
mask_clip6 = core.raws.Source(r'mask.yuv').std.Trim(1071, 1196).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final6 = core.std.MaskedMerge(insaneaa4.std.Trim(9043, 9168), insaneaa.std.Trim(9043, 9168), mask_clip6, planes=[0], first_plane=True)
mask_clip8 = core.raws.Source(r'mask2.yuv').std.Trim(161, 236).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final8 = core.std.MaskedMerge(insaneaa6.std.Trim(5972, 6047), insaneaa.std.Trim(5972, 6047), mask_clip8, planes=[0], first_plane=True)
mask_clip9 = core.raws.Source(r'mask2.yuv').std.Trim(298, 381).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final9 = core.std.MaskedMerge(insaneaa6.std.Trim(6109, 6192), insaneaa.std.Trim(6109, 6192), mask_clip9, planes=[0], first_plane=True)
mask_clip10 = core.raws.Source(r'mask2.yuv').std.Trim(418, 598).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final10 = core.std.MaskedMerge(insaneaa6.std.Trim(10211, 10391), insaneaa.std.Trim(10211, 10391), mask_clip10, planes=[0], first_plane=True)

mrgc = insaneaa.std.Trim(0, 736)+mask_final+insaneaa.std.Trim(858, 905)+insaneaa2.std.Trim(906, 1012)+insaneaa.std.Trim(1013, 1168)+insaneaa4.std.Trim(1169, 1294)+insaneaa.std.Trim(1295, 1651)+mask_final2+insaneaa4.std.Trim(1816, 1915)+insaneaa.std.Trim(1916, 2148)+mask_final3+insaneaa.std.Trim(2413, 3380)+op+insaneaa.std.Trim(5539, 5971)+mask_final8+insaneaa.std.Trim(6048, 6108)+mask_final9+insaneaa.std.Trim(6193, 6670)+insaneaa6.std.Trim(6671, 6740)+insaneaa.std.Trim(6741, 7463)+mask_final4+insaneaa.std.Trim(7552, 8142)+mask_final5+insaneaa.std.Trim(8342, 8995)+insaneaa4.std.Trim(8996, 9042)+mask_final6+insaneaa.std.Trim(9169, 9456)+insaneaa4.std.Trim(9457, 9656)+insaneaa.std.Trim(9657, 10210)+mask_final10+insaneaa.std.Trim(10392, 11554)+stab3.std.Trim(11555, 11614)+insaneaa.std.Trim(11615, 15335)+stab0.std.Trim(15336, 15530)+insaneaa.std.Trim(15531, 17921)+insaneaa2.std.Trim(17922, 17945)+insaneaa.std.Trim(17946, 25238)+stab7.std.Trim(25239, 25431)+insaneaa.std.Trim(25432, 25592)+stab3.std.Trim(25593, 25762)+insaneaa.std.Trim(25763, 26083)+insaneaa2.std.Trim(26084, 26222)+insaneaa.std.Trim(26223, 27302)+insaneaa2.std.Trim(27303, 27374)+insaneaa.std.Trim(27375, 29019)+insaneaa2.std.Trim(29020, 29115)+insaneaa.std.Trim(29116, 29455)+insaneaa2.std.Trim(29456, 29635)+insaneaa.std.Trim(29636, 29731)+ed+stab3.std.Trim(31889, 31984)+insaneaa7.std.Trim(31985, 32068)+insaneaa.std.Trim(32069, 32442)+insaneaa7.std.Trim(32443, 32631)+insaneaa.std.Trim(32632, 32754)+insaneaa2.std.Trim(32755, 32916)+insaneaa.std.Trim(32917, 33118)+insaneaa7.std.Trim(33119, 33190)+insaneaa.std.Trim(33191, 33367)+insaneaa7.std.Trim(33368, 33484)+insaneaa.std.Trim(33485, 33854)+episode.std.Trim(33855, 33950)+insaneaa.std.Trim(33951, 34598)+episode.std.Trim(34599, 34695)
 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\05.png'), "[906 1012]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\06.png'), "[1169 1294]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\06.png'), "[1816 1915]") 
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\07.png'), "[6671 6740]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\10.png'), "[8996 9042]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\08.png'), "[9457 9656]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\12.png'), "[17922 17945]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\15.png'), "[26084 26222]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\16.png'), "[27303 27374]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\17.png'), "[29020 29115]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\17.png'), "[29456 29635]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\18.png'), "[32755 32916]")
 
insaneaa22 = oreigaru3_aa2(mrgc)

mrgc2_5 = mrgc.std.Trim(0, 10210)+insaneaa22.std.Trim(10211, 10391)+mrgc.std.Trim(10392, 34695)

mrgc2_5 = fvf.rfs(mrgc2_5, atf.ApplyImageMask(mrgc2_5, mrgc, r'.\mask\11.png'), "[10211 10391]")

insaneaa5 = oreigaru3_aa2_6(mrgc2_5)

mask_clip7 = core.raws.Source(r'mask2.yuv').std.Trim(27, 133).resize.Point(format=GRAY8).std.Expr('x 16 < 0 x ?').std.Expr('x 16 < 0 x ?').std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.Minimum()
mask_final7 = core.std.MaskedMerge(insaneaa5.std.Trim(906, 1012), mrgc2_5.std.Trim(906, 1012), mask_clip7, planes=[0], first_plane=True)

insaneaa222 = oreigaru3_aa2_6(mrgc2_5)

mrgc2 = mrgc2_5.std.Trim(0, 905)+mask_final7+mrgc2_5.std.Trim(1013, 10210)+insaneaa222.std.Trim(10211, 10391)+mrgc2_5.std.Trim(10392, 17921)+insaneaa222.std.Trim(17922, 17945)+mrgc2_5.std.Trim(17946, 31984)+insaneaa222.std.Trim(31985, 32068)+mrgc2_5.std.Trim(32069, 32754)+insaneaa222.std.Trim(32755, 32916)+mrgc2_5.std.Trim(32917, 34695)
 
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc2_5, r'.\mask\12.png'), "[10211 10391]")
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc2_5, r'.\mask\13.png'), "[17922 17945]")
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc2_5, r'.\mask\20.png'), "[32755 32916]")
mrgc2 = fvf.rfs(mrgc2, atf.ApplyImageMask(mrgc2, mrgc2_5, r'.\mask\21.png'), "[31985 32068]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

stab4 = havsfunc.QTGMC(mrgc2, InputType=1, SourceMatch=1)
stab5 = havsfunc.QTGMC(stab4, InputType=1, SourceMatch=2)
stab6 = havsfunc.QTGMC(stab5, InputType=1, SourceMatch=3)

mrgc3 = mrgc2.std.Trim(0, 2029)+stab6.std.Trim(2030, 2412)+mrgc2.std.Trim(2413, 7463)+stab6.std.Trim(7464, 7551)+mrgc2.std.Trim(7552, 34695)

clip16 = core.fmtc.bitdepth(mrgc3, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=18, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=20, cb=10, cr=10, grainy=28, grainc=28, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
Mask2 = core.std.Binarize(Mask,9828,0)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode3.set_output()
