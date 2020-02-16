@echo off

vspipe.exe -y "..\scripts\SP05.vpy" - | x265-x64-v3.3-pre+7-aMod-gcc9.2.1-opt-znver2 --hevc-aq --qp-adaptation-range 2 --limit-modes --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --no-rskip --no-tskip --keyint 240 --no-cutree --ref 4 --bframes 8 --bframe-bias 0 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 0:1 --tu-intra-depth 2 --tu-inter-depth 2 --me 2 --wpp --subme 5 --crf 15 --qcomp 0.72 --b-pyramid --merange 48 --weightp --weightb --rd 4 --psy-rd 2.5 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "..\output\SP05.hevc" --csv-log-level 2 --csv "..\logs\SP05.txt" --y4m -
