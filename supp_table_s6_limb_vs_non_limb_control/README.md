# Supplementary Table S6: locus-matched Gli3 enhancer signal comparison

This module contains Supplementary Table S6 materials for the revised Gli3 limb regulatory landscape manuscript.

Supplementary Table S6 compares 13 curated functionally supported Gli3 limb enhancers with 41 VISTA Gli3-region elements with reported non-limb activity and no limb annotation in the source records. These 41 elements form an annotation-based comparison set and are not experimentally established universal limb-negative controls.

- S6a provides enhancer-level signal values.
- S6b provides class-level summary statistics.

The analysis includes combined HOX13 signal, the descriptive H3K4me1 + H3K27ac signal sum, GLI3 signal, the PITX1 hindlimb-track average, and associated chromatin/transcription-factor measurements. The combined chromatin signal is not a functional enhancer-activity score or classifier. These measurements describe heterogeneity and overlap between the predefined enhancer groups.

Main files:
- `Supplementary Tables.xlsx`
- `Supplementary_Table_S6.xlsx`
- `Supplementary_Table_S6_limb_vs_non_limb_Gli3_control_analysis.tsv`

## HOXA13/HOXD13 track selection

The 54-enhancer comparison uses the matched mm10
CUT&RUN track pair `TableS2/tracks/HOXA13_mm10.bw`
and `TableS2/tracks/HOXD13_mm10.bw`, rather than the
Figure 3-specific mean tracks.

A historical processing note records that quantification
using the originally considered HOXA13 mean bigWig failed
with a zlib decompression error. The alternative matched
pair successfully yielded measurements for all 54 intervals.

The reported comparative values use the
`bigWigAverageOverBed` mean0 convention. These values
are not directly interchangeable with Figure 3-specific
mean-signal measurements.

See `../docs/HOX13_track_provenance.md` for the complete
verified provenance and limitations.
