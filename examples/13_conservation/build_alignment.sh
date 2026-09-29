#!/usr/bin/env bash
# Build a Cas9 ortholog alignment for the conservation figure.
#
# Fetches Cas9 family sequences from UniProt, keeps those close in length
# to SpCas9 (1368 aa) so the alignment is meaningful rather than a sea of
# gaps, puts SpCas9 first, and aligns with MAFFT.
#
# Conservation is a property of the sequence set, not of the protein. A
# set of close Streptococcus orthologs and a set spanning all type II
# systems give different answers, and both are "the conservation". State
# the set in the figure caption. This one is deliberately broad.
set -euo pipefail
cd "$(dirname "$0")"

SPCAS9=Q99ZW2
MIN=1200
MAX=1500

echo "fetching SpCas9 $SPCAS9"
curl -sf "https://rest.uniprot.org/uniprotkb/${SPCAS9}.fasta" -o spcas9.fasta

echo "fetching Cas9 family sequences"
curl -sf "https://rest.uniprot.org/uniprotkb/search?query=family:%22CRISPR-associated%20protein%20Cas9%20family%22&format=fasta&size=200" -o family_raw.fasta

echo "filtering to ${MIN}-${MAX} aa and dropping SpCas9 duplicates"
awk -v min=$MIN -v max=$MAX -v skip="$SPCAS9" '
  /^>/ { if (name != "" && length(seq) >= min && length(seq) <= max && name !~ skip)
           printf "%s\n%s\n", name, seq
         name = $0; seq = ""; next }
  { seq = seq $0 }
  END { if (name != "" && length(seq) >= min && length(seq) <= max && name !~ skip)
          printf "%s\n%s\n", name, seq }
' family_raw.fasta > family_filtered.fasta

cat spcas9.fasta family_filtered.fasta > cas9_set.fasta
echo "aligning $(grep -c '^>' cas9_set.fasta) sequences with mafft"
mafft --auto --quiet --thread -1 cas9_set.fasta > cas9_orthologs.afa

rm -f spcas9.fasta family_raw.fasta family_filtered.fasta cas9_set.fasta
echo "wrote cas9_orthologs.afa ($(grep -c '^>' cas9_orthologs.afa) sequences)"
