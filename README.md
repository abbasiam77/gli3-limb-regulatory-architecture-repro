# GLI3 limb regulatory architecture reproducibility repository

This repository contains figure- and supplement-oriented reproducibility assets for a **GLI3 limb manuscript resubmission** (Developmental Biology), organized for reviewer-friendly navigation. The project is framed as an **architecture-first, quantitative integrative**, and **conservatively interpreted** analysis of the GLI3 regulatory landscape in mouse limb development.

## Repository design (reviewer-facing)
The repository is organized into self-contained modules corresponding to manuscript main figures and selected supplementary analyses/tables.

### Main figure modules
- `01_main_fig1_mm9/` — Main Fig. 1 reproducibility assets (mm9 context)
- `02_main_fig2_mm9/` — Main Fig. 2 reproducibility assets (mm9 histone/enhancer views and quantification support)
- `03_main_fig3_mm10/` — Main Fig. 3 reproducibility assets (mm10 HOX13 occupancy and quantification)

### Supplementary modules
- `supp_fig_gli3_chipseq_mm10_e11p5/` — Supplementary GLI3 ChIP-seq figure bundle (mm10, E11.5 limb)
- `supp_virtual4c_gli3_hindlimb_hic_mm9/` — Supplementary Virtual 4C module (hindlimb Hi-C, mm9, GLI3 promoter viewpoint)
- `supp_table_s5_phase1_support_layer/` — Supplementary Table S5 (p300/HAND2/PITX1 extension support-layer workflow)

### Repository-wide documentation
- `docs/repo_map.md` — quick module map and navigation notes
- `docs/coordinate_build_policy.md` — mm9/mm10 build usage and conversion policy
- `docs/manuscript_figure_table_mapping.md` — mapping between manuscript items and repository modules/files

## Manuscript framing preserved in this repository
- **Architecture-first**
- **Quantitative integrative**
- **Conservative / non-causal language**
- **S2** = HOX13 quantification source table
- **S3** = GLI3 quantification source table
- **S5** = p300/HAND2/PITX1 extension support-layer table
- **No S6** integrated master prioritization table at this stage

## Genome build policy (summary)
This project intentionally uses a mixed-build strategy based on data provenance and analysis needs:
- Some modules are mm9-based (e.g., Hi-C/histone display contexts)
- Some modules are mm10-based (e.g., HOX13 occupancy analyses)

Please see `docs/coordinate_build_policy.md` for details and rationale.

## Reproducibility scope
This repository focuses on:
- scripts
- processed/derived tables
- panel exports
- metadata/manifests/provenance notes
- selected frozen BED inputs

Large raw sequencing files and full external datasets are not necessarily mirrored here and should be obtained from the corresponding public sources/accessions documented within module-level files.

## Notes for reviewers/readers
If you are reviewing a specific figure or supplementary item, start with the corresponding module README. Each module is organized to keep scripts, outputs, and provenance close together.

## Status
Repository structure has been reorganized for reviewer-facing clarity during final manuscript preparation/resubmission.

## Manuscript-ready submission asset bundles
For reviewer/editor convenience, final manuscript-ready PDFs/XLSX files are also grouped here:
- `supp_figs_submission_pdf/` — supplementary figure PDFs
- `supp_tables_submission_xlsx/` — supplementary table Excel files
- Main figure PDFs are placed in each corresponding main figure module under `outputs/final_pdf/`
