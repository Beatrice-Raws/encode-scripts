prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)

episode=DGSourceIM("01.dgi")
#ncop = DGSource("NCOP1.dgi").trim(0,2160)
#nced = DGSourceIM("NCED2.dgi").trim(0,2158)
#ncop_aa = RawSource("NCOP1.yuv").trim(0,2157)
#nced_aa = RawSource("NCED2.yuv").trim(0,2158)
#op_titles = episode.trim(0,2157)
#ed_titles = episode.trim(30905,33063)
#op = merge_credits64(op_titles, ncop, ncop_aa)
#ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)
ed_titles = episode.trim(30884,33887)
ed_titles_aa=ed_titles.insaneAA(mt=false)
ed_mask=ed_titles.tcolormask("$B4CFFF $868FAB",12,lutthr=9).mt_expand().mt_expand().mt_expand().mt_expand()
ed = mt_merge(ed_titles_aa,ed_titles,ed_mask,true)

insaneaa.trim(0,17428)+insaneaa.trim(17429,17506)+insaneaa.trim(17507,30883)+ed+episode.trim(33888,0)

rfs(external_aa_mask_tlrd(episode,last,".\mask\01_01.png"),"[0 166]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\01_02.png"),"[899 996]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\01_03.png"),"[1006 1089]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\01_04.png"),"[1101 1186]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\01_05.png"),"[1212 1309]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\01_06.png"),"[1609 1703]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\01_07.png"),"[1723 1820]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\01_08.png"),"[1952 2049]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\01_09.png"),"[2101 2198]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\01_10.png"),"[2958 3055]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\01_11.png"),"[3110 3219]")

CoolDegrain1(42,96,false,true,4)
Prefetch(24)
gradfun3(thr_det=3.0,smode=4,mask=6,elast=6,lsb=true,lsb_in=true,debug=0,u=3,y=3,v=3)
ConvertFromStacked(16)
ConvertTo16Bit(10,true)
# CoolDegrain v0.1 - 01.02.2017
# - initial release
# CoolDegrain v0.2 - 01.02.2017
# - added "pf" option: pass heavy denoised clip ontp manalyse to improve denoising
# - more manalyse params are configurable now

function CoolDegrain1(clip c, int "thsad", int "thsadc", bool "lsb", bool "stack16", int "overlap", int "blksize", int "search", int "pelsearch", bool "truemotion", clip "pf") {
    thsad      = Default(thsad,           40)
    thsadc     = Default(thsadc,       thsad)
    lsb        = Default(lsb,          false)
    stack16    = Default(stack16,       true)
    overlap    = Default(overlap,          4)
    blksize    = Default(blksize,          8)
    search     = Default(search,           4)
    pelsearch  = Default(pelsearch,        2)
    truemotion = Default(truemotion,   false)
    pf         = Default(pf,       Undefined)

    c
    Assert(isYUV(), "YUV only.")
    Assert(! (BitsPerComponent() > 8 && lsb), "You can't use LSB mode with HBD input.")
    (! lsb && BitsPerComponent() == 8) ? ConvertBits(16) : NOP()
    sup = msuper()
	sPF = isClip(pf) ? pf.ConvertBits(BitsPerComponent()).msuper() : sup
    fa  = manalyse(sPF, isb=false, delta=1, overlap=overlap, truemotion=truemotion)
    fb  = manalyse(sPF, isb=true,  delta=1, overlap=overlap, truemotion=truemotion)
    mdegrain1(sup, fb, fa, thsad=thsad, thsadc=thsadc, lsb=lsb)
	(! lsb && stack16 && BitsPerComponent() < 16 && BitsPerComponent() > 8) ? ConvertBits(16) : NOP()
    return (! lsb && stack16) ? ConvertToStacked() : last
}

