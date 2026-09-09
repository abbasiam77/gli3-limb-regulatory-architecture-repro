# Repository map

This map describes the September 2026 manuscript-aligned repository structure.

## Main figure modules

- `01_main_fig1_mm9/` — Main Figure 1: Gli3 contact-domain context using mm9
  Hi-C, architectural-protein tracks and RNA-seq.
- `02_main_fig2_mm9/` — Main Figure 2: histone-mark visualization and
  enhancer-wise H3K4me1/H3K27ac/H3K4me3 quantification.
- `03_main_fig3_mm10/` — Main Figure 3: HOXA13/HOXD13 visualization and
  enhancer-wise signal quantification.
- `04_main_fig4/` — Main Figure 4: integrated 54-enhancer × 9-layer
  rank-percentile heatmap.
- `05_main_fig5/` — Main Figure 5: validated limb versus non-limb Gli3-region
  enhancer comparison and single-layer AUC summary.

## Supplementary analysis modules

- `supp_fig_gli3_chipseq_mm10_e11p5/` — GLI3 ChIP-seq reanalysis supporting
  Supplementary Figure S1 and Supplementary Table S3.
- `supp_virtual4c_gli3_hindlimb_hic_mm9/` — promoter-centered Virtual 4C
  analysis supporting Supplementary Figure S2 and Supplementary Tables S4a/S4b.
- `supp_table_s5_phase1_support_layer/` — p300, HAND2 and PITX1 supporting
  signal-layer analysis used in Supplementary Table S5.
- `supp_table_s6_limb_vs_non_limb_control/` — source and provenance materials
  for the 13-limb versus 41-non-limb enhancer comparison.

## Current manuscript-ready supplementary bundles

- `supp_figs_submission_pdf/Additional File 1.pdf` — frozen supplementary
  figure file containing Supplementary Figures S1 and S2.
- `supp_tables_submission_xlsx/Additional File 2.xlsx` — frozen
  supplementary-table workbook containing S1, S2, S3, S4a, S4b, S5, S6a,
  S6b, S7 and S8.

## Exact manuscript snapshot

- `submission_assets/main_figures/` — final Main Figures 1-5.
- `submission_assets/main_tables/` — final Main Tables 1-2.
- `submission_assets/additional_files/` — final Additional Files 1 and 2 and
  the editable source for Additional File 1.

## Historical material

- `archive/legacy_supp_fig_s3_limb_vs_non_limb_control/` — former
  Supplementary Figure S3 materials retained for provenance only.
- `archive/legacy_docs/` — documentation describing earlier repository or
  manuscript configurations.

## Suggested navigation

For figure-specific reproducibility, begin with the README in the relevant
`0X_main_fig*` module.

For the final manuscript package, use `submission_assets/`.

For supplementary tables, use the frozen
`supp_tables_submission_xlsx/Additional File 2.xlsx` together with the relevant
analysis module when provenance or underlying workflow details are required.
