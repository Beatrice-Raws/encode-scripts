prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)

episode=DGSourceIM("04.dgi")
ncop = DGSourceIM("NCOP2.dgi").trim(0,2159)
nced = DGSourceIM("NCED.dgi").trim(247,2502)
ncop_aa = RawSource("NCOP2.yuv").trim(0,2159)
nced_aa = RawSource("NCED.yuv").trim(247,2502)
op_titles = episode.trim(1775,3932)
ed_titles = episode.trim(31790,34045)
op = merge_credits64(op_titles, ncop, ncop_aa)
ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)
#ed_titles = episode.trim(31494,32509)
#ed_titles_aa=ed_titles.insaneAA(mt=false)
#ed_mask=ed_titles.tcolormask("$B4CFFF $868FAB",12,lutthr=9).mt_expand().mt_expand().mt_expand().mt_expand()
#ed = mt_merge(ed_titles_aa,ed_titles,ed_mask,true)

insaneaa.trim(0,1774)+op+insaneaa.trim(3933,31789)+ed+episode.trim(34046,0)

Mdegrain1ChromaFix(22,32,true)
Prefetch(24)
gradfun3(thr_det=3.0,smode=4,mask=6,elast=6,lsb=true,lsb_in=true,debug=0,u=3,y=3,v=3)
ConvertFromStacked()
src = last
u=src.UToY().Spline64Resize(1280,720)
v=src.VToY().Spline64Resize(1280,720)
y = src.ConvertToYUV444().Spline36Resize(1280,720)
YToUV(u, v, y)

ConvertBits(10, true)
