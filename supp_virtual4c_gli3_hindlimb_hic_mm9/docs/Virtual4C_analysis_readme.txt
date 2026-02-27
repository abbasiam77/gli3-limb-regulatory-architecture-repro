
# Virtual 4C Analysis and Manuscript Updates: Gli3 Promoter and Enhancer Interactions

## Introduction
In the course of addressing the reviewer comments for the manuscript titled "Redundant enhancer networks and 3D chromatin architecture stabilize Gli3 regulation during limb development", the Virtual 4C analysis was performed to better understand the spatial interactions of the Gli3 promoter with its associated enhancers in the mouse hindlimb. The following document outlines the steps taken, technical details, interpretations, and how this analysis integrates with the manuscript.

## Key Outcomes
1. **Virtual 4C Construction:**
   - A **Virtual 4C profile** was constructed using Hi-C data for E11.5 hindlimb (mm9 build).
   - **Gli3 promoter viewpoint** (chr13:15,550,000–15,560,000) was chosen as the center of contact analysis.
   - The **contact frequency** was plotted between the Gli3 promoter bin and other bins across the regulatory region.
   - The analysis supports **long-range regulatory communication**, although no discrete **enhancer–promoter loops** were observed at the resolution of this dataset (10 kb).

2. **Technical Steps Taken:**
   - **Data Preprocessing:**
     - A corrected BED file (`gli3_enhancers_mm10_from_TableS1.bed`) was used to update enhancer coordinates.
     - **Liftover** was performed to convert mm10 coordinates to mm9 for compatibility with the Hi-C data.
   - **JuicerTools** was used to extract **Hi-C interaction data** from the `tracks/Hindlimb_mm9.hic` file at 10 kb resolution.
   - The **contact profile** was generated for the region containing Gli3-associated enhancers.
   - **Virtual 4C Vector**:
     - The interaction frequency was extracted for each 10 kb bin across the Gli3 regulatory interval.
     - The **enhancer tick marks** were placed on the plot to show enhancer locations across the region.

3. **Enhancer Marking & Plot Preparation:**
   - The **Virtual 4C figure** was generated with tick marks for Gli3-associated enhancers (mm9 coordinates).
   - Two figure versions were created:
     - **With enhancer tick marks** for a more detailed view.
     - **Curve-only** for a cleaner, broader overview.
   - Both figures were saved as **PNG** and **PDF** formats for submission.

## Interpretation and Framing for Manuscript Updates
1. **Resolution Limitations & Claim Adjustments:**
   - The Virtual 4C profile confirms **broad promoter-centered interactions** across the Gli3 regulatory interval but does not resolve discrete **enhancer–promoter loops**.
   - The resolution of **10 kb** and population-averaged **Hi-C** data do not support claims of **specific enhancer–promoter contacts**.
   - These findings support the **concept of a permissive 3D chromatin environment** for Gli3 regulation but do not provide definitive evidence for direct looping interactions.

2. **Key Manuscript Changes:**
   - In the **Results** section, we revised the discussion on **enhancer–promoter interactions** to ensure that claims are **supported by data**. We emphasize the **lack of specific loops** at the resolution of this study.
   - We explicitly included the following framing:
     - "The Virtual 4C analysis shows broad promoter-centered interactions across the Gli3 locus, but resolution limits prevent assigning specific enhancer–promoter loops."

3. **Enhancer Labels and Figure Legend:**
   - The **enhancers** in the **figure** were labeled with tick marks for clarity and were listed in the figure legend.
   - The updated **figure legend** emphasizes the **virtual 4C limitations** and frames the results within the **context of chromatin domain organization**.

## Files Provided for Submission:
1. **Supplementary Figure Sx**:
   - **Virtual 4C plot (10 kb resolution)** showing Gli3 promoter-centered contact profile.
     - Available in **PNG** and **PDF** formats:
       - [Virtual 4C Figure (ticks)](sandbox:/mnt/data/SuppFig_Virtual4C_Gli3_promoter_mm9_10kb_UNLABELED_ticks.png)
       - [Virtual 4C Figure (curve-only)](sandbox:/mnt/data/SuppFig_Virtual4C_Gli3_promoter_mm9_10kb_UNLABELED_curveonly.png)
   - **Figure Legend**: Describes the virtual 4C analysis, highlighting broad promoter contacts but acknowledging the lack of resolution for definitive looping conclusions.

2. **Updated Table S2**: 
   - **Table of enhancer marks and signals** with the inclusion of the previously missing CNE11 enhancer.
     - [Table S2 (with CNE11)](sandbox:/mnt/data/Table_S2_signal_summary_FINAL_corrected_mm10_with_CNE11_UPDATED_legend.xlsx)

3. **Virtual 4C Data**:
   - **Raw Virtual 4C data** (from the `out/gli3_virtual4c_vector_10000.tsv` file) used to generate the plots.
     - [Virtual 4C data](sandbox:/mnt/data/gli3_virtual4c_vector_10000.tsv)
   - **Enhancer Coordinates** (from `work/gli3_enhancers_mm9.bed.gz`).
     - [Enhancer Coordinates](sandbox:/mnt/data/gli3_enhancers_mm9.bed.gz)

## Conclusion
By addressing the **resolution limitations** and correcting the **enhancer looping claims**, we have ensured that the results presented in the manuscript are both **accurate and clearly framed**. The Virtual 4C analysis, along with the newly generated Supplementary Figure, supports the concept of **long-range chromatin interactions** while remaining cautious about over-interpreting the data.

