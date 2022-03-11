@echo off
FOR %%I IN (12 13 NCOP NCED NCED2 NCED3 NCED4 NCED5) DO (
.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m %%I.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --limit-refs 2 --rc-lookahead 240 --ctu 32 --max-tu-size 16 --hist-scenecut --analyze-src-pics --pme --pmode -F 16 --no-cutree --qp-adaptation-range 2 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 14.7 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --psy-rd 2 --qcomp 0.72 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -

)

@echo off
FOR %%I IN (M1 M2 M3) DO (
.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m %%I.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --limit-refs 2 --rc-lookahead 240 --ctu 32 --max-tu-size 16 --hist-scenecut --analyze-src-pics --pme --pmode -F 16 --no-cutree --qp-adaptation-range 2 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --psy-rd 2 --qcomp 0.72 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -

)

.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m 03.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --zones 9285,9674,b=0.72/19607,19708,b=0.72/19793,20020,b=0.72 --limit-refs 2 --rc-lookahead 240 --ctu 32 --max-tu-size 16 --hist-scenecut --analyze-src-pics --pme --pmode -F 16 --no-cutree --qp-adaptation-range 2 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 14.7 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --psy-rd 2 --qcomp 0.72 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "03.hevc" --csv-log-level 0 --csv "21.txt" --y4m -


@echo off
FOR %%I IN (NCOP) DO (
.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m %%I.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --limit-refs 2 --rc-lookahead 240 --ctu 32 --max-tu-size 16 --hist-scenecut --analyze-src-pics --pme --pmode -F 16 --qp-adaptation-range 2 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 16 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --psy-rd 2 --qcomp 0.72 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -

)






pause

