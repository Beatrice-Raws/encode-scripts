@echo off
FOR %%I IN (01 02 03 04 05 06 07 08 09 10 11 13 14) DO (
.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m %%I.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --temporal-layers --amp --scenecut 40 --limit-refs 2 --rect --b-intra --rc-lookahead 240 --ctu 32 --max-tu-size 16 --no-hist-scenecut --analyze-src-pics --pme --pmode -F 16 --qp-adaptation-range 1 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.02 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 14 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --qcomp 0.72 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -


)

.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m 12.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --zones 2789,3915,b=0.70 --temporal-layers --amp --scenecut 40 --limit-refs 2 --rect --b-intra --rc-lookahead 240 --ctu 32 --max-tu-size 16 --no-hist-scenecut --analyze-src-pics --pme --pmode -F 16 --qp-adaptation-range 1 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.02 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 14 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --qcomp 0.72 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "12.hevc" --csv-log-level 0 --csv "12.txt" --y4m -

@echo off
FOR %%I IN (M01 M02 M03 M04 M05 M06 NCOP1 NCOP2 NCOP3 NCOP4 NCOP4 NCOP5 NCOP6 NCED1 NCED2 NCED3 NEXT01 PV01 PV02 PV03 PV04 PV05) DO (
.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m %%I.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --temporal-layers --amp --scenecut 40 --limit-refs 2 --rect --b-intra --rc-lookahead 240 --ctu 32 --max-tu-size 16 --no-hist-scenecut --analyze-src-pics --pme --pmode -F 16 --qp-adaptation-range 1 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.02 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 14 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --qcomp 0.72 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -


)



pause


