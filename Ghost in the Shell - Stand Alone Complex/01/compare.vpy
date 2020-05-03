from vapoursynth import core, VideoNode, GRAY
import vapoursynth as vs
import atomchtools as atf
import fvsfunc as fvf
import kagefunc as kg
import havsfunc as hf
import mvsfunc as mvf
import gradfun_amod as gfa
import insaneAA
import HardAAp2 as HardAA
import cooldegrain as cd

core.max_cache_size = 5000
    

episode = core.lsmas.LWLibavSource(r'01-1.avi')

rip1 = core.lsmas.LWLibavSource(r'01.hevc')
rip1 = core.resize.Spline36(rip1, 1920, 1036)
rip1.set_output(1)

crop = core.std.CropRel(episode, left=0, top=22, right=0, bottom=22)

ds = core.fmtc.resample(crop, 1280, 690, kernel='blackmanminlobe', taps=8)

filt = core.resize.Spline36(ds, 1920, 1036)

filt.set_output(0)