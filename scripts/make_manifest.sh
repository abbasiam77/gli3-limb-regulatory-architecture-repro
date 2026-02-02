#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-manifest_fig1.tsv}"
echo -e "name\tsize_bytes\tmtime\tsha256" > "$OUT"

for f in *; do
  [[ -f "$f" ]] || continue
  sz=$(stat -c%s "$f")
  mt=$(stat -c%y "$f")
  # sha256 may be heavy for huge files; still ok. Skip .hic if needed.
  sha=$(sha256sum "$f" | awk '{print $1}')
  echo -e "$f\t$sz\t$mt\t$sha" >> "$OUT"
done

echo "Wrote $OUT"
