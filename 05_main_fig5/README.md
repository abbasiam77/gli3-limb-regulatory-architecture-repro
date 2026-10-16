# Main Figure 5: locus-matched enhancer signal comparison

This module supports Main Figure 5 of the revised Mammalian Genome manuscript.

The analysis compares 13 curated functionally supported Gli3 limb enhancers
with 41 VISTA Gli3-region elements with reported non-limb activity and no
limb annotation in the source records.

The comparison elements are not experimentally established universal
limb-negative controls.

Panels a-d show selected signal distributions, and panel e summarizes
empirical area under the receiver operating characteristic curve (AUC)
values.

AUC values quantify separation between the two predefined enhancer groups
under a fixed limb-high signal direction. They are descriptive measures,
not cross-validated estimates of predictive performance.

The considerable overlap across groups supports cautious interpretation
of bulk chromatin and transcription-factor signals rather than claims of
functional classification or direct regulatory mechanism.

## Reproducibility files

- `outputs/final_pdf/Fig. 5.pdf` — figure-module output associated with the
  earlier manuscript configuration.
- `data/Supplementary_Table_S7_single_layer_AUC_summary.tsv` —
  single-layer AUC summary underlying panel e.

Enhancer-level and class-level values are provided in Supplementary
Tables S6a and S6b. The October formatted S6a/S6b/S7 tables are included
in Online Resource 2 (`ESM_2.xlsx`).

The verified October submission files will be included in a separate
release-specific snapshot.

The former Supplementary Figure S3 comparison is retained solely for
historical provenance under:

`../archive/legacy_supp_fig_s3_limb_vs_non_limb_control/`
