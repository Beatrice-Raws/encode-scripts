.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m Film.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --zones 0,455,b=1.8 --ctu 32 --rc-lookahead 240 --max-tu-size 16 --pme --pmode -F 16 --qp-adaptation-range 2 --open-gop --no-strong-intra-smoothing --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 1.02 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15.5 --weightp --weightb --rd 5 --rdoq-level 1 --psy-rdoq 3 --refine-mv 3 --hist-scenecut --analyze-src-pics --qcomp 0.72 --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "Film.hevc" --csv-log-level 0 --csv "01.txt" --y4m -

.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m 02.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --ctu 32 --rc-lookahead 240 --max-tu-size 16 --pme --pmode -F 16 --qp-adaptation-range 2 --open-gop --no-strong-intra-smoothing --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 1.02 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15.7 --weightp --weightb --rd 5 --rdoq-level 1 --psy-rdoq 3 --refine-mv 3 --hist-scenecut --analyze-src-pics --qcomp 0.72 --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "02.hevc" --csv-log-level 0 --csv "01.txt" --y4m -

.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m 04.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --ctu 32 --rc-lookahead 240 --max-tu-size 16 --pme --pmode -F 16 --qp-adaptation-range 2 --open-gop --no-strong-intra-smoothing --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 1.02 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15.7 --weightp --weightb --rd 5 --rdoq-level 1 --psy-rdoq 3 --refine-mv 3 --hist-scenecut --analyze-src-pics --qcomp 0.72 --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "04.hevc" --csv-log-level 0 --csv "01.txt" --y4m -

.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m 01.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --rc-lookahead 240 --pme --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 1 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --aq-mode 4 --aq-strength 1.02 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 16 --weightp --weightb --rd 5 --rdoq-level 1 --psy-rdoq 3 --refine-mv 3 --hist-scenecut --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "01.hevc" --csv-log-level 0 --csv "01.txt" --y4m -

pause
