#!/usr/bin/env bash
set -euo pipefail

IN="${1:-Gli3_named_enhancers.mm10.bed}"
echo "Input: $IN"

# bed4
awk 'BEGIN{OFS="\t"} $1!="track" {print $1,$2,$3,$4}' "$IN" > Gli3_named_enhancers.mm10.bed4

# add group from RGB (gold vs green)
awk 'BEGIN{OFS="\t"}
$1=="track"{next}
{
  rgb=$9
  group="unknown"
  if(rgb=="255,215,0") group="upstream"
  else if(rgb=="144,238,144") group="intronic"
  print $1,$2,$3,$4,group
}' "$IN" > Gli3_named_enhancers.mm10.with_group.bed

echo "Wrote:"
ls -lh Gli3_named_enhancers.mm10.bed4 Gli3_named_enhancers.mm10.with_group.bed
