op_t=DGSource("F:\TsuGaKirei\index\EP12.dgi")#.trim(0,2000)
#ncop=DGSource("F:\TsuGaKirei\index\NCOP.dgi").trim(24,2183)
#mt_makediff(op_t,ncop, 3,3,3)
op_t
rescale_mask(0,0,1920,1080)
function rescale_mask(clip c, int "offX", int "offY", int "w", int "h") {
    offX = Default(offX, 0)
    offY = Default(offY, 0)
    w = Default(w, 0)
    h = Default(h, 0)
    
    offcet = (offX > 0 || offY > 0 ? 2 : 0) # нужно сдвигать область на несколько пикселей вверх и влево, чтобы избежать рамки при склеивании. Баг из-за mt_inflate
    xsize = offcet + 2 # аналогично с offcet, но надо откатить область обратно вправо и внизу (увеличить на offcet) и добавить еще несколько пикселей, чтобы избавитсья от нежелательной рамки

    rescaled = c.DeBicubicResizeMT(1280,720).BicubicResize(1920,1080) # самый простой способ увидеть "неапнутые" детальки - даунскейльнуть и апнуть обратно, затем сравнить через mt_makediff
    diff = mt_makediff(c, rescaled, y=3, u=0, v=0) # только Y плоскость, цвета заполняем черным - они нам не понядобятся
    diff.mt_edge("prewitt", thY1=16, thY2=16, u=0, v=0).mt_expand().mt_expand().mt_inpand().mt_inflate() # строим маску по "разнице"
    ExtractY()
}
function diff_mask(clip c, int "offX", int "offY", int "w", int "h") {
    offX = Default(offX, 0)
    offY = Default(offY, 0)
    w = Default(w, 0)
    h = Default(h, 0)
    
    offcet = (offX > 0 || offY > 0 ? 2 : 0) # нужно сдвигать область на несколько пикселей вверх и влево, чтобы избежать рамки при склеивании. Баг из-за mt_inflate
    xsize = offcet + 2 # аналогично с offcet, но надо откатить область обратно вправо и внизу (увеличить на offcet) и добавить еще несколько пикселей, чтобы избавитсья от нежелательной рамки

    rescaled = c.FreezeFrame(26, 119, 31) # самый простой способ увидеть "неапнутые" детальки - даунскейльнуть и апнуть обратно, затем сравнить через mt_makediff
    diff = mt_makediff(c, rescaled, y=3, u=0, v=0, offX=offX-offcet, offY=offY-offcet, w=w+xsize, h=h+xsize) # только Y плоскость, цвета заполняем черным - они нам не понядобятся
    diff.mt_edge("sobel", thY1=15, thY2=15, u=0, v=0, offX=offX-offcet, offY=offY-offcet, w=w+xsize, h=h+xsize).mt_expand().mt_expand().mt_expand().mt_inpand().mt_inflate() # строим маску по "разнице"
    ExtractY()
}
/*
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\01.png'), "[32 110]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\02.png'), "[111 175]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\03.png'), "[176 243]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\04.png'), "[244 314]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\05.png'), "[339 401]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\06.png'), "[447 542]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\07.png'), "[543 638]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\08.png'), "[639 731]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\09.png'), "[732 815]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\10.png'), "[819 902]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\11.png'), "[906 989]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\12.png'), "[993 1077]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\13.png'), "[1078 1149]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\14.png'), "[1153 1224]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\15.png'), "[1228 1299]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\16.png'), "[1312 1419]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\17.png'), "[1444 1551]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\OP\12\18.png'), "[1576 1677]")

mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\12\01.png'), "[28108 28167]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\12\02.png'), "[28276 28347]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\12\03.png'), "[28348 28413]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\12\04.png'), "[28889 28993]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\12\05.png'), "[29564 29659]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\12\06.png'), "[32446 32543]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\12\07.png'), "[32544 32639]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\ED\12\08.png'), "[32666 32776]")


*/