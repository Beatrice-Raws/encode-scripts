ClearAutoloadDirs()
prefix="C:\0\_Video_\AviSynthPlus\"
AddAutoloadDir(prefix+"plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("00003.dgi")
luma = Histogram(episode, "luma")
insaneaa =        episode           .InsAA()
hiaa =               insaneaa         .HiAA(aa="eedi3", mthr=20)

ncop = DGSource("../../../NCOP.dgi").trim(0,2158)#0,2159
ncop_aa = RawSource("../../../NCOP.yuv").trim(0,2158)
op_titles = episode.trim(1798,3956)#1798,3956
Assert(op_titles.framecount() == ncop.framecount(), "OP DROP"+\
" ncop len: "+String(ncop.framecount())+" op_titles len: "+String(op_titles.framecount()))
op = merge_credits64(op_titles, ncop, ncop_aa)

nced = DGSource("../../../NCED.dgi").trim(24,2161)#24,2161
nced_aa = RawSource("../../../NCED.yuv").trim(24,2161)
ed_titles = episode.trim(31744,33881)#31744,33881
Assert(ed_titles.framecount() == nced.framecount(), "ED DROP"+\
" nced len: "+String(nced.framecount())+" ed_titles len: "+String(ed_titles.framecount()))
ed = merge_credits64(ed_titles, nced, nced_aa)

insaneaa.trim(0,1797)+op+insaneaa.trim(3957,31743)+ed+insaneaa.trim(33882,34191)

#mt_makediff(op_titles, ncop, 3,3,3)
#mt_makediff(ed_titles, nced, 3,3,3)

#scenes
rfs_once(external_aa_mask_tlrd(hiaa, last, ".\mask_09_000126.png"), 126, 167)
rfs_once(external_aa_mask_tlrd(VeryVeryHardAA(insaneaa),last,".\mask_09_007672.png"), 7651, 7695)
rfs_once(external_aa_mask_tlrd(hiaa, last, ".\mask_09_007673.png"), 7651, 7695)
rfs_once(external_aa_mask_tlrd(hiaa, last, ".\mask_09_011323.png"), 11321, 11392)
rfs_once(external_aa_mask_tlrd(hiaa, last, ".\mask_09_012517.png"), 12437, 12532)
rfs_once(hiaa, 12683, 12778)
rfs_once(external_aa_mask_tlrd(hiaa, last, ".\mask_09_019684.png"), 19603, 19710)
rfs_once(hiaa, 20860, 20907)
rfs_once(external_aa_mask_tlrd(hiaa, last, ".\mask_09_022681.png"), 22649, 22690)
rfs_once(hiaa, 23075, 23314)
rfs_once(external_aa_mask_tlrd(VeryVeryHardAA(insaneaa),last,".\mask_09_023209.png"), 23075, 23314)
rfs_once(external_aa_mask_tlrd(hiaa, last, ".\mask_09_025903.png"), 25808, 25903)
rfs_once(hiaa, 34022, 34081)


#filters         
filterblock()
#ConvertBits(8,true,0)    #     */
ConvertTo16Bit(10,true)
Prefetch(8)
Assert(episode.framecount() == last.framecount(), "LENGTH DROP")
last
[*                                                                 functions                                                                 *]

/*function external_aa_mask_tlrd_16bit(clip c, clip filtered, string "mask")
{
    mask = ImageReader(mask,1,1).trim(1,1).ConvertToYV12().ConvertBits(16).loop(c.FrameCount()).mt_binarize().mt_expand().mt_expand()\
	.mt_expand().mt_expand().mt_inflate()
    return mt_merge(filtered,c,mask,luma=true)
}*/
function filterblock(clip c) {
    c
    src=last
    src16=src.ConvertBits(16)
    
    #строит маски по векторам движения, сигма - сила
    #vPF = src.dfttest(sigma=2.0,tbsize=1,lsb=true).ConvertFromStacked()
    
    #кулдеграйн - шумодав по яркости и цвету
    degrain=src.CoolDegrain1(48,80)#,pf=vPF)
        
    # градфан - дебандер. лсб - костыль для высокой битности. 
    # смод - 4, новый, старые нахер. дхт_дет - сила дебанда по яркости
    # u,v — 0 - удалить??, 1 - заменить черным, 2 - копировать, 3 - обрабатывать
    # тв-рендж - 0-255
    filtered=degrain.gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=2.6,u=2,v=2,tv_range=true).ConvertFromStacked()
    mask=src.mixed_linemask_deband_16bit()
    mt_merge(filtered,src16,mask)
}
/*function filterblock_mega(clip c) {
    c
    src16=c.Dither_convert_8_to_16()
    mask = c.mt_edge("prewitt",7,8,8,8,u=3,v=3)
    maskf = mt_logic(mask,mt_logic(mask.utoy(),mask.vtoy(),"or").spline64resize(width,height),"or").mt_expand()
    dfttest(tbsize=3, sigma=15, lsb=true)
    gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=8,u=3,v=3,tv_range=true, dyn_grain=true, detect_val=50, grain_val=80)
    Dither_merge16_8(last, src16, maskf, y=3, u=3, v=3, luma=true)
    ConvertfromStacked()
}*/
function mixed_linemask_deband_16bit(clip c) {
    c.ConvertBits(16)
    # thr - в основном сила дебанда
    thr_y=7
    thr_uv=8
    #mt_edge - создает маску по линиям
    #prewitt - тип маски; paramscale - втф?
    mask=mt_edge("prewitt",thr_y,thr_y,thr_uv,thr_uv,u=3,v=3,paramscale="i8")
    mask_y=mask.ExtractY()
    mask_u=mask.ExtractU()
    mask_v=mask.ExtractV()
    #мт_логик - бинарное сложение масок
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
/*function VeryHardAA(clip c) {
    c
    DeBilinearResizeMT(1280,720, threads=1)
    HiAA(aa="eedi3", mthr=20)
    BilinearResizeMT(1920,1080, threads=1)
}*/
function VeryVeryHardAA(clip c) {
    c
    DeBilinearResizeMT(1280,720, threads=1)
    HiAA(aa="eedi3", mthr=40)
    HiAA(aa="eedi3", mthr=40)
    BilinearResizeMT(1920,1080, threads=1)
}