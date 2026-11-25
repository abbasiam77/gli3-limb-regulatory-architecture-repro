# Main Fig. 3 (mm10) reproducibility module

## Purpose
This module contains reproducibility assets for manuscript **Main Fig. 3**, focused on **mm10 HOXA13/HOXD13 occupancy visualization and enhancer-level quantification** across the *Gli3* locus.

## Scope (current repository contents)
This module includes:
- mm10 enhancer coordinate BED files (all/upstream/intronic/named sets)
- derived quantification tables used for Fig3B/Fig3C and supporting exports
- IGV sessions/snapshots for panel generation
- scripts used to build and replot Fig3C data/scatter outputs
- final panel exports for Fig3A/Fig3B/Fig3C
- source/provenance notes and checksums

## Folder guide
- `coords/` — mm10 enhancer coordinate sets used in Fig3 analyses
- `derived/` — processed/derived tables used for Fig3B/Fig3C and supplementary exports
- `scripts/` — data preparation and plotting scripts (especially Fig3C)
- `outputs/panels/` — final figure panel exports
- `igv/` — IGV sessions, snapshots, and track-range notes
- `docs/` — source notes / caption-support files
- `manifests/` — checksums and module-level provenance

## Notes
This module was reorganized during repository-wide reviewer-facing cleanup.
Fig3 is intentionally kept mm10-based (see repository-level coordinate/build policy).

## HOX13 signal provenance

Figure 3 uses mm10 HOXA13/HOXD13 CUT&RUN mean-signal
bigWigs (`HOXA13_mm10_WT_E12p5_DFL_mean.bw` and
`HOXD13_mm10_WT_E12p5_DFL_mean.bw`).
The Figure 3-specific quantification script calculates
exact interval means using pyBigWig.

The 54-enhancer comparison uses a different processed
HOX13 track pair. Absolute signal values from the two
analyses are therefore not directly interchangeable.
See `../docs/HOX13_track_provenance.md` for track identities,
fingerprints, historical selection rationale, and limitations.
