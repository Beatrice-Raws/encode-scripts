FOR %%I IN (16 17 18 19 20 21 22 23 24 25 26) DO (
.\VapourSynth64-Portable-R50\vspipe.exe -y %%I.vpy - | x265-10b --pme --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240  --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --no-strong-intra-smoothing --aq-strength 1.03 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 16 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -
)



pause
