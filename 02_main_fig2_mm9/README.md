# Fig 2 (mm9) — GLI3 limb manuscript

This folder contains scripts and derived outputs used to generate Figure 2.

## Included
- `scripts/` : quantification + plotting scripts for Fig2C and supporting table generation.
- `inputs/` : derived TSV(s) used to plot Fig2C (tracked in git).
- `outputs/panels/` : panel exports (A/B/C) in PNG/SVG.
- `tables/` : supporting Excel table for Fig2C.
- `notes/caption/` : final caption text.

## Not included (too large)
Raw bigWig tracks (*.bw), Hi-C files (*.hic), and other large binaries are excluded via `.gitignore`.

## Reproduce Fig2C (example)
python fig2/scripts/plot_Fig2C_grouped_three_marks_shared_axis_v3_clean.py \
  --tsv fig2/inputs/Fig2C_enhancer_meanSignal_WT_HL_E115_mm9.fixed.tsv \
  --out-prefix fig2/outputs/panels/Fig2C_grouped_threeMarks_sharedAxis_v3_CLEAN \
  --drop-all-zero \
  --gap-between-groups 0.30

## Final plot used in manuscript
- Final Fig2C basename: `Fig2C_grouped_threeMarks_sharedAxis_v3_CLEAN`
- Fig2C plot script: `scripts/plot_Fig2C_grouped_three_marks_shared_axis_v3_clean.py`
- Input TSV: `inputs/Fig2C_enhancer_meanSignal_WT_HL_E115_mm9.fixed.tsv`
- Expected outputs: `outputs/panels/Fig2C_grouped_threeMarks_sharedAxis_v3_CLEAN.(png|svg)`
