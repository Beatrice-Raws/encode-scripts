from vapoursynth import core, GRAY
import kagefunc as kf
import cooldegrain as cd
import insaneAA as Insane
import descale

core.max_cache_size = 24000
def custom_deupscaler(clip, descale_steps=[720], kernel="bicubic", strength=0.5, b=1/3, c=1/3):
    def make_step(clip, w, h, descale_h, b, c):
        descale_w = (w * descale_h) // h
        return descale.Descale(clip, descale_w, descale_h, kernel=kernel, b=b, c=c)
    gray = core.std.ShufflePlanes(clip, 0, GRAY)
    w = gray.width
    h = gray.height
    deup = False
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

def RescaleMask(clip, descale_steps=[814, 720], kernel="bicubic"):
    grayclip = clip.std.ShufflePlanes(0, GRAY)
    reupscaled = custom_deupscaler(grayclip, descale_steps=descale_steps, kernel=kernel, strength=0.32, b=0, c=0.75).resize.Bicubic(1920, 1080, filter_param_a=0, filter_param_b=0.75)
    return core.std.MakeDiff(grayclip, reupscaled).std.Expr('x 134 < 0 x ?').rgvs.RemoveGrain(1).std.Maximum().std.Expr('x 1.35 *').std.Maximum().std.Inflate()

V, P = 2, 4

episode  = core.dgdecodenv.DGSource(r'.\..\index\BDMENUV{}P{}.dgi'.format(V, P))
hfmask   = RescaleMask(episode)
insaneaa = MainAA(episode)
mrgc = core.std.MaskedMerge(insaneaa, episode, hfmask)
clipsrc = core.fmtc.bitdepth(mrgc, bits=16)
mask = kf.retinex_edgemask(clipsrc.std.ShufflePlanes(0, GRAY), sigma=1).std.Expr('x 2 *')
clip2 = cd.CoolDegrain(clipsrc, bits=16, thsad=48, thsadc=96, blksize=8, overlap=4)
clip2 = core.f3kdb.Deband(clip2, range=8, y=36, cb=28, cr=28, grainy=32, grainc=12, output_depth=16, keep_tv_range=True)
clip = core.std.MaskedMerge(clip2, clipsrc, mask, [0,1,2], first_plane=True)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()