from vapoursynth import core, GRAY
import kagefunc as kf
import atomchtools as atf
import cooldegrain as cd
import insaneAA as Insane
import HardAAp2 as HardAA
import descale

core.max_cache_size = 24000
def custom_deupscaler(clip, descale_steps=[720], kernel="bicubic", strength=0.5, b=1/3, c=1/3):
    def make_step(clip, w, h, descale_h, b, c):
        descale_w = (w * descale_h) // h
        return descale.Descale(clip, descale_w, descale_h, kernel=kernel, b=b, c=c)
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    w = gray.width
    h = gray.height
    deup = False # инициализируем
    for descale_h in descale_steps:
        if not deup:
        	deup = gray
        deup = make_step(deup, w, h, descale_h, b, c)
    smooth = core.resize.Bicubic(gray, ((w * descale_steps[-1]) // h), descale_steps[-1], filter_param_a=b, filter_param_b=c)
    deup = core.std.Expr([deup, smooth], 'x {str} * y 1 {str} - * +'.format(str=strength))
    return deup

def MainAA(clip, descale_steps=[814, 720], kernel="bicubic"):
    w = clip.width
    h = clip.height
    descaled = custom_deupscaler(clip, descale_steps=descale_steps, kernel=kernel, strength=0.32, b=0, c=0.75)
    reupscale = Insane.rescale(descaled, fasterAA=False, alpha=0.115, beta=0.325, eedi3Mode=dict(first=dict(mode='cpu', device=0), second=dict(mode='cpu', device=0)), nnedi3Mode=dict(first=dict(mode='opencl', device=0), second=dict(mode='opencl', device=0)), dx=w, dy=h)
    return Insane.insaneAA(clip, ref=reupscale, inputMode=1, outputMode=0)

epnum = 12
episode = core.dgdecodenv.DGSource(r'.\..\index\EP{:02d}.dgi'.format(epnum))
insaneaa = MainAA(episode)
mrgc = insaneaa
hard1 = HardAA.HardAA(mrgc, mthr=48, useCL=False)
hard2 = HardAA.HardAA(mrgc, mthr=60, useCL=False)
mrgc = core.rfmod.Replace(mrgc, [hard1, hard2, episode], ['[10525:10668]', '[32580:32657]', '[31178:32579]'])
clipsrc = core.fmtc.bitdepth(mrgc, bits=16)
mask = kf.retinex_edgemask(clipsrc.std.ShufflePlanes(0, GRAY), sigma=1).std.Expr('x 2 *')
clip2 = cd.CoolDegrain(clipsrc, bits=16, thsad=48, thsadc=96, blksize=8, overlap=4)
clip2 = core.f3kdb.Deband(clip2, range=8, y=36, cb=28, cr=28, grainy=32, grainc=12, output_depth=16, keep_tv_range=True)
clip = core.std.MaskedMerge(clip2, clipsrc, mask, [0,1,2], first_plane=True)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()