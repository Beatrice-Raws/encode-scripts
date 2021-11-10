prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSource("09.dgi")
nced = DGSource("NCED09.dgi").trim(390,2373)
nced_aa = RawSource("NCED9.yuv").trim(390,2373)
ed_titles = episode.trim(31704,33687)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)





insaneaa.trim(0,31703)+ed+insaneaa.trim(33688,0)

rfs(qtgmc(InputType=1,SourceMatch=3),"[1170 1264]")

rfs(external_aa_mask_tlrd(episode,last,".\mask\01.png"),"[1049 1132]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\02.png"),"[1170 1247]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\03.png"),"[1265 1348]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\04.png"),"[1472 1557]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\05.png"),"[1558 1629]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\06.png"),"[1630 1715]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\07.png"),"[1716 1793]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\08.png"),"[1897 1974]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\09.png"),"[2096 2159]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\10.png"),"[2204 2292]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\11.png"),"[2396 2481]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12.png"),"[2655 2735]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13.png"),"[2776 2852]")








rfs(external_aa_mask_tlrd(episode,last,".\mask\9\01.png"),"[2855 2916]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\9\02.png"),"[33688 33929]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\9\03.png"),"[33930 34047]")


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

