#!/usr/bin/env bash
set -euo pipefail

ARCH="archive_$(date +%Y%m%d)_fig1_cleanup"
mkdir -p "$ARCH"

# Edit this list if you add more intermediates later
cat > archive_list.txt << 'EOL'
Gli3_enhancers_mm9_BED9_itemRgbOn_VIS3_score1000_NAMES_noCNE6.bed
Gli3_enhancers_upstream_gold.mm9.bw
Gli3_enhancers_upstream_gold.mm9.v2.bw
Gli3_intronic_green.mm9.bedGraph
Gli3_upstream_gold.mm9.bedGraph
upstream_gold.merged.bed
upstream_gold.merged.bedGraph
upstream_gold.sorted.bed
EOL

ls -lah > "$ARCH/inventory_before.txt"
: > "$ARCH/move_log.txt"

while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  if [[ -e "$f" ]]; then
    mv -vn -- "$f" "$ARCH/" | tee -a "$ARCH/move_log.txt"
  else
    echo "missing: $f" | tee -a "$ARCH/move_log.txt"
  fi
done < archive_list.txt

ls -lah > "$ARCH/inventory_after.txt"
echo "Archived into: $ARCH"
