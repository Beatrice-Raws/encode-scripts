from vapoursynth import core, VideoNode, GRAY
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc as hf
import mvsfunc as mvf
import gradfun_amod as gfa
import insaneAA
import HardAAp2 as HardAA
import cooldegrain as cd

core.max_cache_size = 25000

maskforQTGMC = core.lsmas.LWLibavSource(r'maskforQTGMC.mp4')
maskforQTGMCfps = core.std.AssumeFPS(maskforQTGMC, fpsnum=3043, fpsden=125)
maskforQTGMCfps.set_output()