ClearAutoloadDirs()
prefix="C:\0\_Video_\AviSynthPlus\"
AddAutoloadDir(prefix+"plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("00003.dgi")
luma = Histogram(episode, "luma")
insaneaa =        episode          .InsAA(720)
hiaa =               insaneaa        .HiAA(aa="eedi3", mthr=20)
insane900 =         episode       .InsAA(900)

insaneaa.trim(0,33090)+episode.trim(33091,35243)

#scenes
rfs_once(hiaa, 13112, 13201)
rfs_once(episode, 13973, 14068)
rfs_once(episode, 14213, 14308)
rfs_once(episode, 14429, 14524)
rfs_once(episode, 14645, 14740)
rfs_once(episode, 14837, 14932)
rfs_once(episode, 15053, 15148)
rfs_once(episode, 15365, 15460)
rfs_once(episode, 15557, 15652)
rfs_once(episode, 16001, 16096)
rfs_once(episode, 16199, 16294)
rfs_once(episode, 16373, 16468)
rfs_once(insane900, 16604, 16663) #title
rfs_once(hiaa, 18598, 18716)

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
rfs_once(external_aa_mask_tlrd(last,episode,".\01\ed.png"), 33091, 35243)
    
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
Assert(episode.framecount() == last.framecount(), "(╯°□°）╯︵ ┻━┻")
last

[*                                                                 functions                                                                 *]

function filterblock(clip c) {
    c
    src=last
    src16=src.ConvertBits(16)
    #                                                             48, 52
    filtered=src.CoolDegrain1(48,52).gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=2.2,u=2,v=2,tv_range=true).ConvertFromStacked()
    #vPF = src.dfttest(sigma=0.6,tbsize=1,lsb=true).ConvertFromStacked()
    #filtered=src.CoolDegrain1(48,52,pf=vPF).gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=2.2,u=2,v=2,tv_range=true).ConvertFromStacked()
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

function InsAA(clip c, int h) {
    c
    aa=ExtractY().InsaneAA(dscale=h,mask=0, desc_str=0.28)
    #aa=ExtractY().InsaneAA(dscale=720,hiaa=true,hiaa_aa="eedi3", hiaa_thr=50, hiaa_uim=true, hiaa_str=0.5, mt=false)
    InsaneAA(aa_clip=aa)
}
function hiaa_with_resize(clip c) {
    c
    DeBicubicResizeMT(848,480)
    HiAA(aa="eedi3", mthr=20)
    nnedi3_resize16(target_height=1080,target_width=1920,kernel_u = "Spline36")
    DeBilinearResizeMT(1920,1080)
    HiAA(aa="eedi3", mthr=20)
}
