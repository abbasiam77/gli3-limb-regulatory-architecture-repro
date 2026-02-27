#!/usr/bin/env bash
set -euo pipefail

BASE="/mnt/e/Amir Various research data_Oct 20th 2024/GLI3 review_Aug 2023/3D genome analysis stuff/Limbs/Publication work_june 2024/Re-Submission to Developmental Biology-Stuff"
ROOT="$BASE/05_phase1_enhancer_prioritization_TableS5"

CHROMS="$ROOT/shared_metadata/ucsc/mm9.chrom.sizes"
TMPDIR="$ROOT/tmp/wig_convert"
mkdir -p "$TMPDIR"

log() { echo "[$(date '+%F %T')] $*" | tee -a "$ROOT/logs/wig_to_bigwig_phase1.log"; }

convert_one() {
  local wig_gz="$1"
  local bw_out="$2"
  local tmp_wig="$TMPDIR/$(basename "${wig_gz%.gz}")"
  log "Converting $(basename "$wig_gz") -> $(basename "$bw_out")"
  gunzip -c "$wig_gz" > "$tmp_wig"
  wigToBigWig "$tmp_wig" "$CHROMS" "$bw_out"
  rm -f "$tmp_wig"
}

# p300
convert_one "$ROOT/p300/tracks/mm9/GSM348066_p300_wiggle.mm9.wig.gz" \
            "$ROOT/p300/tracks/mm9/GSM348066_p300_wiggle.mm9.bw"

# PITX1
convert_one "$ROOT/PITX1/tracks/mm9/GSM1019784_hl1_pitx1_chip.mm9.wig.gz" \
            "$ROOT/PITX1/tracks/mm9/GSM1019784_hl1_pitx1_chip.mm9.bw"
convert_one "$ROOT/PITX1/tracks/mm9/GSM1019786_hl2_pitx1_chip.mm9.wig.gz" \
            "$ROOT/PITX1/tracks/mm9/GSM1019786_hl2_pitx1_chip.mm9.bw"

# HAND2
convert_one "$ROOT/HAND2/tracks/mm9/GSM1342122_HAND2_LIMB_WT.mm9.wig.gz" \
            "$ROOT/HAND2/tracks/mm9/GSM1342122_HAND2_LIMB_WT.mm9.bw"
convert_one "$ROOT/HAND2/tracks/mm9/GSM1342121_HAND2_LIMB_3xF.mm9.wig.gz" \
            "$ROOT/HAND2/tracks/mm9/GSM1342121_HAND2_LIMB_3xF.mm9.bw"
convert_one "$ROOT/HAND2/tracks/mm9/GSM1447340_HAND2_LIMB_3xF_reproc.mm9.wig.gz" \
            "$ROOT/HAND2/tracks/mm9/GSM1447340_HAND2_LIMB_3xF_reproc.mm9.bw"

log "All WIG -> bigWig conversions completed"
