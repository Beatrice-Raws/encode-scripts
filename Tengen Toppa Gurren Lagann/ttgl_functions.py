from vsdenoise import MVTools, SADMode, SearchMode, MotionMode, PelType, BM3D, Prefilter, Profile, nl_means, DFTTest, deblock_qed
from vskernels import BicubicSharp, Bilinear, Catrom, Hermite, Lanczos, Spline36
from vstools import core, set_output, vs, depth, get_y, join, fallback
from vsaa import based_aa, Nnedi3, Eedi3, SangNom
from vsdeband import Placebo, AddNoise
from vsrealesrgan import realesrgan
from vodesfunc import DescaleTarget
from mvsfunc import ToRGB, ToYUV
from vsdehalo import fine_dehalo
from kagefunc import crossfade
from functools import partial, reduce
from vapoursynth import GRAY
from typing import Optional
import havsfunc as haf
import fvsfunc as fvf
import functools
import xvs

# outdated function from havsfunc
def santiag(
    c: vs.VideoNode,
    strh: int = 1,
    strv: int = 1,
    type: str = 'nnedi3',
    nsize: Optional[int] = None,
    nns: Optional[int] = None,
    qual: Optional[int] = None,
    pscrn: Optional[int] = None,
    int16_prescreener: Optional[bool] = None,
    int16_predictor: Optional[bool] = None,
    exp: Optional[int] = None,
    aa: Optional[int] = None,
    alpha: Optional[float] = None,
    beta: Optional[float] = None,
    gamma: Optional[float] = None,
    nrad: Optional[int] = None,
    mdis: Optional[int] = None,
    vcheck: Optional[int] = None,
    fw: Optional[int] = None,
    fh: Optional[int] = None,
    halfres: bool = False,
    typeh: Optional[str] = None,
    typev: Optional[str] = None,
    opencl: bool = False,
    device: Optional[int] = None,
) -> vs.VideoNode:
    '''
    santiag v1.6
    Simple antialiasing

    type = "nnedi3", "eedi3" or "sangnom"
    '''

    def santiag_dir(c: vs.VideoNode, strength: int, type: str, fw: Optional[int] = None, fh: Optional[int] = None) -> vs.VideoNode:
        fw = fallback(fw, c.width)
        fh = fallback(fh, c.height)

        c = santiag_stronger(c, strength, type)

        return c.resize.Spline36(fw, fh, src_top=0 if halfres else 0.5)

    def santiag_stronger(c: vs.VideoNode, strength: int, type: str) -> vs.VideoNode:
        if opencl:
            nnedi3 = partial(core.nnedi3cl.NNEDI3CL, nsize=nsize, nns=nns, qual=qual, pscrn=pscrn, device=device)
            eedi3 = partial(core.eedi3m.EEDI3CL, alpha=alpha, beta=beta, gamma=gamma, nrad=nrad, mdis=mdis, vcheck=vcheck, device=device)
        else:
            nnedi3 = partial(
                core.znedi3.nnedi3, nsize=nsize, nns=nns, qual=qual, pscrn=pscrn, int16_prescreener=int16_prescreener, int16_predictor=int16_predictor, exp=exp
            )
            eedi3 = partial(core.eedi3m.EEDI3, alpha=alpha, beta=beta, gamma=gamma, nrad=nrad, mdis=mdis, vcheck=vcheck)

        strength = max(strength, 0)
        field = strength % 2
        dh = strength <= 0 and not halfres

        if strength > 0:
            c = santiag_stronger(c, strength - 1, type)

        w = c.width
        h = c.height

        if type == 'nnedi3':
            return nnedi3(c, field=field, dh=dh)
        elif type == 'eedi3':
            sclip = nnedi3(c, field=field, dh=dh)
            return eedi3(c, field=field, dh=dh, sclip=sclip)
        elif type == 'sangnom':
            if dh:
                c = c.resize.Spline36(w, h * 2, src_top=-0.25)
            return c.sangnom.SangNom(order=field + 1, aa=aa)
        else:
            raise vs.Error('santiag: unexpected value for type')

    if not isinstance(c, vs.VideoNode):
        raise vs.Error('santiag: this is not a clip')

    type = type.lower()
    typeh = type if typeh is None else typeh.lower()
    typev = type if typev is None else typev.lower()

    w = c.width
    h = c.height
    fwh = fw if strv < 0 else w
    fhh = fh if strv < 0 else h

    if strh >= 0:
        c = santiag_dir(c, strh, typeh, fwh, fhh)
    if strv >= 0:
        c = santiag_dir(c.std.Transpose(), strv, typev, fh, fw).std.Transpose()

    fw = fallback(fw, w)
    fh = fallback(fh, h)
    if strh < 0 and strv < 0:
        c = c.resize.Spline36(fw, fh)
    return c

