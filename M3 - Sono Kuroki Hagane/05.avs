prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)


episode = DGSource("05.dgi")
ncop = DGSource("NCOP.dgi").trim(441,2295)
nced = DGSource("NCED.dgi").trim(258,2182)
ncop_aa = RawSource("NCOP.yuv").trim(441,2295)
nced_aa = RawSource("NCED.yuv").trim(258,2182)
op_titles = episode.trim(2438,4292)
ed_titles = episode.trim(32724,34646)
op = merge_credits64(op_titles, ncop, ncop_aa)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)

insaneaa.trim(0,2437)+op+insaneaa.trim(4293,32723)+ed+episode.trim(34647,0)

rfs(external_aa_mask_tlrd(episode,last,".\mask\05.png"),"[4376 4495]")

#mt_makediff(op_titles, ncop, 3,3,3)#.Histogram("luma")
#mt_makediff(ed_titles, nced, 3,3,3)#.Histogram("luma")

src=last
src16=src.ConvertBits(16)
filtered=src.ConvertTo16Bit().ConvertToStacked().gradfun3(lsb_in=true,lsb=true,smode=4,thr_det=3,u=2,v=2,tv_range=true).ConvertFromStacked(bits=16)
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
