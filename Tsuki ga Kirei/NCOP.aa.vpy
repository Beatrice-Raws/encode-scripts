from vapoursynth import *
import insaneAA
core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
ncop = core.avs.DGSource(r'.\index\NCOP.dgi')
aaop = insaneAA.insaneAA(ncop, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.32, kernel='bicubic', descale_h=720, outputMode=2)
aaop.set_output()