# from atomchtools
def retinex_edgemask(src: vs.VideoNode, sigma: int = 1) -> vs.VideoNode:
    '''
    Use retinex to greatly improve the accuracy of the edge detection in dark scenes.
    sigma is the sigma of tcanny
    '''
    src = core.fmtc.bitdepth(src, bits=16)
    luma = core.std.ShufflePlanes(src, 0, GRAY)
    ret = core.retinex.MSRCP(luma, sigma=[50, 200, 350], upper_thr=0.005)
    tcanny_clip = core.tcanny.TCanny(ret, mode=1, sigma=sigma)
    mask = core.std.Expr([kirsch(luma), tcanny_clip.std.Minimum(coordinates=[1, 0, 1, 0, 0, 1, 0, 1])], 'x y +')
    return mask

# from atomchtools
def kirsch(src: vs.VideoNode) -> vs.VideoNode:
    ''' Kirsch edge detection. This uses 8 directions, so it's slower but better than Sobel (4 directions) '''
    w = [5] * 3 + [-3] * 5
    weights = [w[-i:] + w[:-i] for i in range(4)]
    c = [core.std.Convolution(src, (w[:4] + [0] + w[4:]), saturate=False) for w in weights]
    return core.std.Expr(c, 'x y max z max a max')

# from atomchtools with some changes
def DiffCreditlessMask(titles: vs.VideoNode, nc: vs.VideoNode) -> vs.VideoNode:
    ''' Makes mask based on difference from 2 clips. Raises a mask from that diiference '''
    funcName = 'DiffCreditlessMask'
    if not isinstance(titles, vs.VideoNode):
        raise TypeError(f'{funcName}: "titles" must be a clip!')
    if not isinstance(nc, vs.VideoNode):
        raise TypeError(f'{funcName}: "nc" must be a clip!')
    assert titles.num_frames == nc.num_frames, TypeError(f'{funcName}: input clips are not even! titles: {titles.num_frames}, nc: {nc.num_frames}!')
    mask = core.std.MakeDiff(titles, nc, [0])
    mask = core.std.ShufflePlanes(mask, 0, GRAY)
    mask = mask.std.Prewitt().std.Invert().std.Minimum().std.Inflate()
    return mask

def rfs_img(clip: vs.VideoNode, img: vs.VideoNode, mappings) -> vs.VideoNode:
    ''' rfs from atomchtools, simplified to replace one frame with an image file '''
    if mappings is None:
        mappings = []

    maps = []
    for item in mappings:
        if isinstance(item, int):
            maps.append([item, item])

    out = clip
    for start, end in maps:
        img = img.resize.Point(format=clip.format.id, matrix_s="709").std.SetFrameProps(_Matrix=1, _Transfer=1, _Primaries=1, _ColorRange=1, _FieldBased=0).std.AssumeFPS(fpsnum=24000, fpsden=1001)
        if start != 0:
            temp = out[:start] + img
        if end < out.num_frames - 1:
            temp = temp + out[end+1:]
        out = temp
    return out    

def aa_mask(clip):
    luma = get_y(clip)
    sobel_mask = core.std.Sobel(luma)
    prewitt_mask = core.std.Prewitt(luma)
    mixed_mask = core.std.Expr([sobel_mask, prewitt_mask], 'x y max')
    shrunk = sobel_mask.std.Minimum().std.Inflate()
    edges = core.std.Expr([mixed_mask, shrunk], 'x y - 16 > x 0 ? 64 > x x 2 / ?').rgvs.RemoveGrain(1)
    clean = core.rgvs.RemoveGrain(edges, 1).rgvs.RemoveGrain(2).std.Expr('x 32 < x 3.5 * x 64 < x 2.5 * x 128 < x 1.5 * x ? ? ?')
    smooth = clean.std.Inflate().std.Deflate()
    return smooth

# dehalo wrapper
def dehalo(clip: vs.VideoNode) -> vs.VideoNode:
    fdh = fine_dehalo(clip)
    return fdh

# based_aa wrapper
def baa(clip: vs.VideoNode) -> vs.VideoNode:
    AA = based_aa(clip, supersampler=False)
    fdh = fine_dehalo(AA)
    return fdh

