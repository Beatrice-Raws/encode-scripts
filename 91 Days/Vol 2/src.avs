ClearAutoloadDirs()
prefix="C:\0\_Video_\AviSynthPlus\"
AddAutoloadDir(prefix+"plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)

DGSource("00003.dgi")

selectTotal1=framecount()/100
selectTotal2=selectTotal1*2
selectrangeevery(selectTotal2,50)
last