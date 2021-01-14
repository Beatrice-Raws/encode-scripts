ClearAutoloadDirs()
AddAutoloadDir("C:\0\_Video_\AviSynthPlus\plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("00005.dgi")
insaneaa =        episode         .InsAA()
hiaa     =        episode         .HiAA(aa="eedi3", mthr=20)

ncop = DGSource("../../../NCOP.dgi").trim(48,2205)
ncop_aa = RawSource("../../../NCOP.yuv").trim(48,2205)
op_titles = episode.trim(48,2205)
Assert(op_titles.framecount() == ncop.framecount(), "OP DROP"+\
" ncop len: "+String(ncop.framecount())+" op_titles len: "+String(op_titles.framecount()))
op = merge_credits64(op_titles, ncop, ncop_aa)

insaneaa.trim(0,47)+op+insaneaa.trim(2206,33218)+episode.trim(33219,35340)
Assert(episode.framecount() == last.framecount(), "LENGTH DROP"+\
" episode len: "+String(episode.framecount())+" trim len: "+String(last.framecount()))

#mt_makediff(op_titles, ncop, 3,3,3)
#mt_makediff(ed_titles, nced, 3,3,3)

#scenes 
# первый эпизод с гало - 2326 - 14625
rfs_once(DeHalo_Alpha_MT_y8(darkstr=0, brightstr=0.8), 2326, 14625)
rfs_once(external_aa_mask_tlrd(hiaa,last,".\mask_13_008530.png"), 8452, 8547)
rfs_once(hiaa, 8548, 8607)
rfs_once(hiaa, 30143, 30213)
rfs_once(hiaa, 32238, 32291)


#filters      
filterblock()
#ConvertBits(8,true,0)
ConvertTo16Bit(10,true)
Prefetch(8)

last

[*                                    functions                                      *]

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

function DeHalo_Alpha_MT_y8(clip clp, float "rx", float "ry", float "darkstr", float "brightstr", float "lowsens", float "highsens", float "ss")
{
    rx        = default( rx,        2.0 )
    ry        = default( ry,        2.0 )
    darkstr   = default( darkstr,   1.0 )
    brightstr = default( brightstr, 1.0 )
    lowsens   = default( lowsens,    50 )
    highsens  = default( highsens,   50 )
    ss        = default( ss,        1.5 )
    LOS = string(lowsens)
    HIS = string(highsens/100.0)
    DRK = string(darkstr)
    BRT = string(brightstr)
    ox  = clp.width()
    oy  = clp.height()
    y8 = clp.converttoy8
    halos  = y8.bicubicresize(m4(ox/rx),m4(oy/ry)).bicubicresize(ox,oy,1,0)
    are    = mt_lutxy(y8.mt_expand,y8.mt_inpand,"x y -","x y -","x y -")
    ugly   = mt_lutxy(halos.mt_expand,halos.mt_inpand,"x y -","x y -","x y -")
    so     = mt_lutxy(ugly,are, "y x - y 0.001 + / 255 * "+LOS+" - y 256 + 512 / "+HIS+" + *" )
    lets   = mt_merge(halos,y8,so)
    remove = (ss==1.0) ? y8.repair(lets,1,-1)
              \        : y8.lanczosresize(m4(ox*ss),m4(oy*ss))
              \             .mt_logic(lets.mt_expand.bicubicresize(m4(ox*ss),m4(oy*ss)),"min")
              \             .mt_logic(lets.mt_inpand.bicubicresize(m4(ox*ss),m4(oy*ss)),"max")
              \             .lanczosresize(ox,oy)
    them   = mt_lutxy(clp,remove,"x y < x x y - "+DRK+" * - x x y - "+BRT+" * - ?",U=2,V=2)
    return( them )
}