prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)

episode=DGSourceIM("13.dgi")
insaneaa = episode.insaneAA(mt=false)
ed_titles = episode.trim(28788,29154)
ed_titles_aa=ed_titles.insaneAA(mt=false)
ed_mask=ed_titles.tcolormask("$B4CFFF $868FAB",26,lutthr=9).mt_expand().mt_expand().mt_expand().mt_expand()
ed = mt_merge(ed_titles_aa,ed_titles,ed_mask,true)
ed_titles2 = episode.trim(29501,30183)
ed_titles_aa2=ed_titles2.insaneAA(mt=false)
ed_mask2=ed_titles2.tcolormask("$B4CFFF $868FAB",26,lutthr=9).mt_expand().mt_expand().mt_expand().mt_expand()
ed2 = mt_merge(ed_titles_aa2,ed_titles2,ed_mask2,true)

insaneaa.trim(0,28787)+ed+insaneaa.trim(29155,29500)+ed2+insaneaa.trim(30184,31356)+episode.trim(31357,33716)+insaneaa.trim(33717,34036)+episode.trim(34037,0)

rfs(external_aa_mask_tlrd(episode,last,".\mask\13_01.png"),"[29156 29288]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13_02.png"),"[30369 30490]")
rfs(external_aa_mask_tlrd(episode,last,".\mask\13_03.png"),"[30591 30736]")

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
