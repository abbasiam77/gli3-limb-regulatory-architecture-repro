# Gli3 limb regulatory genomics reproducibility repository

This repository provides figure-, table-, and analysis-oriented reproducibility
materials for a locus-resolved investigation of chromatin architecture,
transcription-factor occupancy, and chromatin signatures across regulatory
elements in the mouse Gli3 region.

## Associated manuscript

**Heterogeneous chromatin and transcription-factor signatures across functionally supported Gli3 limb enhancers in embryonic mouse limb**

Author: Amir Ali Abbasi

Target journal: Mammalian Genome

The study examines 13 curated Gli3 limb enhancers with prior in vivo functional
support. A locus-matched comparison includes 41 VISTA Gli3-region enhancers
with reported non-limb activity and no limb annotation in the source records.
These 41 elements constitute an annotation-based comparison set and are not
assumed to be experimentally established universal limb-negative controls.

Functional evidence anchors enhancer identity. Chromatin, transcription-factor,
and chromosome-contact measurements are interpreted as complementary,
correlative genomic context rather than proof of enhancer function or direct
regulatory mechanism.

The integrated analysis includes nine primary chromatin and transcription-factor
signal layers across 54 enhancers. Within-layer rank percentiles and empirical
AUC values describe molecular heterogeneity and overlap between the predefined
sets. The AUCs are descriptive and are not cross-validated estimates of
predictive performance.

## Main figure modules

- `01_main_fig1_mm9/` — Gli3 contact-domain visualization using mm9 Hi-C,
  architectural-protein tracks, and RNA-seq context.
- `02_main_fig2_mm9/` — histone-mark visualization and enhancer-wise
  H3K4me1/H3K27ac/H3K4me3 quantification.
- `03_main_fig3_mm10/` — HOXA13/HOXD13 visualization and enhancer-wise
  quantification.
- `04_main_fig4/` — integrated 54-enhancer, nine-layer rank-percentile heatmap.
- `05_main_fig5/` — locus-matched comparison of the 13 functionally supported
  limb enhancers with 41 annotation-based VISTA comparison elements,
  including empirical AUC summaries.

## Supplementary analysis modules

- `supp_fig_gli3_chipseq_mm10_e11p5/` — GLI3 ChIP-seq reanalysis supporting
  Supplementary Figure S1 and Table S3.
- `supp_virtual4c_gli3_hindlimb_hic_mm9/` — promoter-centered Virtual 4C
  supporting Supplementary Figure S2 and Tables S4a/S4b.
- `supp_table_s5_phase1_support_layer/` — p300, HAND2 and PITX1 supporting
  signal layers.
- `supp_table_s6_limb_vs_non_limb_control/` — source data and provenance for
  the 54-element locus-matched comparison.

Existing directory names are retained for workflow provenance. In particular,
the directory name containing `control` should not be interpreted as evidence
that the 41 comparison elements are experimentally established limb-negative
controls.

## October 2026 Mammalian Genome submission materials

The revised manuscript uses:

- Main Figures 1-5 and Main Tables 1-2.
- Online Resource 1 (`ESM_1.pdf`), containing Supplementary Figures S1-S2.
- Online Resource 2 (`ESM_2.xlsx`), containing Supplementary Tables S1-S8
  across ten data worksheets plus a README worksheet.

The October submission snapshot will be identified separately from the
September 2026 release. Historical supplementary bundles must not be assumed
to be identical to the October files.

## Historical releases and materials

The September 2026 release, `v2.0-Sep2026-manuscript`, represents the earlier
manuscript-associated reproducibility snapshot.

The previous submission assets remain part of that historical release.
Earlier Supplementary Figure S3 materials are retained under `archive/`
for provenance; their analyses are represented in the revised manuscript
by Main Figure 5 and Tables S6a/S6b/S7.

## Genome-build policy

Analyses are build-aware. Hi-C, architectural-protein, RNA-seq, histone-mark,
and Virtual 4C analyses use mm9 where appropriate to the source datasets.
HOXA13/HOXD13 and GLI3 ChIP-seq analyses use mm10. Coordinate conversions
and dataset-specific contexts are documented in the relevant modules.

## Reproducibility scope

The underlying genomic datasets are publicly available and are not
redistributed when unnecessary. This repository provides processed and
derived tables, analysis scripts, provenance documentation, QC information,
and figure-related resources supporting the study.

## Repository citation

Please cite the associated manuscript and the relevant version-specific
archived repository release. The October 2026 release identifiers will be
added only after the final release and Zenodo archive have been verified.
