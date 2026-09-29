# Compute a per-residue quantity and write it as a ChimeraX attribute file.
#
# Here: the minimum distance from each SpCas9 residue to any nucleic-acid
# atom, which traces the nucleic-acid binding channel. Swap the calculation
# for whatever your data is (conservation, HDX protection, DMS score,
# crosslink count) and keep the rest.
#
# Run inside ChimeraX after opening a structure:
#     runscript compute_attribute.py
#
# The file format is documented at
# https://www.cgl.ucsf.edu/chimerax/docs/user/formats/defattr.html
# Data lines are TAB separated: <tab>atom-spec<tab>value

import os
import numpy
from chimerax.atomic import all_atomic_structures

structure = all_atomic_structures(session)[0]

nucleic = structure.atoms[structure.atoms.residues.polymer_types == 2]
protein_residues = [
    r for r in structure.residues if r.polymer_type == 1 and r.chain_id == "A"
]

nucleic_coords = nucleic.scene_coords

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dna_proximity.defattr")
with open(out, "w") as f:
    f.write("attribute: dnaProximity\n")
    f.write("recipient: residues\n")
    f.write("match mode: any\n")
    for r in protein_residues:
        d = numpy.linalg.norm(
            nucleic_coords[None, :, :] - r.atoms.scene_coords[:, None, :], axis=2
        )
        f.write("\t/%s:%d\t%.2f\n" % (r.chain_id, r.number, d.min()))

session.logger.info("wrote %s (%d residues)" % (out, len(protein_residues)))
