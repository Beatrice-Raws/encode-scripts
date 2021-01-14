ClearAutoloadDirs()
prefix="C:\0\_Video_\AviSynthPlus\"
AddAutoloadDir(prefix+"plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("00002.dgi")
luma = Histogram(episode, "luma")
insaneaa =        episode           .InsAA()
hiaa =               insaneaa         .HiAA(aa="eedi3", mthr=20)

ncop = DGSource("../../../../NCOP.dgi").trim(0,2156)#0,2159
ncop_aa = RawSource("../../../../NCOP.yuv").trim(0,2156)
op_titles = episode.trim(2470,4626)
op = merge_credits64(op_titles, ncop, ncop_aa)
Assert(op_titles.framecount() == op.framecount(), "OP DROP")

nced = DGSource("../../../../NCED.dgi").trim(24,2161)#24,2161
nced_aa = RawSource("../../../../NCED.yuv").trim(24,2161)
ed_titles = episode.trim(32008,34145)
ed = merge_credits64(ed_titles, nced, nced_aa)
Assert(ed_titles.framecount() == ed.framecount(), "ED DROP")

insaneaa.trim(0,2469)+op+insaneaa.trim(4627,32007)+ed+insaneaa.trim(34146,34191)

#mt_makediff(op_titles, ncop, 3,3,3)
#mt_makediff(ed_titles, nced, 3,3,3)

#scenes
rfs_once(external_aa_mask_tlrd(hiaa,last,".\mask_02_7684.png"), 7569, 7836)
rfs_once(external_aa_mask_tlrd(hiaa,last,".\mask_02_7684.png"), 8587, 8711)
rfs_once(external_aa_mask_tlrd(hiaa,last,".\mask_02_25756.png"), 25756, 25822)

#filters      

filterblock()
#ConvertBits(8,true,0)
ConvertTo16Bit(10,true)
Prefetch(8)

Assert(episode.framecount() == last.framecount(), "LENGTH DROP")
last
[*                                                                 functions                                                                 *]

function filterblock(clip c) {
    c
    src=last
    src16=src.ConvertBits(16)
    
    #строит маски по векторам движения, сигма - сила
    #vPF = src.dfttest(sigma=2.0,tbsize=1,lsb=true).ConvertFromStacked()
    
    #кулдеграйн - шумодав по яркости и цвету
    degrain=src.CoolDegrain1(48,52)#,pf=vPF)
        
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