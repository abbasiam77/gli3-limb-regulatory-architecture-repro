# Release notes: reviewer-facing repository restructuring

**Date:** 2026-02-27  
**Repository:** `gli3-limb-regulatory-architecture-repro`

## Summary
This update reorganized the repository from a historical Fig1-era layout into a reviewer-friendly modular structure aligned with the current GLI3 limb manuscript scope.

## Major changes
- Renamed and reorganized top-level content into figure/supplement modules:
  - `01_main_fig1_mm9/`
  - `02_main_fig2_mm9/`
  - `03_main_fig3_mm10/`
  - `04_main_fig4/`
  - `supp_fig_gli3_chipseq_mm10_e11p5/`
  - `supp_virtual4c_gli3_hindlimb_hic_mm9/`
  - `supp_table_s5_phase1_support_layer/`
- Consolidated legacy Fig1-era generic folders into `01_main_fig1_mm9/`
- Removed placeholder/obsolete folders and empty placeholder directories
- Added/updated module READMEs and repo-wide documentation
- Added manuscript-ready main figure PDFs and supplementary figure/table bundles
- Added `docs/submission_assets_manifest.tsv`

## Scientific framing preserved
This restructuring was organizational/documentational only and did **not** alter the scientific framing or analytical conclusions. The following manuscript framing remains unchanged:
- architecture-first
- quantitative integrative
- conservative / non-causal interpretation
- S2 and S3 retained as source quantification tables
- S5 retained as extension support-layer table (no S6 introduced)

## Notes
The restructuring was designed to improve discoverability and usability for reviewers, editors, collaborators, and future reuse.
