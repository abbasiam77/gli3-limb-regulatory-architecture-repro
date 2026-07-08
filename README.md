# Gli3 limb regulatory architecture reproducibility repository

This repository contains figure- and supplement-oriented reproducibility assets for an integrative analysis of the mouse Gli3 limb regulatory landscape.

The revised manuscript emphasizes that functionally validated Gli3 limb enhancers are molecularly heterogeneous across chromatin and transcription-factor layers. It also includes a control comparison showing that validated non-limb enhancers from the broader Gli3 region can show overlapping bulk epigenomic and transcription-factor signal profiles. These results support cautious multi-layer interpretation of enhancer-associated signals rather than classification from any single dataset alone.

## Repository organization

Main figure modules:

- `01_main_fig1_mm9/` — Gli3 contact-domain visualization using mm9 Hi-C, architectural-protein tracks and RNA-seq context.
- `02_main_fig2_mm9/` — histone-mark visualization and enhancer-wise H3K4me1/H3K27ac/H3K4me3 quantification.
- `03_main_fig3_mm10/` — HOXA13/HOXD13 visualization and enhancer-wise HOX13 quantification.
- `04_main_fig4/` — schematic model linking Gli3 contact-domain organization, enhancer redundancy and limb regulatory robustness.

Supplementary figure/table modules:

- `supp_fig_gli3_chipseq_mm10_e11p5/` — GLI3 ChIP-seq reanalysis supporting Supplementary Figure S1 and Supplementary Table S3.
- `supp_virtual4c_gli3_hindlimb_hic_mm9/` — promoter-centered Virtual 4C analysis supporting Supplementary Figure S2 and Supplementary Table S4a,b.
- `supp_table_s5_phase1_support_layer/` — p300, HAND2 and PITX1 occupancy-support analysis supporting Supplementary Table S5.
- `supp_table_s6_limb_vs_non_limb_control/` — control comparison of curated Gli3 limb enhancers and validated non-limb Gli3-region enhancers supporting Supplementary Table S6a,b.
- `supp_fig_s3_limb_vs_non_limb_control/` — visual summary of the limb versus non-limb control comparison supporting Supplementary Figure S3.

Submission-ready bundles:

- `supp_figs_submission_pdf/` — manuscript-ready Supplementary Figures S1-S3.
- `supp_tables_submission_xlsx/` — manuscript-ready combined Supplementary Tables workbook containing S1-S6.
- `docs/` — repository navigation, coordinate/build notes and manuscript figure/table mapping documents.

## Data scope

No new sequencing data are deposited in this repository. The study re-analyzes publicly available datasets from GEO, SRA/ENA mirrors where needed, UCSC resources, and VISTA enhancer annotations. Large raw public datasets should be retrieved from the accessions listed in the manuscript and accompanying documentation.

Derived figure files, supplementary tables, scripts, metadata and selected intermediate outputs are provided here to support reproducibility of the manuscript-level analyses.

## Genome-build policy

Analyses are build-aware. Main histone, architectural-protein, RNA-seq, Hi-C and Virtual 4C analyses are presented in mm9 where required by the processed Hi-C and track context. HOXA13/HOXD13 and GLI3 ChIP-seq analyses are presented in mm10 where required by their source datasets. Build-specific coordinate handling and liftOver steps are documented in the relevant modules.
