# Main Fig. 2 (mm9) reproducibility module

## Purpose
This module contains reproducibility assets for manuscript **Main Fig. 2**, focused on **mm9 hindlimb chromatin tracks, enhancer visualization, and enhancer-level signal quantification** around the *Gli3* regulatory landscape.

## Scope (current repository contents)
This module includes:
- IGV session files for panel generation (wide and zoom views)
- scripts used for Fig2C signal processing/replotting
- panel exports (Fig2A / Fig2B / Fig2C)
- supporting input/derived tables used for Fig2C quantification and plotting
- figure caption notes and manifest placeholders retained from project development

## Folder guide
- `inputs/` — source tables and IGV session XMLs used for panel setup/replotting
- `scripts/` — data processing and plotting scripts for Fig2C and related supporting outputs
- `outputs/panels/` — exported panel images (PNG/SVG) and final panel markers
- `tables/` — supporting Excel table(s) for Fig2C quantification
- `notes/` — caption drafts / project notes (lightly curated)
- `manifests/` — module-level manifest notes
- `config/` / `docs/` / `env/` — auxiliary files retained for reproducibility context

## Notes
This module was reorganized during repository-wide reviewer-facing cleanup.
Genome-build for Fig2 is mm9 (see repository-level coordinate/build policy).
