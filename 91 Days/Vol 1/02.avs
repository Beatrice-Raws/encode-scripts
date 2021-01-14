ClearAutoloadDirs()
prefix="C:\0\_Video_\AviSynthPlus\"
AddAutoloadDir(prefix+"plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("00004.dgi")
luma = Histogram(episode, "luma")
insaneaa =        episode          .InsAA()

ncop = DGSource("../../../NCOP.dgi").trim(49,2206)
ncop_aa = RawSource("../../../NCOP.yuv").trim(49,2206)
op_titles = episode.trim(5012,7167)
op = merge_credits64(op_titles, ncop, ncop_aa)
Assert(op_titles.framecount() == op.framecount(), "OP DROP")
nced = DGSource("../../../NCED.dgi").trim(60,2203)
nced_aa = RawSource("../../../NCED.yuv").trim(60,2203)
ed_titles = episode.trim(31804,33947)
ed = merge_credits64(ed_titles, nced, nced_aa)
Assert(ed_titles.framecount() == ed.framecount(), "ED DROP")

insaneaa.trim(0,5011)+op+insaneaa.trim(7168,31803)+ed+insaneaa.trim(33948,35196)

#scenes
#rfs_once(hiaa, 30000, 31427)

#                                    */

#mask creation
                    /*   
src1=episode
resc=src1.spline36resize(970,540).Spline64Resize(1920, 1080)
#resc=src1.spline36resize(1280,720).Spline64Resize(1920, 1080)
#resc=src1.spline36resize(1440,810).Spline64Resize(1920, 1080)
mt_makediff(src1,resc,3,3,3).mt_edge("roberts",5,5,5,5).removegrain(5)
#                                    */

#masks

#rfs_once(external_aa_mask_tlrd(episode,last,".\masks30\mask_00028_PV_TITLE.png"), 35082, 35172)
    
#filters
        
filterblock()
#ConvertBits(8,true,0)
ConvertTo16Bit(10,true)
Prefetch(8)

#selectTotal1=framecount()/100
#selectTotal2=selectTotal1*2
#selectrangeevery(selectTotal2,50)
#mt_makediff(episode.trim(3669,5925), RawSource("NCOP.yuv"), 3,3,3)
#external_aa_mask(episode.trim(3669,5925),RawSource("NCOP.yuv"),".\mask_check.png")

#Histogram("luma")
#AssumeFPS(last, 60000,1001)
Assert(episode.framecount() == last.framecount(), "LENGTH DROP")
last

[*                                                                 functions                                                                 *]

function filterblock(clip c) {
    c
    src=last
    src16=src.ConvertBits(16)
    #                                                             48, 52
    filtered=src.CoolDegrain1(48,52).gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=2.2,u=2,v=2,tv_range=true).ConvertFromStacked()
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

function InsAA(clip c) {
    c
    aa=ExtractY().InsaneAA(dscale=720,mask=0, desc_str=0.28)
    #aa=ExtractY().InsaneAA(dscale=720,hiaa=true,hiaa_aa="eedi3", hiaa_thr=50, hiaa_uim=true, hiaa_str=0.5, mt=false)
    InsaneAA(aa_clip=aa)
}