function CoolDegrain2(clip c, int "thsad", int "thsadc", bool "lsb", bool "stack16", int "overlap", int "blksize", int "search", int "pelsearch", bool "truemotion", clip "pf") {
    thsad      = Default(thsad,           40)
    thsadc     = Default(thsadc,       thsad)
    lsb        = Default(lsb,          false)
    stack16    = Default(stack16,       true)
    overlap    = Default(overlap,          4)
    blksize    = Default(blksize,          8)
    search     = Default(search,           4)
    pelsearch  = Default(pelsearch,        2)
    truemotion = Default(truemotion,   false)
    pf         = Default(pf,       Undefined)

    c
    Assert(isYUV(), "YUV only.")
    Assert(! (BitsPerComponent() > 8 && lsb), "You can't use LSB mode with HBD input.")
    (! lsb && BitsPerComponent() == 8) ? ConvertBits(16) : NOP()
    sup = msuper()
	sPF = isClip(pf) ? pf.ConvertBits(BitsPerComponent()).msuper() : sup
    fa1  = manalyse(sPF, isb=false, delta=1, overlap=overlap, truemotion=truemotion)
    fa2  = manalyse(sPF, isb=false, delta=2, overlap=overlap, truemotion=truemotion)
    fb1  = manalyse(sPF, isb=true,  delta=1, overlap=overlap, truemotion=truemotion)
    fb2  = manalyse(sPF, isb=true,  delta=2, overlap=overlap, truemotion=truemotion)
    mdegrain2(sup, fb1, fa1, fb2, fa2, thsad=thsad, thsadc=thsadc, lsb=lsb)
	(! lsb && stack16 && BitsPerComponent() < 16 && BitsPerComponent() > 8) ? ConvertBits(16) : NOP()
    return (! lsb && stack16) ? ConvertToStacked() : last
}

function CoolDegrain3(clip c, int "thsad", int "thsadc", bool "lsb", bool "stack16", int "overlap", int "blksize", int "search", int "pelsearch", bool "truemotion", clip "pf") {
    thsad      = Default(thsad,           40)
    thsadc     = Default(thsadc,       thsad)
    lsb        = Default(lsb,          false)
    stack16    = Default(stack16,       true)
    overlap    = Default(overlap,          4)
    blksize    = Default(blksize,          8)
    search     = Default(search,           5)
    pelsearch  = Default(pelsearch,        2)
    truemotion = Default(truemotion,    true)
    pf         = Default(pf,       Undefined)

    c
    Assert(isYUV(), "YUV only.")
    Assert(! (BitsPerComponent() > 8 && lsb), "You can't use LSB mode with HBD input.")
    (! lsb && BitsPerComponent() == 8) ? ConvertBits(16) : NOP()
    sup = msuper()
	sPF = isClip(pf) ? pf.ConvertBits(BitsPerComponent()).msuper() : sup
    fa1  = manalyse(sPF, isb=false, delta=1, overlap=overlap, blksize=blksize, search=search, pelsearch=pelsearch, truemotion=truemotion)
    fa2  = manalyse(sPF, isb=false, delta=2, overlap=overlap, blksize=blksize, search=search, pelsearch=pelsearch, truemotion=truemotion)
    fa3  = manalyse(sPF, isb=false, delta=3, overlap=overlap, blksize=blksize, search=search, pelsearch=pelsearch, truemotion=truemotion)
    fb1  = manalyse(sPF, isb=true,  delta=1, overlap=overlap, blksize=blksize, search=search, pelsearch=pelsearch, truemotion=truemotion)
    fb2  = manalyse(sPF, isb=true,  delta=2, overlap=overlap, blksize=blksize, search=search, pelsearch=pelsearch, truemotion=truemotion)
    fb3  = manalyse(sPF, isb=true,  delta=3, overlap=overlap, blksize=blksize, search=search, pelsearch=pelsearch, truemotion=truemotion)
    mdegrain3(sup, fb1, fa1, fb2, fa2, fb3, fa3, thsad=thsad, thsadc=thsadc, lsb=lsb)
	(! lsb && stack16 && BitsPerComponent() < 16 && BitsPerComponent() > 8) ? ConvertBits(16) : NOP()
    return (! lsb && stack16) ? ConvertToStacked() : last
}

