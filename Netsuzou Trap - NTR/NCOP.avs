prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)
DGSourceIM("NCOP.dgi")
hardaa()


filterblock2()
ConvertTo16Bit(10,true)
Prefetch(24)
function filterblock2(clip c) {
  c
  src=last
  src16=src.ConvertBits(16)
  vPF = src.dfttest(sigma=0.6,tbsize=1,lsb=true).ConvertFromStacked()
  filtered=src.CoolDegrain1(46,46,pf=vPF).gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=2,u=2,v=2,tv_range=true).ConvertFromStacked()
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
y=ExtractY().InsaneAA(dscale=720,mask=0, desc_str=0.28,mt=false)
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
debic2 = HiAA(aa="eedi3", mthr=20, threads=1)
spline2 = InsaneAA(dscale=720,mask=0, desc_str=0.28,mt=false)
Expr(debic2, spline2, "x 50 * y 50 * + 100 /")
}
