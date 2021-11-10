prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)

episode = DGSource("05.dgi")
ncop = DGSource("NCOP.dgi").trim(0,2159)
ncop_aa = RawSource("NCOP.yuv").trim(0,2159)
op_titles = episode.trim(1356,3453)
op = merge_credits64(op_titles, ncop, ncop_aa)
insaneaa = episode.hardaa()


insaneaa.trim(0,1355)+op+insaneaa.trim(3454,12826)+episode.trim(12827,0)

rfs_once(external_aa_mask_tlrd(episode,last,".\mask\05.png"), 3517, 3632)

rfs_once(mt_merge(last, episode, titles_mask, true), 12107, 12826)
#mt_makediff(op_titles, ncop, 3,3,3)#.Histogram("luma")


filterblock2()
ConvertTo16Bit(10,true)
Prefetch(24)

function filterblock2(clip c) {
   c
    src=last
    src16=src.ConvertBits(16)
    filtered=src.ConvertTo16Bit().ConvertToStacked().gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=1.8,u=2,v=2,tv_range=true).ConvertFromStacked()
    mask=src.mixed_linemask_deband_16bit()
    mt_merge(filtered,src16,mask)
 }

function mixed_linemask_deband_16bit(clip c) {
    c.ConvertBits(16)
    thr_y=7
    thr_uv=8
    mask=mt_edge("prewitt",thr_y,thr_y,thr_uv,thr_uv,u=3,v=3,paramscale="i8")
    mask_y=mask.ExtractY()
    mask_u=mask.ExtractU()
    mask_v=mask.ExtractV()
    mt_logic(mask_y.mt_expand().mt_deflate(), mt_logic(mask_u.removegrain(2), mask_v.removegrain(2), "or").BicubicResize(mask_y.Width(), mask_y.Height()), "or")
    uv=last.BicubicResize(mask_u.Width(), mask_u.Height())
    YtoUV(uv,uv,last).mt_binarize()
}

function hardaa(clip c) {
    c
u=Extractu().what_are_you()
v=Extractv().what_are_you()
y=ExtractY().what_are_you2()
CombinePlanes(y, u, v, planes="YUV", source_planes="YYY", pixel_type="YUV420P8")
}

function what_are_you(clip c) {
c
debic = DeBicubicResizeMT(target_width=360/9*16, target_height=360, b=0.33, c=0.33, threads=1)
spline = Spline16Resize(360/9*16, 360)
Expr(debic, spline, "x 40 * y 60 * + 100 /")
eedi3Scale(up_height=540, arx=16, ary=9, mt=false)
}

function what_are_you2(clip c) {
c
h = HiAA(aa="eedi3", mthr=20, threads=1)
i = InsaneAA(dscale=720,mask=0, desc_str=0.28,mt=false)
Expr(h, i, "x 50 * y 50 * + 100 /")
}

function titles_mask(clip c) {
c
rescaled = Spline36Resize(1280,720).Spline64Resize(1920,1080)
diff = mt_makediff(last, rescaled, 3,3,3)
diff.mt_lut("x 110 < 0 255 ?").mt_edge("prewitt",16,16,u=0,v=0).removegrain(2).removegrain(2).removegrain(2).mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_inpand(60).mt_inflate()
}

