# Manuscript figure and supplementary-material mapping

This document maps the October 2026 Mammalian Genome manuscript to its
reproducibility modules, while preserving the September release.

## Main figures

| Manuscript item | Repository location | Description |
|---|---|---|
| Figure 1 | `01_main_fig1_mm9/` | Gli3 contact-domain visualization using mm9 Hi-C, architectural-protein tracks and RNA-seq context. |
| Figure 2 | `02_main_fig2_mm9/` | Histone-mark tracks and enhancer-wise H3K4me1, H3K27ac and H3K4me3 quantification. |
| Figure 3 | `03_main_fig3_mm10/` | HOXA13/HOXD13 tracks and enhancer-wise HOX13 quantification. |
| Figure 4 | `04_main_fig4/` | Integrated 54-enhancer rank-percentile heatmap across nine chromatin/TF layers. |
| Figure 5 | `05_main_fig5/` | Comparison of 13 functionally supported Gli3 limb enhancers with 41 annotation-based VISTA elements and descriptive AUC summaries. |

## Supplementary figures

| Manuscript item | Repository location | Description |
|---|---|---|
| Supplementary Figure S1 | `supp_fig_gli3_chipseq_mm10_e11p5/` and `supp_figs_submission_pdf/` | GLI3 ChIP-seq signal across the curated Gli3 limb-enhancer set. |
| Supplementary Figure S2 | `supp_virtual4c_gli3_hindlimb_hic_mm9/` and `supp_figs_submission_pdf/` | Promoter-centered Virtual 4C from E11.5 hindlimb Hi-C. |

The former Supplementary Figure S3 is not part of the current manuscript and is
retained only under `archive/` for provenance.

## Supplementary tables

The October supplementary workbook is Online Resource 2 (`ESM_2.xlsx`), to be included in the release-specific submission snapshot.

The September workbook remains at `supp_tables_submission_xlsx/Additional File 2.xlsx`.

| Table | Content |
|---|---|
| S1 | Histone-mark enhancer-wise quantification underlying Figure 2C |
| S2 | HOXA13/HOXD13 enhancer-wise signal underlying Figure 3C |
| S3 | GLI3 enhancer-wise signal underlying Supplementary Figure S1C |
| S4a | Promoter-centered Virtual 4C signal vector |
| S4b | mm9 enhancer coordinates used in the Virtual 4C overlay |
| S5 | p300/HAND2/PITX1 support-layer matrix |
| S6a | 54-enhancer locus-matched signal matrix (13 limb and 41 annotation-based VISTA comparison elements) |
| S6b | Class-level summaries |
| S7 | Single-layer AUC summary underlying Figure 5E |
| S8 | 54-enhancer × 9-layer rank-percentile matrix underlying Figure 4 |

## Exact submission snapshot

The directory `submission_assets/` preserves the September manuscript snapshot.
The October submission files will be stored in a separately identified,
checksum-verified release-specific directory.
