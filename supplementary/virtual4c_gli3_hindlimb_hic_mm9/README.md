# Virtual 4C (Hi-C) — Gli3 promoter viewpoint — E11.5 hindlimb (mm9)

This folder contains the reproducible inputs/outputs used to generate the Virtual 4C supplementary figure for the Gli3 locus in the manuscript:
“Redundant enhancer networks and 3D chromatin architecture stabilize Gli3 regulation during limb development.”

## Source Hi-C dataset
- Tissue/stage: mouse hindlimb bud, E11.5
- Genome build: NCBI37/mm9
- File used locally: `tracks/Hindlimb_mm9.hic` (not stored in this repo due to size)
- Normalization: KR (Balanced)
- Resolution: 10 kb bins

## Viewpoint (Gli3 promoter bin)
- Bin size: 10 kb
- Viewpoint coordinates (mm9): chr13:15,550,000–15,560,000
- Interpretation: bin containing the Gli3 promoter/TSS (used as the Virtual 4C anchor)

## Region plotted (WIDE)
- mm9 coordinates: chr13:14,732,034–16,103,316
This window was chosen to include the full upstream region containing all curated Gli3-associated limb enhancers plus intronic elements.

## Enhancer annotations
Enhancer coordinates used for tick marks are in:
- `inputs/gli3_enhancers_mm9.bed` (and `.bed.gz`)

Two figure variants are stored:
- Labeled version with enhancer names for internal interpretation.
- Final clean version (no labels; CNE6 excluded as non-conserved in mouse).

## Outputs
### Figures
`outputs/figures/`
- `SuppFig_Virtual4C_Gli3_promoter_mm9_10kb_OE_WIDE_LABELED_v2.(png/pdf)`
- `SuppFig_Virtual4C_Gli3_promoter_mm9_10kb_OE_WIDE_NOlabels_noCNE6_lightGreenIntronic.(png/pdf)`

### Virtual 4C vector table
`outputs/virtual4c_vectors/`
- `gli3_virtual4c_OE_10kb_FULL_vector_WIDE.tsv`
This table is the plotted y-value series (O/E) for successive 10 kb bins across the region.

## Scripts
`scripts/`
- `plot_virtual4c_oe.py`
- `plot_virtual4c_oe_labeled.py`
- `plot_virtual4c_oe_labeled_v2.py`
- `plot_virtual4c_oe_labeled_v3_nolabels.py`

## Reproducibility (high level)
1. Use `juicer_tools dump oe KR` at 10 kb to extract O/E values between the viewpoint bin and the region.
2. Convert dump output to a continuous vector across the chosen window.
3. Plot the vector and optionally overlay enhancer tick marks from the mm9 BED file.

See `MANIFEST.tsv` for checksums of the exact files cited.
