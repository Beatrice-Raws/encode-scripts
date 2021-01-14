ClearAutoloadDirs()
AddAutoloadDir("C:\0\_Video_\AviSynthPlus\plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(40000)

episode = DGSource("00014.dgi")
insaneaa =        episode           .InsAA()
hiaa =               insaneaa         .HiAA(aa="eedi3", mthr=20)

insaneaa

#mt_makediff(op_titles, ncop, 3,3,3)
#mt_makediff(ed_titles, nced, 3,3,3)

#scenes
rfs_once(hiaa, 281, 308)
rfs_once(hiaa, 678, 725)
rfs_once(hiaa, 3690, 3851)
rfs_once(external_aa_mask_tlrd(hiaa, last,".\mask_13_003853.png"), 3852, 3980)
rfs_once(external_aa_mask_tlrd(VeryHardAA(insaneaa), last,".\mask_13_003852.png"), 3852, 3980)
rfs_once(hiaa, 21781, 21858)
rfs_once(hiaa, 21937, 22484)
rfs_once(hiaa, 23080, 23199)
rfs_once(hiaa, 23748, 23803)
rfs_once(hiaa, 26847, 26918)
rfs_once(hiaa, 28168, 28257)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_030084_src.png"), 28570, 30108)
rfs_once(external_aa_mask_tlrd(hiaa, last,".\mask_13_030084_hiaa.png"), 30109, 30379)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_030084_src.png"), 30109, 30379)
rfs_once(hiaa, 30452, 30607)
rfs_once(hiaa, 30813, 30992)
rfs_once(hiaa, 31879, 32004)
rfs_once(hiaa, 32317, 32472)
rfs_once(hiaa, 32665, 32754)
rfs_once(hiaa, 33960, 34043)

rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_030533.png"), 30513, 30605)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_030688.png"), 30609, 30702)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_030883.png"), 30814, 30901)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_030938.png"), 30905, 30991)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_031284.png"), 31258, 31345)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_031375.png"), 31349, 31429)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_031837.png"), 31802, 31870)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_032637.png"), 32612, 32708)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_032805.png"), 32756, 32855)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_032993.png"), 32942, 33046)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_033225.png"), 33191, 33290)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_033721.png"), 33685, 33814)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_13_030533.png"), 33961, 34043)


#filters
ep = last
fbm = filterblock_mega(ep)
filterblock(ep)
rfs_once(fbm, 26847, 26918)
#ConvertBits(8,true,0)    #     */
ConvertTo16Bit(10,true)
Prefetch(32)
last

[*                                                                 functions                                                                 *]

function filterblock_mega(clip c) {
    c
    src=last
    src16=src.ConvertBits(16)
    vPF = src.dfttest(sigma=4.0,tbsize=1,lsb=true).ConvertFromStacked()
    degrain=src.CoolDegrain1(56,80,pf=vPF)
    filtered=degrain.gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=5,u=2,v=2,tv_range=true).ConvertFromStacked()
    mask=src.mixed_linemask_deband_16bit()
    mt_merge(filtered,src16,mask)
}
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
    HiAA(aa="eedi3", mthr=20)
    BilinearResizeMT(1920,1080, threads=1)
}