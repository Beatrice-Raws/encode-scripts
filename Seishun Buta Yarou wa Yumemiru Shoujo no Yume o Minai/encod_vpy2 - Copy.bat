.\VSPortableR48\vspipe.exe -y 01.vpy - | x265-x64-v3.2.1+7-aMod-gcc9.2.1-opt-ivybridge -F 16 --pme --pmode --hevc-aq --qp-adaptation-range 2 --limit-modes --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --no-rskip --no-tskip --keyint 240 --no-cutree --ref 4 --bframes 9 --bframe-bias 0 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 2 --tu-inter-depth 2 --me 2 --wpp --subme 5 --crf 14.5 --qcomp 0.72 --b-pyramid --merange 48 --weightp --weightb --rd 4 --psy-rd 2 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "01.hevc" --csv-log-level 2 --csv "22.txt" --y4m -

.\VSPortableR48\vspipe.exe -y 01_720.vpy - | x265-x64-v3.2.1+7-aMod-gcc9.2.1-opt-ivybridge -F 16 --pme --pmode --hevc-aq --qp-adaptation-range 2 --limit-modes --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --no-rskip --no-tskip --keyint 240 --no-cutree --ref 6 --bframes 9 --bframe-bias 0 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 2 --tu-inter-depth 2 --me 2 --wpp --subme 5 --crf 13.4 --qcomp 0.72 --b-pyramid --merange 48 --weightp --weightb --rd 4 --psy-rd 2 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "01_720.hevc" --csv-log-level 2 --csv "25_720.txt" --y4m -


























pause
