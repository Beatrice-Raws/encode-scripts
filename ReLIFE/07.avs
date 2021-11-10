prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSource("07.dgi")
nced = DGSource("NCED07.dgi").trim(316,2714)
nced_aa = RawSource("NCED7.yuv").trim(316,2714)
ed_titles = episode.trim(31288,33686)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)





insaneaa.trim(0,31287)+ed+insaneaa.trim(33687,0)

rfs(qtgmc(InputType=1,SourceMatch=3),"[2321 2415]")


rfs(external_aa_mask_tlrd(episode,last,".\mask\01.png"),"[2200 2283]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\02.png"),"[2321 2398]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\03.png"),"[2416 2499]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\04.png"),"[2623 2708]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\05.png"),"[2709 2780]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\06.png"),"[2781 2866]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\07.png"),"[2867 2944]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\08.png"),"[3048 3125]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\09.png"),"[3247 3310]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\10.png"),"[3355 3443]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\11.png"),"[3547 3632]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12.png"),"[3806 3886]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13.png"),"[3927 4003]")






rfs(external_aa_mask_tlrd(episode,last,".\mask\7\01.png"),"[4005 4087]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\7\02.png"),"[33687 33928]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\7\03.png"),"[33929 34046]")


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

