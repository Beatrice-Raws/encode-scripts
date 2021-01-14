ClearAutoloadDirs()
prefix="C:\0\_Video_\AviSynthPlus\"
AddAutoloadDir(prefix+"plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)
SetMemoryMax(8000)

episode = DGSource("NCED.dgi")
episode.InsAA()    

Prefetch(8)

last

[*                                                                 functions                                                                 *]

function InsAA(clip c) {
    c
    aa=ExtractY().InsaneAA(dscale=719,mask=0, desc_str=0.28)
    InsaneAA(aa_clip=aa)
}