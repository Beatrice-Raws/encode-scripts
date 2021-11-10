prefix="C:\Program Files (x86)\AviSynth+\"
AddAutoloadDir(prefix+"plugins64")
SetMemoryMax(30000)
SetFilterMTMode("DEFAULT_MT_MODE",2)

DGSourceIM("PD2.dgi")
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
