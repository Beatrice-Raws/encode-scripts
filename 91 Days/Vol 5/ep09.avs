ClearAutoloadDirs()
AddAutoloadDir("C:\0\_Video_\AviSynthPlus\plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("00003.dgi")
insaneaa =        episode         .InsAA()

ncop = DGSource("../../../NCOP.dgi").trim(48,2204)
ncop_aa = RawSource("../../../NCOP.yuv").trim(48,2204)
op_titles = episode.trim(1392,3548)
Assert(op_titles.framecount() == ncop.framecount(), "OP DROP"+\
" ncop len: "+String(ncop.framecount())+" op_titles len: "+String(op_titles.framecount()))
op = merge_credits64(op_titles, ncop, ncop_aa)

nced = DGSource("../../../NCED.dgi").trim(60,2204)
nced_aa = RawSource("../../../NCED.yuv").trim(60,2204)
ed_titles = episode.trim(32716,34860)
Assert(ed_titles.framecount() == nced.framecount(), "ED DROP"+\
" nced len: "+String(nced.framecount())+" ed_titles len: "+String(ed_titles.framecount()))
ed = merge_credits64(ed_titles, nced, nced_aa)

insaneaa.trim(0,1391)+op+insaneaa.trim(3549,32715)+ed+insaneaa.trim(34861,34884)
Assert(episode.framecount() == last.framecount(), "LENGTH DROP"+\
" episode len: "+String(episode.framecount())+" trim len: "+String(last.framecount()))

#mt_makediff(ed_titles, nced, 3,3,3)
#scenes 
/*
#rfs_once(hiaa, 30000, 31427)
#rfs_once(external_aa_mask_tlrd(episode,last,".\masks30\mask_00028_PV_TITLE.png"), 35082, 35172)
*/
#mask creation
                    /*   
src1=episode
resc=src1.spline36resize(970,540).Spline64Resize(1920, 1080)
#resc=src1.spline36resize(1280,720).Spline64Resize(1920, 1080)
#resc=src1.spline36resize(1440,810).Spline64Resize(1920, 1080)
mt_makediff(src1,resc,3,3,3).mt_edge("roberts",5,5,5,5).removegrain(5)
#                                    */

#filters      
filterblock()
#ConvertBits(8,true,0)
ConvertTo16Bit(10,true)
Prefetch(8)

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