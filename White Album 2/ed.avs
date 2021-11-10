prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)

DGSourceIM("00004.dgi")
Mdegrain1ChromaFix(48,64,true)
Prefetch(24)
gradfun3(thr_det=3.0,smode=4,mask=6,elast=6,lsb=true,lsb_in=true,debug=0,u=3,y=3,v=3)
ConvertFromStacked(16)
ConvertTo16Bit(10,true)
