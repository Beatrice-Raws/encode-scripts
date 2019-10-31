from vapoursynth import *
import atomchtools as atf
import fvsfunc as fvf
import gradfun_amod as gfa
import mvsfunc as mvf
import insaneAA
import cooldegrain

core.avs.LoadPlugin(r'D:\VS\AVSPlugins\DGDecodeNV.dll')
nced = core.avs.DGSource(r'.\..\index\NCED.dgi')
nced = insaneAA.insaneAA(nced, eedi3Cl1=True, eedi3Cl2=True, nnedi3Cl=True, descale_str=0.33, kernel='bicubic', descale_h=720, outputMode=2)
nced.set_output()
