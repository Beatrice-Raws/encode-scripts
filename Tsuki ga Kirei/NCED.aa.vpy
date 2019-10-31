from vapoursynth import *
import insaneAA
core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
nced = core.avs.DGSource(r'.\index\NCED.dgi')
aaed = insaneAA.insaneAA(nced, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.32, kernel='bicubic', descale_h=720, outputMode=2)
aaed.set_output()
