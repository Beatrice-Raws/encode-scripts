vspipe -c y4m movie.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --qcomp 0.72 --pme --pmode -F 16 --no-cutree --qp-adaptation-range 4 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.03 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "movie.hevc" --csv-log-level 0 --csv "movie.txt" --y4m -
pause


