@echo off
FOR %%I IN (01 02 03 04 05 06 07 08 09 10 11 12) DO (
.\VapourSynth64-Portable-R50\vspipe.exe -y %%I.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --csv-log-level 0 --csv "%%I.txt" --y4m -

)


.\VapourSynth64-Portable-R50\vspipe.exe -y pv1.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "pv1.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y pv2.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "pv2.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y pv3.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "pv3.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p1.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p1.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p2.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p2.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p3.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p3.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p4.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p4.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p5.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p5.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p6.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p6.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p7.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p7.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p8.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p8.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p9.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p9.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p10.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p10.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y p11.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "p11.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y cm1.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "cm1.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y cm2.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "cm2.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y cm3.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "cm3.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y cm4.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "cm4.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y cm5.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "cm5.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y cm6.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "cm6.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y cm7.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "cm7.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y cm8.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "cm8.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y cm9.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "cm9.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y NCED.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "NCED.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -

.\VapourSynth64-Portable-R50\vspipe.exe -y NCOP.vpy - | x265-x64-v3.5+20-aMod-gcc10.2.1-opt-ivybridge --pme --no-cutree --no-strong-intra-smoothing --pmode -F 16 --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 8 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --aq-strength 1.01 --qcomp 0.72 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 4 --psy-rd 2 --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "NCOP.hevc" --csv-log-level 0 --csv "pv1.txt" --y4m -








pause

