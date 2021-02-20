@echo off
FOR %%I IN (12) DO (
.\VapourSynth64-Portable-R50\vspipe.exe -y %%I.vpy - | x265-x64-v3.4+56-aMod-gcc10.2.1-opt-ivybridge --pme --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.02 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 16 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -
)







pause


