#!/usr/bin/env bash
set -euo pipefail

# ----------------------------
# Virtual 4C extraction script
# ----------------------------
# Extracts an O/E (observed/expected) KR-normalized 10 kb Virtual 4C vector
# for the Gli3 promoter viewpoint against a wide chr13 window (mm9).
#
# Requirements:
# - Java
# - juicer_tools.jar (Juicer Tools v2+)
# - mm9 .hic file with KR norms at 10 kb (validated previously)
#
# Outputs:
# - outputs/virtual4c_vectors/gli3_virtual4c_OE_10kb_FULL_vector_WIDE.tsv
#
# Usage example:
#   ./scripts/extract_virtual4c_vector_from_hic.sh \
#     --hic /path/to/Hindlimb_mm9.hic \
#     --juicer /path/to/juicer_tools.jar
#

HIC=""
JAR=""

CHR="13"
BINSIZE=10000

# Gli3 promoter viewpoint bin (mm9)
VP1=15550000
VP2=15560000

# Wide window to include all enhancers (mm9)
START=14732034
END=16103316

OUTDIR="outputs/virtual4c_vectors"
OUTTMP_A="$OUTDIR/oe_region_vs_view.tsv"
OUTTMP_B="$OUTDIR/oe_view_vs_region.tsv"
OUTVEC="$OUTDIR/gli3_virtual4c_OE_10kb_FULL_vector_WIDE.tsv"

die () { echo "ERROR: $*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hic)    HIC="$2"; shift 2;;
    --juicer) JAR="$2"; shift 2;;
    --start)  START="$2"; shift 2;;
    --end)    END="$2"; shift 2;;
    --vp1)    VP1="$2"; shift 2;;
    --vp2)    VP2="$2"; shift 2;;
    --binsize) BINSIZE="$2"; shift 2;;
    *) die "Unknown argument: $1";;
  esac
done

[[ -n "$HIC" ]] || die "Missing --hic"
[[ -f "$HIC" ]] || die "Hi-C file not found: $HIC"
[[ -n "$JAR" ]] || die "Missing --juicer"
[[ -f "$JAR" ]] || die "juicer_tools.jar not found: $JAR"

mkdir -p "$OUTDIR"

echo "== Dump O/E (KR) at ${BINSIZE} bp bins =="
echo "HIC: $HIC"
echo "JAR: $JAR"
echo "chr${CHR}:${START}-${END}"
echo "viewpoint: chr${CHR}:${VP1}-${VP2}"

# Dump both orientations (defensive: some dumps return values in one orientation)
java -jar "$JAR" dump oe KR "$HIC" ${CHR}:${START}:${END} ${CHR}:${VP1}:${VP2} BP ${BINSIZE} "$OUTTMP_A"
java -jar "$JAR" dump oe KR "$HIC" ${CHR}:${VP1}:${VP2} ${CHR}:${START}:${END} BP ${BINSIZE} "$OUTTMP_B"

echo "== Build full contiguous vector (fill missing bins with 0) =="

python3 - <<PY
START=int("$START"); END=int("$END"); B=int("$BINSIZE")
VP1=int("$VP1")

vals = {}

def ingest(path):
    with open(path, "r") as f:
        for line in f:
            if not line.strip(): 
                continue
            a,b,v = line.split()
            a=int(a); b=int(b); v=float(v)
            # Identify which coordinate is the region coordinate
            if a == VP1 and b != VP1:
                vals[b] = v
            elif b == VP1 and a != VP1:
                vals[a] = v
            elif a == VP1 and b == VP1:
                vals[VP1] = v

ingest("$OUTTMP_A")
ingest("$OUTTMP_B")

# Emit vector for bins START..END stepping B (END treated as exclusive for bin start)
out_path = "$OUTVEC"
with open(out_path, "w") as out:
    n=0
    for x in range(START - (START % B), END, B):
        if x < START: 
            continue
        out.write(f"{x}\t{vals.get(x, 0.0)}\n")
        n += 1

print("Wrote:", out_path)
print("n_lines:", n)
print("first5:")
with open(out_path) as f:
    for i in range(5):
        print(f.readline().rstrip())
PY

echo "== Done =="
ls -lh "$OUTVEC"
