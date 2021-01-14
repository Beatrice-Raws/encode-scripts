ClearAutoloadDirs()
prefix="C:\0\_Video_\AviSynthPlus\"
AddAutoloadDir(prefix+"plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("00001.dgi")
luma = Histogram(episode, "luma")

insaneaa =        episode          .InsAA()
hiaa =               insaneaa         .HiAA(aa="eedi3", mthr=20)

             #         /*
ncop = DGSource("../../../../NCOP.dgi").trim(0,2157)#0,2159
ncop_aa = RawSource("../../../../NCOP.yuv").trim(0,2157)
op_titles = episode.trim(3213,5370)
op = merge_credits64(op_titles, ncop, ncop_aa)
Assert(op_titles.framecount() == op.framecount(), "OP DROP")

insaneaa.trim(0,3212)+op+insaneaa.trim(5371,34191)

#mt_makediff(op_titles, ncop, 3,3,3)
#mt_makediff(ed_titles, nced, 3,3,3)

#scenes
rfs_once(hiaa, 8858, 9007)
rfs_once(hiaa, 15554, 15697)
rfs_once(external_aa_mask_tlrd(hiaa,last,".\mask_01_17369.png"), 17214, 17369)
rfs_once(hiaa, 17615, 17758)
rfs_once(external_aa_mask_tlrd(hiaa,last,".\mask_01_28436.png"), 28376, 28416)
rfs_once(hiaa, 28417, 28463)
rfs_once(hiaa, 29044, 29097)
rfs_once(hiaa, 29393, 29402)
rfs_once(external_aa_mask_tlrd(hiaa,last,".\mask_01_32345.png"), 32344, 32415)

mask118 = titles_mask(episode, 720, 118)
mask119 = titles_mask(episode, 720, 119)
mask120 = titles_mask(episode, 720, 120)
mask121 = titles_mask(episode, 720, 121)
rfs_once(mt_merge(last,  episode, mask118, true), 29450, 29499)
rfs_once(mt_merge(last,  episode, mask119, true, offX = 130, offY = 0, w = 518, h = 1080), 29500, 30028)
rfs_once(mt_merge(last,  episode, mask120, true, offX = 130, offY = 0, w = 640, h = 1080), 30029, 30242)
rfs_once(mt_merge(last,  episode, mask120, true, offX = 130, offY = 0, w = 530, h = 1080), 30243, 30354)
rfs_once(mt_merge(last,  episode, mask119, true, offX = 130, offY = 0, w = 590, h = 1080), 30355, 30604)
rfs_once(mt_merge(last,  episode, mask120, true, offX = 130, offY = 0, w = 530, h = 1080), 30605, 31261)
rfs_once(mt_merge(last,  episode, mask120, true, offX = 130, offY = 0, w =1010,h = 1080), 31262, 31475)
rfs_once(mt_merge(last,  episode, mask120, true, offX = 130, offY = 0, w = 530, h = 1080), 31476, 31732)
rfs_once(mt_merge(last,  episode, mask121, true, offX = 130, offY = 0, w = 650, h = 1080), 31733, 31827)
rfs_once(mt_merge(last,  episode, mask120, true, offX = 130, offY = 0, w = 650, h = 1080), 31828, 31834)
rfs_once(mt_merge(last,  episode, mask121, true, offX = 130, offY = 0, w = 650, h = 0608), 31835, 31947)
rfs_once(external_aa_mask_tlrd(episode,last,".\mask_partners.png"), 34082, 34165)

#mask creation */
                    /*   
src1=episode
#resc=src1.spline36resize(970,540).Spline64Resize(1920, 1080)
resc=src1.spline36resize(1120,630).Spline64Resize(1920, 1080)
resc=src1.spline36resize(1280,720).Spline64Resize(1920, 1080)
#resc=src1.spline36resize(1440,810).Spline64Resize(1920, 1080)
mt_makediff(src1,resc,3,3,3).mt_edge("roberts",5,5,5,5).removegrain(5)
#                                    */
ep = last
#filters           /*
fbm = filterblock_mega(ep)
filterblock(ep)
rfs_once(fbm, 21863, 21940)
#ConvertBits(8,true,0)
ConvertTo16Bit(10,true)
Prefetch(8)

#selectTotal1=framecount()/100
#selectTotal2=selectTotal1*2
#selectrangeevery(selectTotal2,50)

#Histogram("luma")
#AssumeFPS(last, 60000,1001)
#Assert(episode.framecount() == last.framecount(), "LENGTH DROP") */
last#.ExtractV().BicubicResize(1920, 1080)
[*                                                                 functions                                                                 *]

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
    degrain=src.CoolDegrain1(48,52)#,pf=vPF)
        
    # градфан - дебандер. лсб - костыль для высокой битности. 
    # смод - 4, новый, старые нахер. дхт_дет - сила дебанда по яркости
    # u,v — 0 - удалить??, 1 - заменить черным, 2 - копировать, 3 - обрабатывать
    # тв-рендж - 0-255
    filtered=degrain.gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=2.2,u=2,v=2,tv_range=true).ConvertFromStacked()
    mask=src.mixed_linemask_deband_16bit()
    mt_merge(filtered,src16,mask)
}
function filterblock_mega(clip c) {
    c
    src16=c.Dither_convert_8_to_16()
    mask = c.mt_edge("prewitt",7,8,8,8,u=3,v=3)
    maskf = mt_logic(mask,mt_logic(mask.utoy(),mask.vtoy(),"or").spline64resize(width,height),"or").mt_expand()
    dfttest(tbsize=3, sigma=148, lsb=true)
    gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=100,u=3,v=3,tv_range=true, dyn_grain=true, detect_val=90, grain_val=80)
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