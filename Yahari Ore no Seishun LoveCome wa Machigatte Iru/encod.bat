@echo off
FOR %%I IN (02 05 11 ova) DO (
.\VapourSynth64-Portable-R55-API4-RC1\vspipe.exe -c y4m %%I.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --limit-refs 2 --ctu 32 --rc-lookahead 60 --max-tu-size 16 -F 4 --no-cutree --qp-adaptation-range 2 --no-strong-intra-smoothing --open-gop --cbqpoffs -2 --crqpoffs -2 --lookahead-slices 1 --no-early-skip --tskip --rskip 0 --keyint 240 --ref 4 --bframes 9 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.03 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 1 --psy-rdoq 2 --psy-rd 2 --qcomp 0.72 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -
)









































pause
