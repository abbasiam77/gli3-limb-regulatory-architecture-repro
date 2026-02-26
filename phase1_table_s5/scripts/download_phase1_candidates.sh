#!/usr/bin/env bash
set -euo pipefail

BASE="/mnt/e/Amir Various research data_Oct 20th 2024/GLI3 review_Aug 2023/3D genome analysis stuff/Limbs/Publication work_june 2024/Re-Submission to Developmental Biology-Stuff"
ROOT="$BASE/05_phase1_enhancer_prioritization_TableS5"

log() { echo "[$(date '+%F %T')] $*" | tee -a "$ROOT/logs/download_history_phase1.log"; }

mkdir -p "$ROOT"/{logs,tmp}
mkdir -p "$ROOT/p300"/{raw,tracks/mm9,peaks/mm9,logs}
mkdir -p "$ROOT/PITX1"/{raw,tracks/mm9,peaks/mm9,logs}
mkdir -p "$ROOT/HAND2"/{raw,tracks/mm9,tracks/mm10,peaks/mm9,peaks/mm10,logs}

# -----------------------------
# p300 (GSE13845 / GSM348066)
# -----------------------------
log "Downloading p300 processed files (GSM348066, E11.5 limb, mm9)"
wget -c -O "$ROOT/p300/tracks/mm9/GSM348066_p300_wiggle.mm9.wig.gz" \
  "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM348nnn/GSM348066/suppl/GSM348066_p300_wiggle.txt.gz"

wget -c -O "$ROOT/p300/peaks/mm9/GSM348066_p300_peaks.mm9.bed.gz" \
  "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM348nnn/GSM348066/suppl/GSM348066_p300_peaks.txt.gz"

# Optional aligned reads text (can be large; useful for provenance/debug)
wget -c -O "$ROOT/p300/raw/GSM348066_p300_aligned.txt.gz" \
  "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM348nnn/GSM348066/suppl/GSM348066_p300_aligned.txt.gz" || true

# Optional series RAW tar (heavy)
wget -c -O "$ROOT/p300/raw/GSE13845_RAW.tar" \
  "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE13nnn/GSE13845/suppl/GSE13845_RAW.tar" || true

# -----------------------------
# PITX1 (GSE41591 / GSM1019784 + GSM1019786)
# -----------------------------
log "Downloading PITX1 processed files (Rep1/Rep2, E11.5 hindlimb, mm9)"

# Rep1
wget -c -O "$ROOT/PITX1/tracks/mm9/GSM1019784_hl1_pitx1_chip.mm9.wig.gz" \
  "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1019nnn/GSM1019784/suppl/GSM1019784_hl1_pitx1_chip.wig.gz"

wget -c -O "$ROOT/PITX1/peaks/mm9/GSM1019784_hl1_pitx1_peaks.mm9.bed.gz" \
  "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1019nnn/GSM1019784/suppl/GSM1019784_hl1_pitx1_peaks.bed.gz"

wget -c -O "$ROOT/PITX1/peaks/mm9/GSM1019784_top_pitx1_peaks.mm9.bed.gz" \
  "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1019nnn/GSM1019784/suppl/GSM1019784_top_pitx1_peaks.bed.gz" || true

# Rep2
wget -c -O "$ROOT/PITX1/tracks/mm9/GSM1019786_hl2_pitx1_chip.mm9.wig.gz" \
  "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1019nnn/GSM1019786/suppl/GSM1019786_hl2_pitx1_chip.wig.gz"

wget -c -O "$ROOT/PITX1/peaks/mm9/GSM1019786_hl2_pitx1_peaks.mm9.bed.gz" \
  "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1019nnn/GSM1019786/suppl/GSM1019786_hl2_pitx1_peaks.bed.gz"

# Optional series RAW tar (heavy)
wget -c -O "$ROOT/PITX1/raw/GSE41591_RAW.tar" \
  "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE41nnn/GSE41591/suppl/GSE41591_RAW.tar" || true

# -----------------------------
# HAND2 (GSE55707) - start with series tar (candidate)
# -----------------------------
log "Downloading HAND2 GSE55707 series RAW tar (candidate; inspect contents next)"
wget -c -O "$ROOT/HAND2/raw/GSE55707_RAW.tar" \
  "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE55nnn/GSE55707/suppl/GSE55707_RAW.tar" || true

log "Download script completed"
