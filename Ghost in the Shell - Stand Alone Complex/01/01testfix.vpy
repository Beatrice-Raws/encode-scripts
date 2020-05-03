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

episode = core.lsmas.LWLibavSource(r'01-1.avi')
maskforQTGMC = core.raws.Source(r'01losslessforfix.y4m')

qtgmcclip = hf.QTGMC(episode, Preset='Placebo', NoisePreset="Slower", ThSAD1=400, ThSAD2=200, EZDenoise=0, InputType=1, opencl=True)
qtgmclines = core.std.MaskedMerge(episode, qtgmcclip, maskforQTGMC)

mrgc = episode.std.Trim(0, 889) + qtgmclines.std.Trim(890, 976) + episode.std.Trim(977, episode.num_frames-1)
mrgc.set_output()