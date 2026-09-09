# Supplementary Table S5 supporting signal-layer reproducibility module

## Purpose

This module contains reproducibility assets underlying Supplementary Table S5,
which summarizes p300, HAND2 and PITX1 signal across the curated Gli3
limb-enhancer set.

These datasets are used as additional genomic context alongside the other
chromatin and transcription-factor layers analyzed in the study. They are not
treated as direct evidence of enhancer function, tissue specificity, regulatory
mechanism or causation.

Functional validation remains the anchor for enhancer identity.

## Relationship to the current supplementary tables

- **S1** — histone-mark quantification underlying Main Figure 2C
- **S2** — HOXA13/HOXD13 quantification underlying Main Figure 3C
- **S3** — GLI3 quantification underlying Supplementary Figure S1C
- **S4a/S4b** — promoter-centered Virtual 4C data and coordinates
- **S5** — p300/HAND2/PITX1 supporting signal layers
- **S6a/S6b** — validated limb versus non-limb enhancer comparison
- **S7** — single-layer AUC summary underlying Main Figure 5E
- **S8** — integrated rank-percentile matrix underlying Main Figure 4

The exact formatted current Supplementary Table S5 is included in the frozen
master workbook:

`../supp_tables_submission_xlsx/Additional File 2.xlsx`

## Contents overview

This module preserves:

- final and intermediate S5 exports;
- factor-specific `p300/`, `HAND2/` and `PITX1/` folders;
- enhancer BED files and metadata;
- track and value provenance;
- QC summaries;
- scripts used for data acquisition, conversion, quantification and table
  construction;
- supporting intermediate files retained for reproducibility.

## Folder guide

- `scripts/` — workflow scripts
- `p300/`, `HAND2/`, `PITX1/` — factor-specific metadata and quantification
  assets
- `shared_beds/` — enhancer BED files used in the workflow
- `shared_metadata/` — manifests and provenance metadata
- `shared_qc/` — QC summaries
- `tables/` — intermediate/supporting tables retained for provenance

## Interpretation

Signal enrichment in these bulk datasets is interpreted conservatively.
Presence or magnitude of a signal does not by itself establish limb enhancer
activity, direct transcription-factor binding at every element, enhancer-
promoter interaction, or regulatory function.
