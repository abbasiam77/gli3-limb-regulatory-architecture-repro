# Fig 1 reproducibility package (GLI3 limb manuscript)

This folder contains the small, figure-specific configuration, scripts, and metadata needed to reproduce Fig 1 visualization choices.

## Locked settings
- Build: mm9
- Locus: chr13:12861604-16470132
- Juicebox: Observed, Balanced/KR, 5 kb
- IGV: see `docs/igv_session.xml`
- Enhancer track naming: IGV session expects `Gli3_enhancers_gold-mm9.bw` (created from the merged upstream BW)

## What is NOT stored here
Large raw tracks (e.g., `*.bw`, `*.hic`) are not committed to git by default. Use the manifest/checksums and public accession sources to retrieve them.

## Scripts
- `scripts/ensure_simple_enhancer_bw_name.sh` – ensures `Gli3_enhancers_gold-mm9.bw` exists
- `scripts/make_manifest.sh` – generates a TSV + SHA256 checksums in the current folder
- `scripts/archive_extras_fig1.sh` – archives intermediate/duplicate files
