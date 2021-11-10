prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSource("01.dgi")
nced = DGSource("NCED01.dgi").trim(24,2060)
nced_aa = RawSource("NCED.yuv").trim(24,2060)
ed_titles = episode.trim(30413,32449)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)





insaneaa.trim(0,30412)+ed+insaneaa.trim(32500,0)

rfs(qtgmc(InputType=1,SourceMatch=3),"[8074 8168]")

rfs(external_aa_mask_tlrd(episode,last,".\mask\01.png"),"[7953 8036]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\02.png"),"[8074 8151]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\03.png"),"[8169 8252]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\04.png"),"[8376 8461]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\05.png"),"[8462 8533]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\06.png"),"[8534 8619]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\07.png"),"[8620 8697]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\08.png"),"[8801 8878]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\09.png"),"[9000 9063]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\10.png"),"[9108 9196]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\11.png"),"[9300 9385]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12.png"),"[9559 9639]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13.png"),"[9680 9756]")

rfs(external_aa_mask_tlrd(episode,last,".\mask\1\01.png"),"[1023 1122]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\1\02.png"),"[33687 33936]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\1\03.png"),"[33937 34046]")


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







