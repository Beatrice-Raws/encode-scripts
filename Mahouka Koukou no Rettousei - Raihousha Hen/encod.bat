@echo off
FOR %%I IN (01 02 03 04 05 06 07 08 09 10 11 12 13 NCED NCOP PV1 PV2 PV3 CM1 CM2 CM3 CM4 CM5 CM6 NEXT1 NEXT2 NEXT3 NEXT4 NEXT5 NEXT6 NEXT7 NEXT8 NEXT9 NEXT10 NEXT11 NEXT12 NEXT13) DO (
.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m %%I.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --ctu 32 --rc-lookahead 240 --max-tu-size 16 --pme --pmode -F 16 --no-cutree --qp-adaptation-range 2 --open-gop --no-strong-intra-smoothing --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 1.02 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 14.5 --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --refine-mv 3 --hist-scenecut --analyze-src-pics --qcomp 0.72 --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -
)

@echo off
FOR %%I IN (M1 M2 M3 M4 M5 M6) DO (
.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m %%I.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --ctu 32 --rc-lookahead 240 --max-tu-size 16 --pme --pmode -F 16 --no-cutree --qp-adaptation-range 2 --open-gop --no-strong-intra-smoothing --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 1.02 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --refine-mv 3 --hist-scenecut --analyze-src-pics --qcomp 0.72 --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -
)

pause

