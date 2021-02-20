@echo off
FOR %%I IN (01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24) DO (
.\VapourSynth64-Portable-R50\vspipe.exe -y %%I.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -
)


.\VapourSynth64-Portable-R50\vspipe.exe -y NCOP.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "NCOP.hevc" --csv-log-level 0 --csv "NCOP.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y NCOP2.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "NCOP2.hevc" --csv-log-level 0 --csv "NCOP.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y NCED.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "NCED.hevc" --csv-log-level 0 --csv "NCED.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y NCED2.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "NCED2.hevc" --csv-log-level 0 --csv "NCED.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y m1.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "m1.hevc" --csv-log-level 0 --csv "m1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y m2.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "m2.hevc" --csv-log-level 0 --csv "m2.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y m3.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "m3.hevc" --csv-log-level 0 --csv "m3.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y m4.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "m4.hevc" --csv-log-level 0 --csv "m4.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y m5.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "m5.hevc" --csv-log-level 0 --csv "m5.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y m6.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "m6.hevc" --csv-log-level 0 --csv "m6.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p1.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 300 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p1.hevc" --csv-log-level 0 --csv "p1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p2.vpy - | x265-10b --pme --pmode -F 16 --hevc-aq --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 1 --keyint 240 --no-cutree --ref 4 --bframes 8 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 4 --aq-strength 0.86 --deblock 1:-1 --tu-intra-depth 3 --refine-intra 4 --dynamic-refine --tu-inter-depth 3 --me 3 --wpp --subme 7 --crf 14.5 --no-strong-intra-smoothing --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 5 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p2.hevc" --csv-log-level 0 --csv "p2.txt" --y4m -


































pause


