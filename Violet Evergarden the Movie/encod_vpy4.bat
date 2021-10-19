.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m film.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --ctu 32 --max-tu-size 16 --pme --pmode -F 16 --no-cutree --qp-adaptation-range 4 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --lookahead-slices 1 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.02 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --hrd --master-display G(8500,39850)B(6550,2300)R(35400,14600)WP(15635,16450)L(10000000,1) --max-cll 308,123 --vbv-bufsize 160000 --vbv-maxrate 160000 --dolby-vision-rpu "RPU.bin" --dolby-vision-profile 81 --chromaloc 2 --colorprim bt2020 --transfer smpte2084 --colormatrix bt2020nc --qcomp 0.72 --output "01.hevc" --csv-log-level 0 --csv "01.txt" --y4m -



pause


