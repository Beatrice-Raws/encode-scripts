vspipe.exe -y 08/08.vpy - | x265-x64-v3.0-aMod --pools "" --limit-modes --open-gop --cbqpoffs -2 --crqpoffs -2 --no-rskip --no-tskip --keyint 240 --no-cutree --ref 6 --bframes 9 --bframe-bias 0 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --deblock 1:-1 --aq-mode 3 --aq-strength 0.86 --tu-intra-depth 2 --tu-inter-depth 2 --me 2 --wpp --subme 5 --crf 14.5 --qcomp 0.72 --b-pyramid --merange 48 --weightp --weightb --rd 6 --psy-rd 2 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output 08/08.hevc --csv 08/08.txt --y4m -

vspipe.exe -y 09/09.vpy - | x265-x64-v3.0-aMod --pools "" --limit-modes --open-gop --cbqpoffs -2 --crqpoffs -2 --no-rskip --no-tskip --keyint 240 --no-cutree --ref 6 --bframes 9 --bframe-bias 0 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --deblock 1:-1 --aq-mode 3 --aq-strength 0.86 --tu-intra-depth 2 --tu-inter-depth 2 --me 2 --wpp --subme 5 --crf 14.5 --qcomp 0.72 --b-pyramid --merange 48 --weightp --weightb --rd 6 --psy-rd 2 --rdoq-level 2 --psy-rdoq 4 --sar 1:1 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output 09/09.hevc --csv 09/09.txt --y4m -

pause