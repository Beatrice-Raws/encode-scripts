prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSource("04.dgi")
nced = DGSource("NCED04.dgi").trim(240,2579)
nced_aa = RawSource("NCED4.yuv").trim(240,2579)
ed_titles = episode.trim(31345,33684)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)





insaneaa.trim(0,31344)+ed+insaneaa.trim(33685,0)

rfs(qtgmc(InputType=1,SourceMatch=3),"[3257 3351]")


rfs(external_aa_mask_tlrd(episode,last,".\mask\01.png"),"[3136 3219]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\02.png"),"[3257 3334]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\03.png"),"[3352 3435]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\04.png"),"[3559 3644]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\05.png"),"[3645 3716]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\06.png"),"[3717 3802]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\07.png"),"[3803 3880]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\08.png"),"[3984 4061]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\09.png"),"[4183 4246]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\10.png"),"[4291 4379]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\11.png"),"[4483 4568]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12.png"),"[4742 4822]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13.png"),"[4863 4939]")




rfs(external_aa_mask_tlrd(episode,last,".\mask\4\02.png"),"[33685 33923]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\4\03.png"),"[33924 34044]")


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