# santiag eedi wrapper
def eedi(clip: vs.VideoNode) -> vs.VideoNode:
    AA = santiag(clip, type='eedi3')
    fdh = fine_dehalo(AA)
    return fdh

# santiag sangnom wrapper
def sangnom(clip: vs.VideoNode) -> vs.VideoNode:
    AA = santiag(clip, type='sangnom', aa=64)
    fdh = fine_dehalo(AA)
    return fdh

# santiag sangnom x2 wrapper
def sangnom_x2(clip: vs.VideoNode) -> vs.VideoNode:
    AA = santiag(clip, type='sangnom', aa=128)
    AA = santiag(AA, type='sangnom', aa=128)
    fdh = fine_dehalo(AA)
    return fdh

def main_AA(clip: vs.VideoNode, credit_mask: bool = None) -> vs.VideoNode:
    dt = DescaleTarget(width=1280, height=720, kernel=Lanczos(3), do_post_descale=dehalo, downscaler=Hermite(linear=True), credit_mask=credit_mask).get_upscaled(clip)
    return dt

def op_ed_AA(clip: vs.VideoNode) -> vs.VideoNode:
    dt = DescaleTarget(width=1280, height=720, kernel=Bilinear, do_post_descale=dehalo, downscaler=Hermite(linear=True), credit_mask=True).get_upscaled(clip)
    return dt

def op_ed_AA_2(clip: vs.VideoNode, credit_mask: bool = None) -> vs.VideoNode:
    dt = DescaleTarget(width=1280, height=720, kernel=BicubicSharp, do_post_descale=dehalo, downscaler=Hermite(linear=True), credit_mask=credit_mask).get_upscaled(clip)
    return dt

def weakest_nnedi3_AA(clip):
    luma = get_y(clip)
    AA = santiag(luma, type='nnedi3')
    mask = core.std.MaskedMerge(luma, AA, aa_mask(clip))
    return join(mask, clip)

def weakest_nneedi3_AA(clip):
    luma = get_y(clip)
    AA = santiag(luma, type='eedi3')
    AA = santiag(AA, type='nnedi3')
    mask = core.std.MaskedMerge(luma, AA, aa_mask(clip))
    return join(mask, clip)

def weak_eedi_AA(clip: vs.VideoNode, credit_mask: bool = False) -> vs.VideoNode:
    dt_weedi = DescaleTarget(width=1280, height=720, kernel=Lanczos(3), downscaler=Hermite(linear=True), do_post_double=baa, credit_mask=credit_mask).get_upscaled(clip)
    return dt_weedi

def eedi_AA(clip: vs.VideoNode, credit_mask: bool = False) -> vs.VideoNode:
    dt_eedi = DescaleTarget(width=1280, height=720, kernel=Lanczos(3), downscaler=Hermite(linear=True), do_post_descale=eedi, credit_mask=credit_mask).get_upscaled(clip)
    return dt_eedi

def eedi_AA_YUV(clip: vs.VideoNode) -> vs.VideoNode:
    line_mask = retinex_edgemask(clip)
    descale = Lanczos(3).descale(clip, 1280, 720)
    fdh = fine_dehalo(descale)
    eedi = santiag(fdh, type='eedi3')
    rescale = Nnedi3(opencl=True).scale(eedi, 1920, 1080)
    rescaled = core.std.MaskedMerge(clip, rescale, line_mask)
    return rescaled

def strong_eedi_AA(clip: vs.VideoNode) -> vs.VideoNode:
    luma = get_y(clip)
    line_mask = retinex_edgemask(luma).std.Maximum().std.Expr('x 4 *')
    descale = Lanczos(3).descale(luma, 854, 480)
    eedi = santiag(descale, type='eedi3')
    rescale = Nnedi3(opencl=True).scale(eedi, 1920, 1080)
    rescale_dh = fine_dehalo(rescale)
    rescaled = core.std.MaskedMerge(luma, rescale_dh, line_mask)
    rescaled = join(rescaled, clip)
    return rescaled

def very_strong_eedi_AA(clip: vs.VideoNode) -> vs.VideoNode:
    luma = get_y(clip)
    line_mask = retinex_edgemask(luma).std.Maximum().std.Expr('x 4 *')
    descale = Lanczos(3).descale(luma, 460, 360)
    eedi = santiag(descale, type='eedi3')
    rescale = Nnedi3(opencl=True).scale(eedi, 1920, 1080)
    rescale_dh = fine_dehalo(rescale)
    rescaled = core.std.MaskedMerge(luma, rescale_dh, line_mask)
    rescaled = join(rescaled, clip)
    return rescaled

