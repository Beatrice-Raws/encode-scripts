.\VapourSynth64-Portable-R50\vspipe.exe -y 12.vpy - | x265-x64-v3.3+14-aMod-gcc9.2.1-opt-ivybridge --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --no-tskip --keyint 240 --no-cutree --ref 4 --bframes 6 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.85 --deblock 1:-1 --tu-intra-depth 3 --b-intra --rd-refine --tu-inter-depth 3 --me 3 --wpp --subme 5 --crf 15 --no-strong-intra-smoothing --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --b-pyramid --merange 48 --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "12.hevc" --csv-log-level 2 --csv "film.txt" --y4m -














pause


