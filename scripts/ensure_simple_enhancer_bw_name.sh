#!/usr/bin/env bash
set -euo pipefail

# Run this inside the folder that contains the BW files and igv_session.xml

MERGED="Gli3_enhancers_upstream_gold_MERGED.mm9.bw"
SIMPLE="Gli3_enhancers_gold-mm9.bw"

if [[ ! -f "$MERGED" ]]; then
  echo "ERROR: missing $MERGED"
  exit 1
fi

if [[ -f "$SIMPLE" ]]; then
  echo "OK: $SIMPLE already exists (size: $(stat -c%s "$SIMPLE") bytes)"
  exit 0
fi

cp -av "$MERGED" "$SIMPLE"
echo "Created $SIMPLE from $MERGED"
