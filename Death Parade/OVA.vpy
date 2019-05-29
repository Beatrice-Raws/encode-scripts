from vapoursynth import core, GRAY
import kagefunc as kf
import atomchtools as atf
import mvsfunc as mvf
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
    deup = False # инициализируем
    for descale_h in descale_steps:
        if not deup:
        	deup = gray
        deup = make_step(deup, w, h, descale_h, b, c)
    smooth = core.resize.Bicubic(gray, ((w * descale_steps[-1]) // h), descale_steps[-1], filter_param_a=b, filter_param_b=c)
    deup = core.std.Expr([deup, smooth], 'x {str} * y 1 {str} - * +'.format(str=strength))
    return deup
    
def localmask(source, replacement, immask, LumaOnly=True):
    filemask = core.imwrif.Read(immask).resize.Point(format=source.format.id, matrix_s="709", chromaloc_s="top_left")
    NumPlanes = source.format.num_planes
    if LumaOnly is True or NumPlanes == 1:
        planes = [0]
        filemask = mvf.GetPlane(filemask, 0)
        source_ = mvf.GetPlane(source, 0)
        replacement_ = mvf.GetPlane(replacement, 0)
    else:
        planes = [0,1,2]
        source_ = source
        replacement_ = replacement
    mask = filemask.std.Binarize(48).std.Maximum().std.Deflate()
    #replacement_ = core.std.Merge(replacement_, mask, 0.5)
    masked = core.std.MaskedMerge(source_, replacement_, mask, planes)
    if LumaOnly is True and NumPlanes > 1:
        masked = core.std.ShufflePlanes([masked, mvf.GetPlane(source, 1), mvf.GetPlane(source, 2)], planes=[0, 0, 0], colorfamily=source.format.color_family)
    return masked

def MainAA(clip, descale_steps=[814, 720], kernel="bicubic"):
    w = clip.width
    h = clip.height
    descaled = custom_deupscaler(clip, descale_steps=descale_steps, kernel=kernel, strength=0.32, b=0, c=0.75)
    reupscale = Insane.rescale(descaled, fasterAA=False, alpha=0.115, beta=0.325, eedi3Mode=dict(first=dict(mode='cpu', device=0), second=dict(mode='cpu', device=0)), nnedi3Mode=dict(first=dict(mode='opencl', device=0), second=dict(mode='opencl', device=0)), dx=w, dy=h)
    return Insane.insaneAA(clip, ref=reupscale, inputMode=1, outputMode=0)

episode = core.dgdecodenv.DGSource(r'.\..\index\OVA.dgi')

insaneaa = MainAA(episode)
maps = [
    [   385,   472, [r'.\masks\OVA.01.png']],
    [   525,   611, [r'.\masks\OVA.02.png']],
    [   656,   744, [r'.\masks\OVA.03.png']],
    [   787,   879, [r'.\masks\OVA.04.png']],
    [   981,  1073, [r'.\masks\OVA.05.png']],
    [  1096,  1184, [r'.\masks\OVA.06.png']],
    [  1210,  1303, [r'.\masks\OVA.07.png']],
    [  1354,  1448, [r'.\masks\OVA.08.png']],
    [ 34087, 34180, [r'.\masks\OVA.09.png']],
    [ 34231, 34328, [r'.\masks\OVA.10.png']],
    [ 34378, 34471, [r'.\masks\OVA.11.png']],
    [ 34583, 34676, [r'.\masks\OVA.12.png']],
    [ 34707, 34832, [r'.\masks\OVA.13.png']],
    [ 34908, 35001, [r'.\masks\OVA.14.png']],
    [ 35052, 35145, [r'.\masks\OVA.15.png']],
    [ 35197, 35289, [r'.\masks\OVA.16.png']],
    [ 35507, 35601, [r'.\masks\OVA.17.png']],
    [ 35689, 35784, [r'.\masks\OVA.18.png']],
    [ 35822, 35915, [r'.\masks\OVA.19.png']],
    [ 36111, 36203, [r'.\masks\OVA.20.png']],
]

mrgc = atf.RfsMany(insaneaa, episode, maps, localmask).std.Trim(360, episode.num_frames-1)
clipsrc = core.fmtc.bitdepth(mrgc, bits=16)
mask = kf.retinex_edgemask(clipsrc.std.ShufflePlanes(0, GRAY), sigma=1).std.Expr('x 2 *')
clip2 = cd.CoolDegrain(clipsrc, bits=16, thsad=48, thsadc=96, blksize=8, overlap=4)
clip2 = core.f3kdb.Deband(clip2, range=8, y=36, cb=28, cr=28, grainy=32, grainc=12, output_depth=16, keep_tv_range=True)
clip = core.std.MaskedMerge(clip2, clipsrc, mask, [0,1,2], first_plane=True)
clip = core.fmtc.bitdepth(clip, bits=10)
clip.set_output()