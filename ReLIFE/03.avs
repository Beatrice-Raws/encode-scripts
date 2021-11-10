prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSource("03.dgi")
nced = DGSource("NCED03.dgi").trim(421,2113)
nced_aa = RawSource("NCED3.yuv").trim(421,2113)
ed_titles = episode.trim(31996,33688)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)





insaneaa.trim(0,31995)+ed+insaneaa.trim(33689,0)

rfs(qtgmc(InputType=1,SourceMatch=3),"[1098 1192]")


rfs(external_aa_mask_tlrd(episode,last,".\mask\01.png"),"[977 1060]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\02.png"),"[1098 1175]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\03.png"),"[1193 1276]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\04.png"),"[1400 1485]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\05.png"),"[1486 1557]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\06.png"),"[1558 1643]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\07.png"),"[1644 1721]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\08.png"),"[1825 1902]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\09.png"),"[2024 2087]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\10.png"),"[2132 2220]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\11.png"),"[2324 2409]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12.png"),"[2583 2663]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13.png"),"[2704 2780]")


rfs(external_aa_mask_tlrd(episode,last,".\mask\3\01.png"),"[0 83]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\3\02.png"),"[33689 33929]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\3\03.png"),"[33930 34048]")


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

