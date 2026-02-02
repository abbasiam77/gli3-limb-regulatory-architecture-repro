# Fig 1 reproducibility package (GLI3 limb manuscript)

This repository snapshot contains the minimal figure-specific metadata and helper scripts needed to reproduce **Figure 1** visualization settings.

## Locked settings
- Genome build: **mm9**
- Locus: **chr13:12861604-16470132 (mm9)**
- Juicebox: **Observed**, **Balanced/KR**, **5 kb**
- IGV session: `docs/igv_session.xml`
- Enhancer naming: IGV session expects upstream enhancer bigWig as `Gli3_enhancers_gold-mm9.bw`

## What is included
- IGV session XML + enhancer BED (`docs/`)
- Figure settings (`config/fig1_params.yaml`)
- Source table for methods/caption (`docs/sources.tsv`)
- Manifest + SHA256 checksums (`manifests/`)
- Utility scripts (`scripts/`)

## What is not included
Large raw datasets (e.g., `*.bw`, `*.hic`) and final assembled figure binaries are not committed by default.
They can be retrieved from the listed GEO accessions and verified against the manifest checksums.
