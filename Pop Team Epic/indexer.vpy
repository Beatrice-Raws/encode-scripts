from vapoursynth import core
ep=int(epn)
clip = core.lsmas.LWLibavSource(r'.\..\m2ts\Vol{i}.m2ts'.format(i=ep))
clip.set_output()
