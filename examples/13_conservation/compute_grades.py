# Turn ChimeraX's continuous conservation score into ConSurf-style grades.
#
# ConSurf bins residues into nine grades by percentile, not by equal score
# width, because conservation scores are strongly skewed and equal-width
# bins put almost everything in one or two colors. Grade 1 is the most
# variable ninth, grade 9 the most conserved ninth.
#
# ChimeraX's "seq_conservation" is an information-theoretic score computed
# from the open alignment, not ConSurf's rate4site evolutionary rate. The
# grading scheme is the same; the underlying quantity is not. Say which
# one a figure used.
#
# Residues with no alignment column, or with too few aligned sequences to
# judge, get grade 0 and are drawn in neutral gray, matching ConSurf's
# "insufficient data" category.
#
# Run inside ChimeraX after the alignment is open and associated:
#     runscript compute_grades.py

import os
from chimerax.atomic import all_atomic_structures

MIN_COVERAGE = 0.5   # fraction of sequences that must be non-gap in a column
N_GRADES = 9

structure = all_atomic_structures(session)[0]
residues = [r for r in structure.residues if r.chain_id == "A" and r.polymer_type == 1]

scored, unscored = [], []
for r in residues:
    v = getattr(r, "seq_conservation", None)
    (scored if v is not None else unscored).append((r, v))

# Percentile bins: sort by score, cut into N_GRADES equal-count groups
scored.sort(key=lambda rv: rv[1])
n = len(scored)
grade = {}
for i, (r, _) in enumerate(scored):
    grade[r] = min(N_GRADES, int(i * N_GRADES / n) + 1)
for r, _ in unscored:
    grade[r] = 0

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "consurf_grade.defattr")
with open(out, "w") as f:
    f.write("attribute: consurfGrade\n")
    f.write("recipient: residues\n")
    f.write("match mode: any\n")
    for r in residues:
        f.write("\t/%s:%d\t%d\n" % (r.chain_id, r.number, grade[r]))

counts = {g: sum(1 for v in grade.values() if v == g) for g in range(N_GRADES + 1)}
session.logger.info(
    "wrote %s: %d residues graded, %d without data; per-grade counts %s"
    % (out, n, len(unscored), counts)
)
