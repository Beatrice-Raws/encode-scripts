ClearAutoloadDirs()
prefix="C:\0\_Video_\AviSynthPlus\"
AddAutoloadDir(prefix+"plugins64")
SetFilterMTMode("DEFAULT_MT_MODE",2)

LWLibAvVideoSource("crf16_dfttest_sigma_2.0.264")
ConvertFromDoubleWidth(10)
ConvertBits(8, dither=0)