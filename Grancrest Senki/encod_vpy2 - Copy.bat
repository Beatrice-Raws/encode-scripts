.\VSPortableR48\vspipe.exe -y 22.vpy - | x265-x64-v3.3+11-aMod-gcc9.2.1-opt-ivybridge -F 16 --pme --pmode --hevc-aq --qp-adaptation-range 2 --limit-modes --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --no-tskip --keyint 240 --no-cutree --ref 4 --bframes 9 --bframe-bias 0 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 4 --tu-inter-depth 4 --me 3 --wpp --subme 5 --crf 15.5 --qcomp 0.72 --b-pyramid --b-intra --rd-refine --analyze-src-pics --temporal-mvp --max-merge 5 --merange 48 --weightp --weightb --rd 5 --psy-rd 2.5 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "22.hevc" --csv-log-level 2 --csv "22.txt" --y4m -

.\VSPortableR48\vspipe.exe -y 23.vpy - | x265-x64-v3.3+11-aMod-gcc9.2.1-opt-ivybridge -F 16 --pme --pmode --hevc-aq --qp-adaptation-range 2 --limit-modes --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --no-tskip --keyint 240 --no-cutree --ref 4 --bframes 9 --bframe-bias 0 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 4 --tu-inter-depth 4 --me 3 --wpp --subme 5 --crf 15.5 --qcomp 0.72 --b-pyramid --b-intra --rd-refine --analyze-src-pics --temporal-mvp --max-merge 5 --merange 48 --weightp --weightb --rd 5 --psy-rd 2.5 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "23.hevc" --csv-log-level 2 --csv "22.txt" --y4m -

@echo off
FOR %%I IN (02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24) DO (
.\VSPortableR48\vspipe.exe -y P%%I.vpy - | x265-x64-v3.3+11-aMod-gcc9.2.1-opt-ivybridge -F 16 --pme --pmode --hevc-aq --qp-adaptation-range 2 --limit-modes --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --no-tskip --keyint 240 --no-cutree --ref 4 --bframes 9 --bframe-bias 0 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 4 --tu-inter-depth 4 --me 3 --wpp --subme 5 --crf 15.5 --qcomp 0.72 --b-pyramid --b-intra --rd-refine --analyze-src-pics --temporal-mvp --max-merge 5 --merange 48 --weightp --weightb --rd 5 --psy-rd 2.5 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "P%%I.hevc" --csv-log-level 2 --csv "22.txt" --y4m -

)





pause
