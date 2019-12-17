.\vaporPortable-r44\vspipe.exe -y 12.vpy - | x265-x64-v3.0-aMod -F 16 --pools "" --hevc-aq --qp-adaptation-range 2 --limit-modes --open-gop --cbqpoffs -2 --crqpoffs -2 --no-rskip --no-tskip --keyint 240 --no-cutree --ref 4 --bframes 9 --bframe-bias 0 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 2 --tu-inter-depth 2 --me 2 --wpp --subme 5 --crf 14.9 --qcomp 0.72 --b-pyramid --merange 48 --weightp --weightb --rd 4 --psy-rd 2 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "12.hevc" --csv-log-level 2 --csv "12.txt" --y4m -

.\vaporPortable-r44\vspipe.exe -y 12_720.vpy - | x265-x64-v3.0-aMod -F 16 --pools "" --hevc-aq --qp-adaptation-range 2 --limit-modes --open-gop --cbqpoffs -2 --crqpoffs -2 --no-rskip --no-tskip --keyint 240 --no-cutree --ref 6 --bframes 9 --bframe-bias 0 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 2 --tu-inter-depth 2 --me 2 --wpp --subme 5 --crf 13.8 --qcomp 0.72 --b-pyramid --merange 48 --weightp --weightb --rd 4 --psy-rd 2 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "12_720.hevc" --csv-log-level 2 --csv "12_720.txt" --y4m -


.

































pause
