from vapoursynth import core, VideoNode, GRAY, YUV, RGB48, YUV444P16
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

core.max_cache_size = 120000
Raw = core.imwrif.Read(filename=r"H:\vdm\sollevante_lp_vdm_16b_p3d65_pq_20200218_3840x2160\3840x2160\%07d.tif", firstnum=0)
Fps_Raw = core.std.AssumeFPS(Raw, None, 24, 1)
RGB_to_YUV=core.resize.Bicubic(Fps_Raw, format=RGB48, transfer_in_s="st2084", transfer_s="st2084", primaries_in=12)
RGB_to_YUV=core.resize.Bicubic(RGB_to_YUV, format=YUV444P16, filter_param_a=0.33, filter_param_b=0.33, matrix_s="2020ncl", range=0)
RGB_to_YUV = core.fmtc.resample(RGB_to_YUV, css="420")
RGB_to_YUV = core.fmtc.bitdepth(RGB_to_YUV, bits=10)
RGB_to_YUV.set_output()












