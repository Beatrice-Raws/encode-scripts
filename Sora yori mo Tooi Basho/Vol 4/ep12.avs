ClearAutoloadDirs()
prefix="C:\0\_Video_\AviSynthPlus\"
AddAutoloadDir(prefix+"plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("00003.dgi")
insaneaa =        episode           .InsAA()
hiaa =               insaneaa         .HiAA(aa="eedi3", mthr=20)

insaneaa

#scenes

rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_000103.png"), 0078, 0147)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_000207.png"), 0195, 0264)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_000329.png"), 0308, 0377)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_000439.png"), 0416, 0485)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_000530.png"), 0520, 0590)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_000633.png"), 0621, 0690)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_000749.png"), 0734, 0803)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_000892.png"), 0864, 0933)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_001070.png"), 1046, 1116)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_001206.png"), 1178, 1247)

rfs_once(hiaa, 3409, 3410)
rfs_once(hiaa, 5557, 5700)
rfs_once(hiaa, 16318, 16365)
rfs_once(hiaa, 19304, 19363)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_022618.png"), 22541, 22621)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_022679.png"), 22664, 22720)

rfs_once(episode, 32610, 34166)/*
rfs_once(mt_merge(last,  episode, mask, true, offX = 100, offY = 0, w = 790, h = 1080), 32610, 33642)
rfs_once(mt_merge(last,  episode, mask, true, offX = 100, offY = 0, w = 960, h = 1080), 33643, 33803)
rfs_once(mt_merge(last,  episode, mask, true, offX = 100, offY = 0, w = 560, h = 1080), 33804, 33822)
rfs_once(mt_merge(last,  episode, mask, true, offX = 100, offY = 0, w = 470, h = 1080), 33823, 33880)
rfs_once(mt_merge(last,  episode, mask, true, offX = 100, offY = 0, w = 630, h = 1080), 33881, 34041)
rfs_once(external_aa_mask_tlrd(episode, last,".\mask_12_034134.png"), 34096, 34166)*/

/*
src1=episode
#resc=src1.spline36resize(970,540).Spline64Resize(1920, 1080)
resc=src1.spline36resize(1120,630).Spline64Resize(1920, 1080)
resc=src1.spline36resize(1280,720).Spline64Resize(1920, 1080)
#resc=src1.spline36resize(1440,810).Spline64Resize(1920, 1080)
mt_makediff(src1,resc,3,3,3).mt_edge("roberts",5,5,5,5).removegrain(5)*/

#filters
filterblock()
#ConvertBits(8,true,0)    #     */
ConvertTo16Bit(10,true)
Prefetch(8)
last
[*                                                                 functions                                                                 *]

/*function external_aa_mask_tlrd_16bit(clip c, clip filtered, string "mask")
{
    mask = ImageReader(mask,1,1).trim(1,1).ConvertToYV12().ConvertBits(16).loop(c.FrameCount()).mt_binarize().mt_expand().mt_expand()\
	.mt_expand().mt_expand().mt_inflate()
    return mt_merge(filtered,c,mask,luma=true)
}*/
function titles_mask(clip c, int height, int lut_edge) {
c 
width = height * 16 / 9
rescaled = DeBilinearResizeMT(width,height, threads=1).BilinearResizeMT(1920,1080, threads=1)
diff = mt_makediff(last, rescaled, 3,3,3)

diff.mt_lut("x "+String(lut_edge)+" < 0 255 ?").\
mt_edge("prewitt",16,16,u=0,v=0).removegrain(2).removegrain(2).removegrain(2).mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_expand().mt_inpand(60)#.mt_inflate()
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
/*function VeryHardAA(clip c) {
    c
    DeBilinearResizeMT(1280,720, threads=1)
    HiAA(aa="eedi3", mthr=20)
    BilinearResizeMT(1920,1080, threads=1)
}*/