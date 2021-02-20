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



core.set_max_cache_size(120000)
episode = core.dgdecodenv.DGSource(r'01.dgi')


mrgc = episode.std.Trim(1799, 2132)

mrgc.set_output()





