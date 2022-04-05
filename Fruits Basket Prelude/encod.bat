.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m 01.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --zones 5531,6785,b=0.60 --limit-refs 2 --rc-lookahead 240 --ctu 32 --max-tu-size 16 --hist-scenecut --analyze-src-pics --pme --pmode -F 16 --no-cutree --qp-adaptation-range 2 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 14.5 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --psy-rd 2 --qcomp 0.72 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "01.hevc" --csv-log-level 0 --csv "01.txt" --y4m -

.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m 02.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --limit-refs 2 --rc-lookahead 240 --ctu 32 --max-tu-size 16 --hist-scenecut --analyze-src-pics --pme --pmode -F 16 --qp-adaptation-range 2 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --psy-rd 2 --qcomp 0.72 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "02.hevc" --csv-log-level 0 --csv "02.txt" --y4m -









pause

