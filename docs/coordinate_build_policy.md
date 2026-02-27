# Coordinate / genome-build policy

This repository contains modules generated from datasets aligned to different genome builds (primarily mm9 and mm10), reflecting the original source datasets and analysis requirements.

## General principle
Build usage is preserved according to source-data provenance and intended analysis context, rather than forcing all modules into a single build.

## Module-level summary
- `01_main_fig1_mm9/` — mm9-centered context
- `02_main_fig2_mm9/` — mm9-centered context
- `03_main_fig3_mm10/` — mm10-centered HOX13 occupancy context
- `supp_virtual4c_gli3_hindlimb_hic_mm9/` — mm9
- `supp_fig_gli3_chipseq_mm10_e11p5/` — mm10
- `supp_table_s5_phase1_support_layer/` — mixed support workflow (includes mm10 enhancer sets and mm9 lifted/quantified variants where applicable)

## Recommendation for reuse
When reusing files, always verify the genome build from the module README and/or file names before combining tracks or coordinates across modules.