def weak_sangnom_AA(clip: vs.VideoNode) -> vs.VideoNode:
    dt_saa = DescaleTarget(width=1280, height=720, kernel=Lanczos(3), downscaler=Hermite(linear=True), do_post_double=sangnom, credit_mask=False).get_upscaled(clip)
    return dt_saa

def sangnom_AA(clip: vs.VideoNode) -> vs.VideoNode:
    dt_saa = DescaleTarget(width=1280, height=720, kernel=Lanczos(3), downscaler=Hermite(linear=True), do_post_double=sangnom_x2, credit_mask=False).get_upscaled(clip)
    return dt_saa

def sangnom_AA_YUV(clip: vs.VideoNode) -> vs.VideoNode:
    line_mask = retinex_edgemask(clip)
    descale = Lanczos(3).descale(clip, 1280, 720)
    fdh = fine_dehalo(descale)
    sangnom = sangnom_x2(fdh)
    rescale = Nnedi3(opencl=True).scale(sangnom, 1920, 1080)
    rescaled = core.std.MaskedMerge(clip, rescale, line_mask)
    return rescaled

def strong_AA(clip: vs.VideoNode) -> vs.VideoNode:
    luma = get_y(clip)
    line_mask = retinex_edgemask(luma).std.Maximum().std.Expr("x 2 *")
    descale = Lanczos(3).descale(luma, 1280, 720)
    fdh = fine_dehalo(descale)
    sangnom = santiag(fdh, type='sangnom', aa=128)
    sangnom = santiag(sangnom, type='sangnom', aa=128)
    rescale = Nnedi3(opencl=True).scale(sangnom, 1920, 1080)
    rescale_dh = fine_dehalo(rescale)
    rescaled = core.std.MaskedMerge(luma, rescale_dh, line_mask)
    rescaled = join(rescaled, clip)
    return rescaled

def strong_AA_YUV(clip: vs.VideoNode) -> vs.VideoNode:
    line_mask = retinex_edgemask(clip).std.Maximum().std.Expr("x 2 *")
    descale = Lanczos(3).descale(clip, 1280, 720)
    fdh = fine_dehalo(descale)
    sangnom = santiag(fdh, type='sangnom', aa=128)
    sangnom = santiag(sangnom, type='sangnom', aa=128)
    rescale = Nnedi3(opencl=True).scale(sangnom, 1920, 1080)
    rescaled = core.std.MaskedMerge(clip, rescale, line_mask)
    return rescaled

def very_strong_AA(clip: vs.VideoNode) -> vs.VideoNode:
    luma = get_y(clip)
    line_mask = retinex_edgemask(luma).std.Maximum().std.Expr("x 4 *")
    descale = Lanczos(3).descale(luma, 854, 480)
    sangnom = santiag(descale, type='sangnom', aa=128)
    sangnom = santiag(sangnom, type='sangnom', aa=128)
    rescale = Nnedi3(opencl=True).scale(sangnom, 1920, 1080)
    rescale_dh = fine_dehalo(rescale)
    rescaled = core.std.MaskedMerge(luma, rescale_dh, line_mask)
    rescaled = join(rescaled, clip)
    return rescaled

def strongest_AA(clip: vs.VideoNode) -> vs.VideoNode:
    luma = get_y(clip)
    line_mask = retinex_edgemask(luma).std.Maximum().std.Expr('x 8 *')
    descale = Lanczos(3).descale(luma, 480, 270)
    sangnom = santiag(descale, type='sangnom', aa=128)
    sangnom = santiag(sangnom, type='sangnom', aa=128)
    rescale = Nnedi3(opencl=True).scale(sangnom, 1920, 1080)
    rescale_dh = fine_dehalo(rescale)
    rescaled = core.std.MaskedMerge(luma, rescale_dh, line_mask)
    rescaled = join(rescaled, clip)
    return rescaled

def RealESRGAN_AA(clip: vs.VideoNode) -> vs.VideoNode:
    line_mask = retinex_edgemask(clip)
    descale = BicubicSharp.descale(clip, 1280, 720)
    fdh = fine_dehalo(descale)
    realESR = ToRGB(fdh, 1, 32)
    realESR = realesrgan(realESR, model=4, auto_download=True, denoise_strength=0.0)
    realESR = ToYUV(realESR, matrix=1, css="420", depth=16)
    realESR = core.resize.Bicubic(realESR, 1920, 1080)
    fdh2 = fine_dehalo(realESR)
    rescaled = core.std.MaskedMerge(clip, fdh2, line_mask)
    return rescaled

