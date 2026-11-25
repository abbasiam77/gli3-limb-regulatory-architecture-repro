# HOXA13/HOXD13 CUT&RUN track provenance

## Scope

This record distinguishes the processed mm10 HOXA13
and HOXD13 CUT&RUN tracks used in the manuscript's
Figure 3-specific analysis from those used for the
54-enhancer comparison (Supplementary Table S6,
Figures 4 and 5).

The biological source is wild-type E12.5 mouse distal
forelimb. Relevant HOXA13 samples are GSM5828329,
GSM5828330 and GSM5828331; HOXD13 samples are
GSM5828332, GSM5828333 and GSM5828334.

## Figure 3-specific processed tracks

Original external archive location:

`All source data file_GLI3_TAD_Publication/files/05_fig3_mm10/raw/`

- `HOXA13_mm10_WT_E12p5_DFL_mean.bw`
- `HOXD13_mm10_WT_E12p5_DFL_mean.bw`

The Figure 3-specific script
`03_main_fig3_mm10/scripts/make_Fig3C_WT_HOX13_table_scatter.py`
uses `pyBigWig.stats(..., type="mean", exact=True)`
to summarize these tracks over BED-defined enhancer
intervals. Its plotted coordinates use
log10(1 + mean signal).

## 54-enhancer comparative processed tracks

Original external archive location:

`All source data file_GLI3_TAD_Publication/files/TableS2/tracks/`

- `HOXA13_mm10.bw`
- `HOXD13_mm10.bw`

The comparative analysis uses
`bigWigAverageOverBed` interval summaries with mean0
values retained in Supplementary Table S6a.
The enhancer panel comprises 13 curated limb enhancers
and 41 VISTA comparison elements.

## Historical track-selection decision

The original analysis first considered the Figure 3
mean-signal tracks for the 54-enhancer comparison.
The HOXD13 mean bigWig quantified successfully, but
the HOXA13 mean bigWig produced a zlib decompression
error during `bigWigAverageOverBed` execution.

The analysis consequently selected the alternative
matched TableS2 HOXA13/HOXD13 track pair. Both
alternative tracks successfully produced 54
enhancer-interval measurements.

This decision is documented in the historical file
`08_notes/HOX13_track_choice_note.txt` under the
July-25th-BMC-Genomics-submission working directory.

## Verified SHA-256 fingerprints

| Analysis | Factor | SHA-256 |
| --- | --- | --- |
| Figure 3 | HOXA13 | `479068743bb8c212a18063e69b33d2866c0ab8c4d9728d4c564cc36b6e319958` |
| Figure 3 | HOXD13 | `2ddfbead4a703ca183ce4826d93e7027cf9eb1d9e4fabc26cdbff1b3d6c75117` |
| 54-enhancer comparison | HOXA13 | `5285cddb39d036263099b4bc2a07bf32a52c562698ae184c6db04ad5062da2b0` |
| 54-enhancer comparison | HOXD13 | `2daa880e16e92ff4c113cc723b853ff8577d24a59a0af97add1455493adf6979` |

These fingerprints were calculated from the surviving
processed bigWigs on the external G: archive.

## Numerical verification

The surviving comparative quantification outputs
contain 54 intervals for each factor. For
CNE14_hs1586_mm1977, they report:

- HOXA13 mean0: 23.9374
- HOXD13 mean0: 6.8588

Both tracks cover the full 1,119-bp interval for this
element, so mean and mean0 are equal for this interval.

## Reproducibility limits

The four processed bigWigs have distinct file hashes
and different signal coverage/summary characteristics.

The exact upstream track-generation procedures,
replicate-combination details, and normalization
differences between these track pairs have not been
independently reconstructed from the available
processing records.

Accordingly, the distinct processed tracks establish
different measurement provenance, but no specific
normalization procedure is asserted as the numerical
cause of the differences.

The processed bigWigs are retained in the original
external archive and are not distributed in this Git
repository. The historical track-selection record,
identities, and checksums are documented here.

No enhancer classifications, quantitative values,
figures, or statistical results are changed by this
provenance documentation.
