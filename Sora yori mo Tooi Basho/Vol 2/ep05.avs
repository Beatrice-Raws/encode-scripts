ClearAutoloadDirs()
prefix="C:\0\_Video_\AviSynthPlus\"
AddAutoloadDir(prefix+"plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("00002.dgi")
insaneaa =        episode           .InsAA()
hiaa =               insaneaa         .HiAA(aa="eedi3", mthr=20)

ncop = DGSource("../../../NCOP.dgi").trim(0,2158)#0,2159
ncop_aa = RawSource("../../../NCOP.yuv").trim(0,2158)
op_titles = episode.trim(1630,3788)
Assert(op_titles.framecount() == ncop.framecount(), "OP DROP"+\
" ncop len: "+String(ncop.framecount())+" op_titles len: "+String(op_titles.framecount()))
op = merge_credits64(op_titles, ncop, ncop_aa)

nced = DGSource("../../../NCED.dgi").trim(24,2161)#24,2161
nced_aa = RawSource("../../../NCED.yuv").trim(24,2161)
ed_titles = episode.trim(31721,33858)
Assert(ed_titles.framecount() == nced.framecount(), "ED DROP"+\
" nced len: "+String(nced.framecount())+" ed_titles len: "+String(ed_titles.framecount()))
ed = merge_credits64(ed_titles, nced, nced_aa)

insaneaa.trim(0,1629)+op+insaneaa.trim(3789,31720)+ed+insaneaa.trim(33859,34191)
Assert(episode.framecount() == last.framecount(), "LENGTH DROP")

#mt_makediff(op_titles, ncop, 3,3,3)
#mt_makediff(ed_titles, nced, 3,3,3)

#scenes 
rfs_once(external_aa_mask_tlrd(hiaa,last,".\mask_05_008847.png"), 8843, 8923)
rfs_once(external_aa_mask_tlrd(hiaa,last,".\mask_05_009590.png"), 9521, 9598)
rfs_once(external_aa_mask_tlrd(hiaa,last,".\mask_05_017665.png"), 17665, 17811)
rfs_once(hiaa, 30447, 30506)

#filters      
filterblock()
#ConvertBits(8,true,0)    #     */
ConvertTo16Bit(10,true)
Prefetch(8)

last
[*                                                                 functions                                                                 *]

function external_aa_mask_tlrd_16bit(clip c, clip filtered, string "mask")
{
    mask = ImageReader(mask,1,1).trim(1,1).ConvertToYV12().ConvertBits(16).loop(c.FrameCount()).mt_binarize().mt_expand().mt_expand()\
	.mt_expand().mt_expand().mt_inflate()
    return mt_merge(filtered,c,mask,luma=true)
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
function filterblock_mega(clip c) {
    c
    src16=c.Dither_convert_8_to_16()
    mask = c.mt_edge("prewitt",7,8,8,8,u=3,v=3)
    maskf = mt_logic(mask,mt_logic(mask.utoy(),mask.vtoy(),"or").spline64resize(width,height),"or").mt_expand()
    dfttest(tbsize=3, sigma=15, lsb=true)
    gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=8,u=3,v=3,tv_range=true, dyn_grain=true, detect_val=50, grain_val=80)
    Dither_merge16_8(last, src16, maskf, y=3, u=3, v=3, luma=true)
    ConvertfromStacked()
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