# from atomchtools
def ApplyImageMask(source: vs.VideoNode, replacement: vs.VideoNode, image_mask: str = None, luma_only: bool = True, binarize_threshold: int = 17, scaled_binarize: bool = False, preview: bool = False, first_plane_mask: bool = True, blur: bool = False) -> vs.VideoNode:
    ''' Applies custom (hand-drawn) image as static mask for two clips '''
    funcName = 'ApplyImageMask'
    if not isinstance(source, vs.VideoNode):
        raise TypeError(f'{funcName}: "source" must be a clip!')
    if not isinstance(replacement, vs.VideoNode):
        raise TypeError(f'{funcName}: "replacement" must be a clip!')
    if not isinstance(image_mask, vs.VideoNode):
        MaskReader = core.imwrif.Read if hasattr(core, 'imwrif') else core.imwri.Read
        filemask = MaskReader(image_mask).resize.Point(format=source.format.id, matrix_s="709", chromaloc_s="top_left")
    elif isinstance(image_mask, vs.VideoNode):
        filemask = image_mask
    else:
        raise TypeError(f'{funcName}: "image_mask" has unsupported type!')
    mum_planes = source.format.num_planes
    if luma_only is True or mum_planes == 1:
        planes = [0]
        filemask = core.std.ShufflePlanes(filemask, 0, GRAY)
        source_ = core.std.ShufflePlanes(source, 0, GRAY)
        replacement_ = core.std.ShufflePlanes(replacement, 0, GRAY)
    else:
        planes = [0,1,2]
        source_ = source
        replacement_ = replacement
    assert source.num_frames == replacement.num_frames, TypeError(f'{funcName}: input clips are not even! source: {source.num_frames}, replacement: {replacement.num_frames}!')
    if not scaled_binarize:
        max_pixel_value = (256 << (source.format.bits_per_sample - 8)) - 1
        binarize_threshold = min(binarize_threshold << (source.format.bits_per_sample - 8), max_pixel_value)
    filemask = core.std.Expr(filemask, f'x {binarize_threshold} < 0 x ?').std.Maximum().std.Deflate()
    if preview:
        replacement_ = core.std.Merge(filemask, replacement_, 0.5)
    masked = core.std.MaskedMerge(source_, replacement_, filemask, planes, first_plane_mask)
    if blur:
        filemask = filemask.std.Maximum().std.Inflate()
        masked_blurry = haf.MinBlur(masked, 3)
        masked = core.std.MaskedMerge(masked, masked_blurry, filemask, planes, first_plane_mask)
    if luma_only is True and mum_planes > 1:
        masked = core.std.ShufflePlanes([masked, source], planes=[0, 1, 2], colorfamily=source.format.color_family)
    return masked

# from atomchtools
def ApplyCredits(credits: vs.VideoNode, nc: vs.VideoNode, fixed_nc: vs.VideoNode, luma_only: bool = True) -> vs.VideoNode:
    ''' Convenient helper for applying credits on processed creditless videos (OP/ED) '''
    funcName = 'ApplyCredits'
    if not isinstance(credits, vs.VideoNode):
        raise TypeError(f'{funcName}: "credits" must be a clip!')
    if not isinstance(nc, vs.VideoNode):
        raise TypeError(f'{funcName}: "nc" must be a clip!')
    if not isinstance(fixed_nc, vs.VideoNode):
        raise TypeError(f'{funcName}: "fixed_nc" must be a clip!')
    assert credits.num_frames == nc.num_frames == fixed_nc.num_frames, TypeError(f'{funcName}: input clips are not even! credits: {credits.num_frames}, nc - {nc.num_frames}, fixed_nc - {fixed_nc.num_frames}!')
    if luma_only is True:
        credits_ = core.std.ShufflePlanes(credits, 0, GRAY)
        nc = core.std.ShufflePlanes(nc, 0, GRAY)
        fixed_nc = core.std.ShufflePlanes(fixed_nc, 0, GRAY)
    else:
        credits_ = credits
    averaged = core.std.Expr([credits_, nc, fixed_nc], ['x y - z +'])
    if luma_only is True:
        averaged = core.std.ShufflePlanes([averaged, credits], planes=[0, 1, 2], colorfamily=credits.format.color_family)
    return averaged

