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
def fate_zero_aa(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=855, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    return mixyuv 

def fate_zero_aa2(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=855, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=30, useCL=True)
    return mixyuv  

def fate_zero_aa3(clip):
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=855, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(clip, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, clip, clip], [0,1,2], clip.format.color_family)
    mixyuv = hiaa.HardAA(mixyuv, mask='simple', mthr=60, useCL=True)
    return mixyuv
 
core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'11.dgi')
op_titles = core.std.Trim(episode, 648, 2807)
ncop = core.dgdecodenv.DGSource(r'NCOP.dgi').std.Trim(24, 2183)
ncop_aa = core.raws.Source(r'NCOP.y4m').std.Trim(24, 2183)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)
ed_titles = core.std.Trim(episode, 33737, 35893)
nced = core.dgdecodenv.DGSource(r'NCED.dgi').std.Trim(25,2181)
nced_aa = core.raws.Source(r'NCED.y4m').std.Trim(25,2181)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)
insaneaa = fate_zero_aa(episode)
insaneaa2 = fate_zero_aa2(episode)
insaneaa3 = fate_zero_aa3(episode)
insaneaa4 = havsfunc.QTGMC(episode, InputType=1, SourceMatch=3)
insaneaa4 = fate_zero_aa(insaneaa4)
stab = havsfunc.QTGMC(insaneaa, InputType=1, SourceMatch=3)
stab2 = havsfunc.QTGMC(insaneaa2, InputType=1, SourceMatch=3)
stab3 = havsfunc.QTGMC(insaneaa3, InputType=1, SourceMatch=3)
stab4 = havsfunc.QTGMC(insaneaa4, InputType=1, SourceMatch=3)

mrgc = insaneaa.std.Trim(0, 647)+op+insaneaa.std.Trim(2808, 3692)+insaneaa2.std.Trim(3693, 3726)+insaneaa.std.Trim(3727, 4360)+insaneaa2.std.Trim(4361, 4450)+insaneaa.std.Trim(4451, 5294)+stab2.std.Trim(5295, 5360)+insaneaa.std.Trim(5361, 5533)+insaneaa2.std.Trim(5534, 5560)+insaneaa.std.Trim(5561, 6809)+insaneaa2.std.Trim(6810, 6932)+insaneaa.std.Trim(6933, 7281)+insaneaa2.std.Trim(7282, 7317)+insaneaa.std.Trim(7318, 7429)+insaneaa2.std.Trim(7430, 7463)+insaneaa.std.Trim(7464, 8406)+stab2.std.Trim(8407, 8448)+stab4.std.Trim(8449, 8673)+insaneaa.std.Trim(8674, 10835)+stab2.std.Trim(10836, 10875)+stab.std.Trim(10876, 11267)+insaneaa.std.Trim(11268, 32066)+stab.std.Trim(32067, 32155)+insaneaa.std.Trim(32156, 32478)+stab3.std.Trim(32479, 32568)+insaneaa.std.Trim(32569, 33334)+insaneaa3.std.Trim(33335, 33453)+insaneaa.std.Trim(33454, 33663)+episode.std.Trim(33664, 33736)+ed+insaneaa.std.Trim(35894, 36193)+episode.std.Trim(36194, 36277)

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, insaneaa, r'.\mask\32.png'), "[4361 4450]")

#core.std.MakeDiff(op_titles, ncop, [0,1,2]).set_output()
#core.std.MakeDiff(ed_titles, nced, [0,1,2]).set_output()

clip16 = core.fmtc.bitdepth(mrgc, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=24, thsadc=26, bits=16, blksize=8, overlap=4, pf=pf)
db = core.f3kdb.Deband(den, range=31, y=16, cb=10, cr=10, grainy=22, grainc=22, output_depth=16, keep_tv_range=True)
db2 = core.f3kdb.Deband(den, range=31, y=34, cb=14, cr=14, grainy=42, grainc=42, output_depth=16, keep_tv_range=True)
db3 = core.f3kdb.Deband(den, range=31, y=54, cb=14, cr=14, grainy=42, grainc=42, output_depth=16, keep_tv_range=True)
Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=True)
filtered2 = core.std.MaskedMerge(db, clip16, Mask, planes=[0,1,2], first_plane=True)
filtered3 = core.std.MaskedMerge(db2, clip16, Mask, planes=[0,1,2], first_plane=True)
filtered4 = core.std.MaskedMerge(db3, clip16, Mask, planes=[0,1,2], first_plane=True)
episode3 = core.fmtc.bitdepth(filtered2, bits=10)
episode4 = core.fmtc.bitdepth(filtered3, bits=10)
episode5 = core.fmtc.bitdepth(filtered4, bits=10)
mrgc2 = episode3.std.Trim(0, 4947)+episode5.std.Trim(4948, 5019)+episode3.std.Trim(5020, 36277)
mrgc2.set_output()








