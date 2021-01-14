ClearAutoloadDirs()
AddAutoloadDir("C:\0\_Video_\AviSynthPlus\plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("00004.dgi")
insaneaa =        episode         .InsAA()
hiaa =               episode        .HiAA(aa="eedi3", mthr=20)

ncop = DGSource("../../../NCOP.dgi").trim(48,2206)
ncop_aa = RawSource("../../../NCOP.yuv").trim(48,2206)
op_titles = episode.trim(1990,4148)
Assert(op_titles.framecount() == ncop.framecount(), "OP DROP"+\
" ncop len: "+String(ncop.framecount())+" op_titles len: "+String(op_titles.framecount()))
op = merge_credits64(op_titles, ncop, ncop_aa)

insaneaa.trim(0,1989)+op+insaneaa.trim(4149,34860)
Assert(episode.framecount() == last.framecount(), "LENGTH DROP"+\
" episode len: "+String(episode.framecount())+" trim len: "+String(last.framecount()))

#mt_makediff(op_titles, ncop, 3,3,3)
#mt_makediff(ed_titles, nced, 3,3,3)
#scenes 

rfs_once(hiaa, 102, 184)
rfs_once(hiaa, 515, 560)   
rfs_once(hiaa, 1268, 1335)
rfs_once(external_aa_mask_tlrd(hiaa.VeryHardAA(),last,".\mask_12_019435.png"), 19435, 19444)
rfs_once(external_aa_mask_tlrd(hiaa.VeryHardAA(),last,".\mask_12_019445.png"), 19445, 19454)
rfs_once(external_aa_mask_tlrd(hiaa.VeryHardAA(),last,".\mask_12_019455.png"), 19455, 19464)
rfs_once(external_aa_mask_tlrd(hiaa.VeryHardAA(),last,".\mask_12_019465.png"), 19465, 19474)
rfs_once(external_aa_mask_tlrd(hiaa.VeryHardAA(),last,".\mask_12_019475.png"), 19475, 19484)
rfs_once(external_aa_mask_tlrd(hiaa.VeryHardAA(),last,".\mask_12_019485.png"), 19485, 19494)
rfs_once(external_aa_mask_tlrd(hiaa.VeryHardAA(),last,".\mask_12_019495.png"), 19495, 19504)
rfs_once(external_aa_mask_tlrd(hiaa.VeryHardAA(),last,".\mask_12_019505.png"), 19505, 19514)
rfs_once(external_aa_mask_tlrd(hiaa.VeryHardAA(),last,".\mask_12_019515.png"), 19515, 19524)
rfs_once(external_aa_mask_tlrd(hiaa.VeryHardAA(),last,".\mask_12_019525.png"), 19525, 19530)

rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_032105.png"), 32066, 32173)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_032235.png"), 32210, 32317)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_032380.png"), 32354, 32461)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_032529.png"), 32498, 32605)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_032685.png"), 32642, 32749)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_032803.png"), 32786, 32893)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_032969.png"), 32930, 33037)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_033134.png"), 33074, 33181)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_033260.png"), 33218, 33325)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_033397.png"), 33362, 33469)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_033575.png"), 33506, 33613)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_033683.png"), 33650, 33757)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_033819.png"), 33794, 33901)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_033980.png"), 33938, 34045)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_034107.png"), 34082, 34189)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_034255.png"), 34226, 34333)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_12_034720.png"), 34692, 34799)





#mask creation
                   /*   
src1=episode
#resc=src1.spline36resize(970,540).Spline64Resize(1920, 1080)
resc=src1.spline36resize(1280,720).Spline64Resize(1920, 1080)
#resc=src1.spline36resize(1440,810).Spline64Resize(1920, 1080)
mt_makediff(src1,resc,3,3,3).mt_edge("roberts",5,5,5,5).removegrain(5)
#                                    */

#filters      
filterblock()
#ConvertBits(8,true,0)
ConvertTo16Bit(10,true)
Prefetch(6)

last
[*                                                                 functions                                                                 *]

function filterblock(clip c) {
    c
    src=last
    src16=src.ConvertBits(16)
    
    #строит маски по векторам движения, сигма - сила
    vPF = src.dfttest(sigma=2.0,tbsize=1,lsb=true).ConvertFromStacked()
    
    #кулдеграйн - шумодав по яркости и цвету
    degrain=src.CoolDegrain1(54,60,pf=vPF)
    
    # градфан - дебандер. лсб - костыль для высокой битности. 
    # смод - 4, новый, старые нахер. дхт_дет - сила дебанда по яркости
    # u,v — 0 - удалить??, 1 - заменить черным, 2 - копировать, 3 - обрабатывать
    # тв-рендж - 0-255
    filtered=degrain.gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=2.2,u=2,v=2,tv_range=true).ConvertFromStacked()
    mask=src.mixed_linemask_deband_16bit()
    mt_merge(filtered,src16,mask)
}
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
function VeryHardAA(clip c) {
    c
    DeBilinearResizeMT(1280,720, threads=1)
    HiAA(aa="eedi3", mthr=13)
    BilinearResizeMT(1920,1080, threads=1)
}