def ApplyStab(clip, times=3):
  for _ in range(times):
    clip = haf.QTGMC(clip, InputType=1, SourceMatch=3, Sharpness=0.1, Denoiser="DFTTest")
  return clip

def denoise_deband(clip: vs.VideoNode, thSAD: int = None, thr: int = None, sigma: int = None) -> vs.VideoNode:
    luma = get_y(clip)
    line_detail_mask = xvs.mwdbmask(clip, sigma=2.5, t_h=0.9, t_l=0.5)
    line_detail_mask = get_y(line_detail_mask)

    ref = MVTools.denoise(luma, prefilter=Prefilter.DFTTEST, thSAD=thSAD, block_size=32, overlap=16, sad_mode=SADMode.ADAPTIVE_SPATIAL_MIXED, search=SearchMode.DIAMOND, motion=MotionMode.HIGH_SAD, pel_type=PelType.WIENER)
    
    denoise = BM3D.denoise(luma, ref=ref, profile=Profile.LOW_COMPLEXITY, sigma=sigma, radius=3)
    nlm = nl_means(clip, strength=0.25, tr=3, sr=2, planes=[1, 2])

    deband = Placebo.deband(denoise, thr=thr)
    
    deband = core.std.MaskedMerge(deband, ref, line_detail_mask)
    deband = join(deband, nlm)

    return deband

def denoise_deband_strong(clip: vs.VideoNode, thSAD: int = None, thr: int = None, sigma: int = None) -> vs.VideoNode:
    luma = get_y(clip)
    line_detail_mask = xvs.mwdbmask(clip, sigma=2.5, t_h=0.9, t_l=0.5)
    line_detail_mask = get_y(line_detail_mask)

    dftt = DFTTest(sloc={0.0: 4, 0.2: 9, 1.0: 15}, tr=0).denoise(luma)
    ref = MVTools.denoise(luma, prefilter=dftt, thSAD=thSAD, block_size=32, overlap=16, sad_mode=SADMode.ADAPTIVE_SPATIAL_MIXED, search=SearchMode.DIAMOND, motion=MotionMode.HIGH_SAD, pel_type=PelType.WIENER)
    
    denoise = BM3D.denoise(luma, ref=ref, profile=Profile.LOW_COMPLEXITY, sigma=sigma, radius=3)
    nlm = nl_means(clip, strength=0.25, tr=3, sr=2, planes=[1, 2])

    deband = Placebo.deband(denoise, thr=thr)
    deband = core.neo_f3kdb.Deband(deband)
    deband = core.std.MaskedMerge(deband, ref, line_detail_mask)
    deband = join(deband, nlm)

    grain = AddNoise.GAUSS((1.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(deband)

    return grain

def denoise_deband_strongest(clip: vs.VideoNode, thSAD: int = None, thr: int = None, y: int = 128, sigma: int = None) -> vs.VideoNode:
    luma = get_y(clip)

    dftt = DFTTest(sloc={0.0: 4, 0.2: 9, 1.0: 15}, tr=0).denoise(luma)
    ref = MVTools.denoise(luma, prefilter=dftt, thSAD=thSAD, block_size=32, overlap=16, sad_mode=SADMode.ADAPTIVE_SPATIAL_MIXED, search=SearchMode.DIAMOND, motion=MotionMode.HIGH_SAD, pel_type=PelType.WIENER)
    
    denoise = BM3D.denoise(luma, ref=ref, profile=Profile.LOW_COMPLEXITY, sigma=sigma, radius=3)
    nlm = nl_means(clip, strength=0.25, tr=3, sr=2, planes=[1, 2])

    deband = Placebo.deband(denoise, thr=thr)
    deband = core.neo_f3kdb.Deband(deband, y=y)
    deband = join(deband, nlm)

    grain = AddNoise.GAUSS((1.0, 0), 0.85, Catrom, True, luma_scaling=6).grain(deband)

    return grain

def denoise_deblock(clip: vs.VideoNode) -> vs.VideoNode:
    luma = get_y(clip)
    
    deblock = deblock_qed(luma)

    denoise = MVTools.denoise(deblock, prefilter=Prefilter.BM3D, thSAD=200, block_size=32, overlap=16, sad_mode=SADMode.ADAPTIVE_SPATIAL_MIXED, search=SearchMode.DIAMOND, motion=MotionMode.HIGH_SAD, pel_type=PelType.WIENER)

    deband = Placebo.deband(denoise, thr=2.0)
    return join(deband, clip)