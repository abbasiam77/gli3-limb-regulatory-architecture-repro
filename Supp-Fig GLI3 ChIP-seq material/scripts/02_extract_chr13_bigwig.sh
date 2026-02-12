#!/usr/bin/env bash
set -euo pipefail

# Extract chr13 region to make smaller bigWigs for IGV sharing.
# Requires UCSC bigWigToBedGraph + bedGraphToBigWig OR deepTools bigwigCompare is not enough here.
# Alternative: keep full bigWig and just document the locus.

BW_IN="${1:-}"
CHROMSIZES="${2:-}"
OUT_PREFIX="${3:-chr13_only}"

if [[ -z "$BW_IN" || -z "$CHROMSIZES" ]]; then
  echo "Usage: bash 02_extract_chr13_bigwig.sh <in.bw> <chrom.sizes> <out_prefix>" >&2
  exit 1
fi

command -v bigWigToBedGraph >/dev/null || { echo "Missing bigWigToBedGraph (UCSC)"; exit 1; }
command -v bedGraphToBigWig >/dev/null || { echo "Missing bedGraphToBigWig (UCSC)"; exit 1; }

TMP="${OUT_PREFIX}.chr13.bedGraph"
OUT="${OUT_PREFIX}.chr13.bw"

bigWigToBedGraph "$BW_IN" /dev/stdout \
  | awk '$1=="chr13"{print}' > "$TMP"

bedGraphToBigWig "$TMP" "$CHROMSIZES" "$OUT"
rm -f "$TMP"

echo "Wrote: $OUT"
