@echo off
FOR %%I IN (01 02 03 04 05 06 07 08 09 10 11 12 13 14 NCED) DO (
.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m %%I.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --limit-refs 2 --rc-lookahead 240 --ctu 32 --max-tu-size 16 --hist-scenecut --analyze-src-pics --pme --pmode -F 16 --no-cutree --qp-adaptation-range 2 --open-gop --no-strong-intra-smoothing --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 1.01 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 14 --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 3 --refine-mv 3 --qcomp 0.72 --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -


)

pause


