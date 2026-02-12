#!/usr/bin/env bash
set -euo pipefail

# GLI3 ChIP-seq processing: SRR FASTQ -> BAM -> CPM bigWig -> log2(ChIP/Input) bigWig
#
# Usage (example):
#   bash 01_srr_to_log2_bigwig.sh \
#     --workdir /mnt/e/.../Supp-Fig-Gli3_ChipSeq/work_mm10 \
#     --genome mm10 \
#     --bowtie2_index /path/to/bowtie2/index/prefix \
#     --chip_srr "SRR11907926,SRR11907927,SRR11907928" \
#     --input_bam /path/to/input_merged.bam \
#     --threads 8
#
# Notes:
# - This script assumes SINGLE-END SRR runs unless you pass paired FASTQs manually.
# - It requires: sra-tools (prefetch,fasterq-dump), bowtie2, samtools, deepTools (bamCoverage,bigwigCompare)

WORKDIR=""
GENOME="mm10"
BOWTIE2_INDEX=""
CHIP_SRR_CSV=""
INPUT_BAM=""
THREADS=8

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workdir) WORKDIR="$2"; shift 2;;
    --genome) GENOME="$2"; shift 2;;
    --bowtie2_index) BOWTIE2_INDEX="$2"; shift 2;;
    --chip_srr) CHIP_SRR_CSV="$2"; shift 2;;
    --input_bam) INPUT_BAM="$2"; shift 2;;
    --threads) THREADS="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 1;;
  esac
done

if [[ -z "$WORKDIR" || -z "$BOWTIE2_INDEX" || -z "$CHIP_SRR_CSV" || -z "$INPUT_BAM" ]]; then
  echo "ERROR: missing required args. Need --workdir --bowtie2_index --chip_srr --input_bam" >&2
  exit 1
fi

mkdir -p "$WORKDIR"/{raw/sra,raw/fastq,processed/bam,processed/bw,logs,tmp}
LOG="$WORKDIR/logs/pipeline_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

echo "== GLI3 ChIP pipeline started =="
echo "WORKDIR=$WORKDIR"
echo "GENOME=$GENOME"
echo "BOWTIE2_INDEX=$BOWTIE2_INDEX"
echo "CHIP_SRR=$CHIP_SRR_CSV"
echo "INPUT_BAM=$INPUT_BAM"
echo "THREADS=$THREADS"
echo "Log: $LOG"
echo

# Basic tool checks
command -v bowtie2 >/dev/null || { echo "Missing bowtie2"; exit 1; }
command -v samtools >/dev/null || { echo "Missing samtools"; exit 1; }
command -v prefetch >/dev/null || { echo "Missing sra-tools prefetch"; exit 1; }
command -v fasterq-dump >/dev/null || { echo "Missing sra-tools fasterq-dump"; exit 1; }
command -v bamCoverage >/dev/null || { echo "Missing deepTools bamCoverage"; exit 1; }
command -v bigwigCompare >/dev/null || { echo "Missing deepTools bigwigCompare"; exit 1; }

IFS=',' read -r -a CHIP_SRR <<< "$CHIP_SRR_CSV"

download_and_fastq () {
  local SRR="$1"
  local SRA_DIR="$WORKDIR/raw/sra"
  local FQ_DIR="$WORKDIR/raw/fastq"
  local TMP_DIR="$WORKDIR/tmp/${SRR}"
  mkdir -p "$TMP_DIR"

  echo "---- $SRR: prefetch ----"
  prefetch -O "$SRA_DIR" "$SRR"

  echo "---- $SRR: fasterq-dump ----"
  fasterq-dump -e "$THREADS" -O "$FQ_DIR" -t "$TMP_DIR" "$SRA_DIR/$SRR"

  # Most SRA single-end runs become ${SRR}.fastq
  if [[ -f "$FQ_DIR/${SRR}.fastq" ]]; then
    echo "FASTQ: $FQ_DIR/${SRR}.fastq"
  else
    echo "WARNING: expected $FQ_DIR/${SRR}.fastq not found. Listing:"
    ls -lh "$FQ_DIR" | grep "$SRR" || true
  fi
}

align_single_end () {
  local SRR="$1"
  local FQ="$WORKDIR/raw/fastq/${SRR}.fastq"
  local BAM_OUT="$WORKDIR/processed/bam/${SRR}.sorted.bam"

  echo "---- $SRR: bowtie2 align (single-end) ----"
  bowtie2 -x "$BOWTIE2_INDEX" -U "$FQ" -p "$THREADS" \
    | samtools view -bS - \
    | samtools sort -@ "$THREADS" -o "$BAM_OUT" -

  samtools index "$BAM_OUT"
  echo "BAM: $BAM_OUT"
}

echo "== Step 1: Download + FASTQ =="
for SRR in "${CHIP_SRR[@]}"; do
  download_and_fastq "$SRR"
done

echo "== Step 2: Align + sort/index each replicate =="
for SRR in "${CHIP_SRR[@]}"; do
  align_single_end "$SRR"
done

echo "== Step 3: Merge replicates =="
MERGED_BAM="$WORKDIR/processed/bam/GLI3_E115_ChIP_merged.${GENOME}.bam"
samtools merge -@ "$THREADS" -f "$MERGED_BAM" \
  $(printf "%q " "$WORKDIR/processed/bam/"*.sorted.bam)
samtools sort -@ "$THREADS" -o "${MERGED_BAM%.bam}.sorted.bam" "$MERGED_BAM"
mv -f "${MERGED_BAM%.bam}.sorted.bam" "$MERGED_BAM"
samtools index "$MERGED_BAM"
rm -f "$WORKDIR/processed/bam/"*.sorted.bam "$WORKDIR/processed/bam/"*.sorted.bam.bai 2>/dev/null || true
echo "Merged BAM: $MERGED_BAM"

echo "== Step 4: CPM bigWigs (bin=25) =="
CHIP_BW="$WORKDIR/processed/bw/GLI3_E115_ChIP_merged.${GENOME}.CPM.bin25.bw"
INPUT_BW="$WORKDIR/processed/bw/Input_E115.${GENOME}.CPM.bin25.bw"

bamCoverage -b "$MERGED_BAM" -o "$CHIP_BW" --binSize 25 --normalizeUsing CPM -p "$THREADS"
bamCoverage -b "$INPUT_BAM"  -o "$INPUT_BW" --binSize 25 --normalizeUsing CPM -p "$THREADS"

echo "ChIP CPM BW: $CHIP_BW"
echo "Input CPM BW: $INPUT_BW"

echo "== Step 5: log2(ChIP/Input) bigWig =="
LOG2_BW="$WORKDIR/processed/bw/GLI3_log2ChIPoverInput.${GENOME}.bin25.skipNAs.bw"

bigwigCompare -b1 "$CHIP_BW" -b2 "$INPUT_BW" \
  --operation log2 --skipNonCoveredRegions \
  -o "$LOG2_BW" -p "$THREADS"

echo "log2 BW: $LOG2_BW"
echo "== DONE =="
