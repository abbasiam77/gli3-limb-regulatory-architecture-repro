# Gli3 limb regulatory genomics reproducibility repository

This repository contains figure-, table-, and analysis-oriented reproducibility
materials for an integrative re-analysis of validated regulatory elements in
the mouse Gli3 locus.

The September 2026 manuscript revision analyzes 13 curated functionally
supported Gli3 limb enhancers across chromatin, transcription-factor, and
chromosome-contact datasets. Functional validation is the anchor for enhancer
identity; genomic signal layers are interpreted as correlative and contextual
rather than as evidence of direct regulatory mechanism or causation.

A locus-matched comparison with 41 validated non-limb Gli3-region enhancers
shows substantial overlap across several bulk chromatin and
transcription-factor signal layers. The repository therefore supports
multi-layer contextual interpretation rather than functional classification
from any single genomic dataset.

## Main figure modules

- `01_main_fig1_mm9/` — Gli3 contact-domain visualization using mm9 Hi-C,
  architectural-protein tracks, and RNA-seq context.
- `02_main_fig2_mm9/` — histone-mark visualization and enhancer-wise
  H3K4me1/H3K27ac/H3K4me3 quantification.
- `03_main_fig3_mm10/` — HOXA13/HOXD13 visualization and enhancer-wise HOX13
  quantification.
- `04_main_fig4/` — integrated 54-enhancer rank-percentile signal heatmap.
- `05_main_fig5/` — locus-matched validated limb versus non-limb enhancer
  comparison and single-layer AUC summary.

## Supplementary analysis modules

- `supp_fig_gli3_chipseq_mm10_e11p5/` — GLI3 ChIP-seq reanalysis supporting
  Supplementary Figure S1 and Supplementary Table S3.
- `supp_virtual4c_gli3_hindlimb_hic_mm9/` — promoter-centered Virtual 4C
  supporting Supplementary Figure S2 and Supplementary Tables S4a/S4b.
- `supp_table_s5_phase1_support_layer/` — p300, HAND2, and PITX1 supporting
  signal layers.
- `supp_table_s6_limb_vs_non_limb_control/` — source materials for the
  validated limb versus non-limb comparison.
- `supp_figs_submission_pdf/` — exact current Additional File 1 PDF.
- `supp_tables_submission_xlsx/` — exact current Additional File 2 workbook.

## Exact current manuscript assets

`submission_assets/` contains byte-identical copies of the five current main
figure PDFs, two current main tables, Additional File 1, its editable
PowerPoint source, and Additional File 2.

## Historical material

Materials belonging to an earlier manuscript configuration but no longer part
of the current submission are retained under `archive/` where useful for
provenance. In particular, the former Supplementary Figure S3 is historical.
Its limb/non-limb comparison is represented in the current manuscript by Main
Figure 5 and Supplementary Tables S6a/S6b/S7.

## Genome-build policy

Analyses are build-aware. Architectural-protein, histone, RNA-seq, Hi-C, and
Virtual 4C analyses are presented in mm9 where required by their processed-data
context. HOXA13/HOXD13 and GLI3 ChIP-seq analyses are presented in mm10.
Build-specific coordinate handling is documented in the relevant modules.

## Reproducibility scope

The underlying genomic datasets are publicly available and are not
redistributed when unnecessary. This repository provides processed or derived
tables, scripts, provenance documentation, manuscript-ready outputs, and exact
submission assets needed to trace the analyses to their public sources.
