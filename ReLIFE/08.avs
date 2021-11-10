prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSource("08.dgi")
nced = DGSource("NCED08.dgi").trim(1123,3601)
nced_aa = RawSource("NCED8.yuv").trim(1123,3601)
ed_titles = episode.trim(31507,33685)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)





insaneaa.trim(0,31506)+ed+insaneaa.trim(33686,0)

rfs(qtgmc(InputType=1,SourceMatch=3),"[1458 1552]")

rfs(external_aa_mask_tlrd(episode,last,".\mask\01.png"),"[1337 1420]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\02.png"),"[1458 1535]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\03.png"),"[1553 1636]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\04.png"),"[1760 1845]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\05.png"),"[1846 1917]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\06.png"),"[1918 2003]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\07.png"),"[2004 2081]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\08.png"),"[2185 2262]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\09.png"),"[2384 2447]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\10.png"),"[2492 2580]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\11.png"),"[2684 2769]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12.png"),"[2943 3023]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13.png"),"[3064 3140]")







rfs(external_aa_mask_tlrd(episode,last,".\mask\8\01.png"),"[3141 3188]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\8\02.png"),"[33686 33927]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\8\03.png"),"[33928 34045]")


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

