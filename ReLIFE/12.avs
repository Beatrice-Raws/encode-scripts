prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSource("12.dgi")
nced = DGSource("NCED12.dgi").trim(799,2921)
nced_aa = RawSource("NCED12.yuv").trim(799,2921)
ed_titles = episode.trim(30056,32178)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)





insaneaa.trim(0,30055)+ed+insaneaa.trim(32179,0)

rfs(qtgmc(InputType=1,SourceMatch=3),"[474 568]")

rfs(external_aa_mask_tlrd(episode,last,".\mask\01.png"),"[353 436]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\02.png"),"[474 551]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\03.png"),"[569 652]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\04.png"),"[776 861]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\05.png"),"[862 933]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\06.png"),"[934 1019]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\07.png"),"[1020 1097]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\08.png"),"[1201 1278]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\09.png"),"[1400 1463]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\10.png"),"[1508 1596]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\11.png"),"[1700 1785]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12.png"),"[1959 2039]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13.png"),"[2080 2156]")




rfs(external_aa_mask_tlrd(episode,last,".\mask\12\01.png"),"[5594 5676]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12\02.png"),"[33687 33929]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12\03.png"),"[33930 34046]")


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

