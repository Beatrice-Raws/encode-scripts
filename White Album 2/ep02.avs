prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)

episode=DGSourceIM("02.dgi")
ncop = DGSourceIM("NCOP.dgi").trim(0,2159)
#nced = DGSourceIM("NCED2.dgi").trim(0,2158)
ncop_aa = RawSource("NCOP.yuv").trim(0,2159)
#nced_aa = RawSource("NCED2.yuv").trim(0,2158)
op_titles = episode.trim(2111,4268)
#ed_titles = episode.trim(30905,33063)
op = merge_credits64(op_titles, ncop, ncop_aa)
#ed = merge_credits64(ed_titles, nced, nced_aa)
insaneaa = episode.insaneAA(mt=false)
#ed_titles = episode.trim(30884,33887)
#ed_titles_aa=ed_titles.insaneAA(mt=false)
#ed_mask=ed_titles.tcolormask("$B4CFFF $868FAB",12,lutthr=9).mt_expand().mt_expand().mt_expand().mt_expand()
#ed = mt_merge(ed_titles_aa,ed_titles,ed_mask,true)

insaneaa.trim(0,2110)+op+insaneaa.trim(4269,32367)+episode.trim(32368,0)

Mdegrain1ChromaFix(48,64,true)
Prefetch(24)
gradfun3(thr_det=3.0,smode=4,mask=6,elast=6,lsb=true,lsb_in=true,debug=0,u=3,y=3,v=3)
ConvertFromStacked(16)
ConvertTo16Bit(10,true)


