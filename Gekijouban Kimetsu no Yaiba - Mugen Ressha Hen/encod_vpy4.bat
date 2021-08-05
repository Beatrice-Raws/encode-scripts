.\VapourSynth64-Portable-R50\vspipe.exe -y 01.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --zones 80168,81528,b=0.8 --pme --pmode -F 16 --ctu 32 --max-tu-size 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --no-cutree --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --no-strong-intra-smoothing --aq-strength 1.03 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 16 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "01.hevc" --csv-log-level 0 --csv "16.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y 02.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --pmode -F 16 --ctu 32 --max-tu-size 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --no-cutree --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --no-strong-intra-smoothing --aq-strength 1.03 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 16 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "02.hevc" --csv-log-level 0 --csv "16.txt" --y4m -












pause


