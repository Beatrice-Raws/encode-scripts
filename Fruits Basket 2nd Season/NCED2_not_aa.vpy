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

core.max_cache_size = 120000
episode = core.dgdecodenv.DGSource(r'NCED2.dgi')
episode2 = core.dgdecodenv.DGSource(r'14.dgi').std.Trim(33960, 34046)
mrgc = episode.std.Trim(0, 158)+episode.std.Trim(189, 2005)+episode2+episode.std.Trim(2063, 2207)
mrgc.set_output()







