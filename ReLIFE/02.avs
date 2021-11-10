prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSource("02.dgi")
nced = DGSource("NCED02.dgi").trim(512,2346)
nced_aa = RawSource("NCED2.yuv").trim(512,2346)
ed_titles = episode.trim(31852,33686)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)





insaneaa.trim(0,31851)+ed+insaneaa.trim(33687,0)

rfs(qtgmc(InputType=1,SourceMatch=3),"[1218 1312]")


rfs(external_aa_mask_tlrd(episode,last,".\mask\01.png"), "[1097 1180]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\02.png"), "[1218 1295]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\03.png"), "[1313 1396]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\04.png"), "[1520 1605]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\05.png"), "[1606 1677]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\06.png"), "[1678 1763]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\07.png"), "[1764 1841]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\08.png"), "[1945 2022]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\09.png"), "[2144 2207]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\10.png"), "[2252 2340]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\11.png"), "[2444 2529]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\12.png"), "[2703 2783]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13.png"), "[2824 2900]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\2\01.png"),"[2901 3019]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\2\02.png"),"[33687 33943]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\2\03.png"),"[33944 34046]")


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

