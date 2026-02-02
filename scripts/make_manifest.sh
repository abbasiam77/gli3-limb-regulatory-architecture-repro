#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./make_manifest.sh /path/to/data_dir manifest_fig1.tsv
DIR="${1:-.}"
OUT="${2:-manifest.tsv}"

cd "$DIR"
echo -e "name\tsize_bytes\tmtime\tsha256" > "$OUT"

for f in *; do
  [[ -f "$f" ]] || continue
  sz=$(stat -c%s "$f")
  mt=$(stat -c%y "$f")
  sha=$(sha256sum "$f" | awk '{print $1}')
  echo -e "$f\t$sz\t$mt\t$sha" >> "$OUT"
done

echo "Wrote: $DIR/$OUT"
