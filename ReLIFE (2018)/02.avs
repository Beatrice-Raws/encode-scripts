prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSourceim("02.dgi")
insaneaa = episode.RELIFEAA()





insaneaa.trim(0,0)

rfs(qtgmc(InputType=1,SourceMatch=3),"[3591 3685]")

rfs_once(mt_merge(last, episode, titles_mask, true), 3470, 5274)
rfs_once(mt_merge(last, episode, titles_mask, true), 31846,33685)
rfs(external_aa_mask_tlrd(episode,last,".\mask\2\01.png"),"[5275 5340]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\2\02.png"),"[33686 33930]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\2\03.png"),"[33931 34045]")

filterblock2()
ConvertTo16Bit(10,true)
Prefetch(32)
function filterblock2(clip c) {
c
    src=last
    src16=src.ConvertBits(16)
    filtered=src.ConvertTo16Bit().ConvertToStacked().gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=2.2,u=2,v=2).ConvertFromStacked()
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

function RELIFEAA(clip c) {
    c
    aa=ExtractY().InsaneAA(dscale=720,mask=0, desc_str=0.28, mt=false)
InsaneAA(aa_clip=aa)
}


function titles_mask(clip c) {
c
rescaled = DeBilinearResizeMT(1280,720, threads=1).BilinearResizeMT(1920,1080, threads=1)
diff = mt_makediff(last, rescaled, 3,3,3)
diff.mt_lut("x 114 < 0 255 ?").mt_edge("prewitt",16,16,u=0,v=0).removegrain(2).removegrain(2).removegrain(2).mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_inpand(60).mt_inflate()
}


