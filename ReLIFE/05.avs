prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSource("05.dgi")
nced = DGSource("NCED05.dgi").trim(266,1801)
nced_aa = RawSource("NCED5.yuv").trim(266,1801)
ed_titles = episode.trim(30783,32318)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)





insaneaa.trim(0,30782)+ed+insaneaa.trim(32319,0)

rfs(qtgmc(InputType=1,SourceMatch=3),"[978 1072]")


rfs(external_aa_mask_tlrd(episode,last,".\mask\01.png"),"[857 940]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\02.png"),"[978 1055]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\03.png"),"[1073 1156]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\04.png"),"[1280 1365]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\05.png"),"[1366 1437]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\06.png"),"[1438 1523]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\07.png"),"[1524 1601]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\08.png"),"[1705 1782]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\09.png"),"[1904 1967]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\10.png"),"[2012 2100]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\11.png"),"[2204 2289]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12.png"),"[2463 2543]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13.png"),"[2584 2660]")




rfs(external_aa_mask_tlrd(episode,last,".\mask\5\01.png"),"[2670 2732]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\5\02.png"),"[33689 33929]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\5\03.png"),"[33930 34048]")


#mt_makediff(ed_titles, nced,FALSE, 3,3,3)#.Histogram("luma")


src=last
src16=src.ConvertBits(16)
filtered=src.ConvertTo16Bit().ConvertToStacked().gradfun3(thr_det=2.2,smode=4,lsb_in=true,lsb=true,debug=0,u=3,y=3,v=3).ConvertFromStacked(bits=16)
mask=src.build_lumachroma322_mask16bit().mt_invert()
mt_merge(src16, filtered,mask, true)
ConvertTo16Bit(10,true)
Prefetch(24)
function build_lumachroma322_mask16bit(clip c) {
c.ConvertBits(16)
thr_y=2250
thr_uv=954
mask=mt_edge("prewitt",thr_y,thr_y,thr_uv,thr_uv,u=3,v=3)
mask_y=mask.converttoy()
mask_u=mask.UToY()
mask_v=mask.VToY()
mt_logic(mask_y.mt_expand().mt_deflate(), mt_logic(mask_u.removegrain(2), mask_v.removegrain(2), "or").BicubicResize(mask_y.Width(), mask_y.Height()), "or")
uv=last.BicubicResize(mask_u.Width(), mask_u.Height())
YtoUV(uv,uv,last).mt_binarize()
}
function build_lumachroma322_mask(clip c) {
c
thr_y=15
thr_uv=10
mask=mt_edge("prewitt",thr_y,thr_y,thr_uv,thr_uv,u=3,v=3)
mask_y=mask.converttoy()
mask_u=mask.UToY()
mask_v=mask.VToY()
mt_logic(mask_y.mt_expand().mt_deflate(), mt_logic(mask_u, mask_v, "or").BicubicResize(mask_y.Width(), mask_y.Height()), "or")
}

