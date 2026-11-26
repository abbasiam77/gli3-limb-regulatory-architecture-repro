# Main Figure 4: integrated enhancer-signal heatmap

This module supports Main Figure 4 of the revised manuscript:

**Heterogeneous chromatin and transcription-factor signatures across
functionally supported Gli3 limb enhancers in embryonic mouse limb**

Target journal: Mammalian Genome.

Main Figure 4 presents an integrated within-layer rank-percentile view of
nine chromatin and transcription-factor signal layers across 54 Gli3-region
enhancer elements.

The analysis comprises 13 curated functionally supported Gli3 limb enhancers
and 41 VISTA Gli3-region comparison elements with reported non-limb activity
and no limb annotation in the source records.

The 41 elements are an annotation-based comparison group and are not assumed
to be experimentally established universal limb-negative controls.

Signal ranks describe relative position within each genomic layer.
The unweighted mean percentile is used only for heatmap row ordering and is
not interpreted as enhancer activity or predictive performance.

Functional evidence anchors enhancer identity. The molecular signals provide
correlative genomic context rather than direct evidence of function or
regulatory mechanism.

## Reproducibility files

- `outputs/final_pdf/Fig. 4.pdf` — figure-module output associated with the
  earlier manuscript configuration.
- `data/Supplementary_Table_S8_integrated_rank_percentile_matrix.tsv` —
  54-enhancer by 9-layer rank-percentile matrix underlying Figure 4.

For the October 2026 Mammalian Genome submission, the corresponding formatted
table is Supplementary Table S8 in Online Resource 2 (`ESM_2.xlsx`).

The verified October submission files will be provided in a separate
release-specific snapshot. Historical module outputs are retained for
reproducibility and provenance.

## November 2026 vector Figure 4 reproduction

The final Figure 4 submitted with the Mammalian Genome manuscript is
generated directly from the 54-enhancer by 9-layer numerical matrix
in Supplementary Table S8, without image-generation software.

### Reproduction files

- `data/Fig4_TableS8_source.csv` — plotting-ready export of
  Supplementary Table S8.
- `scripts/build_fig4_from_S8.py` — Python plotting script.
- `../submission_assets/main_figures/Figure_4.pdf` — final submitted
  vector PDF.
- `outputs/reproduced/` — locally generated verification outputs
  (not required for archival).

The pre-existing `outputs/final_pdf/Fig. 4.pdf` is retained as a
historical figure-module output and is not the updated submission PDF.

### Software environment

The final figure was reproduced under Ubuntu WSL with:

- Python 3.12.3
- NumPy 1.26.4
- Matplotlib 3.6.3

### Reproduction command

Run from the repository root:

```bash
python3 04_main_fig4/scripts/build_fig4_from_S8.py
```

The script reads `04_main_fig4/data/Fig4_TableS8_source.csv`
and writes:

- `04_main_fig4/outputs/reproduced/Fig4_S8_Vector_Final.pdf`
- `04_main_fig4/outputs/reproduced/Fig4_S8_Vector_Preview.png`

The input data were compared with the existing repository TSV:
all 54 enhancer identities, row ordering, 54 class assignments,
486 signal-layer values, and 54 mean percentiles matched.
The CNE14/hs1586/mm1977 identifier uses equivalent naming conventions
between the two input files.

The plot uses within-layer rank percentiles and does not imply
causal enhancer activity or regulatory mechanism.
