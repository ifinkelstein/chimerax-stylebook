# Per-residue displacement vectors, the "porcupine plot", done carefully.
#
# One small arrow per residue, drawn at the Calpha, pointing from where
# that residue sits in the start state to where it sits in the end state.
#
# The published version of this figure is usually unreadable: an arrow on
# every residue, all in saturated red, at an unstated scale factor, over
# a yellow and magenta cartoon. Four changes fix it.
#
#   SUBSAMPLE. One arrow per residue is a hairball at any useful zoom.
#   Every Nth residue carries the same information and leaves the
#   structure visible underneath.
#   THRESHOLD. Residues that barely move get no arrow. Below the
#   coordinate error the direction is noise, and a reader cannot tell a
#   noisy arrow from a real one.
#   COLOUR BY MAGNITUDE, not by nothing. A single red for every arrow
#   throws away the one quantity the figure is about. A sequential ramp
#   puts it back, and the key then does real work.
#   STATE THE SCALE, and prefer not to need one. Porcupine plots are
#   usually drawn scaled up, because for a small conformational change
#   true-length arrows are invisible. This motion is not small, so SCALE
#   is 1.0 here and the arrows are real lengths. If your motion does need
#   scaling, put the factor on the figure. Watch out for the failure mode
#   that forces the issue: scaling a 35 A displacement by 2.5 sends the
#   arrow clean off the canvas and wrecks the framing for everything else.
#
# Run inside ChimeraX after superposing:  runscript draw_vectors.py

import numpy
from chimerax.core.commands import run

START = "#1"
END = "#2"
CHAIN = "B"

STRIDE = 5          # draw an arrow every Nth residue
MIN_SHIFT = 1.0     # Angstrom; below this, no arrow
SCALE = 1.0         # 1.0 = true length; raise only if the motion is small
SHAFT_RADIUS = 0.26
HEAD_RADIUS = 0.62
HEAD_FRACTION = 0.35

# Sequential ramp, dark low to bright high, same family as example 06.
RAMP = ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"]
RAMP_MAX = 35.0     # Angstrom mapped to the top of the ramp


def ca_coords(model):
    run(session, "select %s/%s@CA" % (model, CHAIN), log=False)
    sel = session.selection.items("atoms")
    out = {}
    if sel and len(sel[0]) > 0:
        atoms = sel[0]
        for a, xyz in zip(atoms, atoms.scene_coords):
            out[a.residue.number] = xyz
    run(session, "select clear", log=False)
    return out


def ramp_color(shift):
    t = min(1.0, shift / RAMP_MAX) * (len(RAMP) - 1)
    return RAMP[int(round(t))]


a = ca_coords(START)
b = ca_coords(END)
shared = sorted(set(a) & set(b))

fmt = lambda p: "%.2f,%.2f,%.2f" % (p[0], p[1], p[2])

drawn = 0
shifts = []
for n in shared:
    d = b[n] - a[n]
    shift = float(numpy.linalg.norm(d))
    shifts.append(shift)
    if n % STRIDE or shift < MIN_SHIFT:
        continue
    tip = a[n] + d * SCALE
    join = a[n] + (tip - a[n]) * (1.0 - HEAD_FRACTION)
    c = ramp_color(shift)
    run(session, "shape cylinder fromPoint %s toPoint %s radius %g color %s name v%d_s"
        % (fmt(a[n]), fmt(join), SHAFT_RADIUS, c, n))
    run(session, "shape cone fromPoint %s toPoint %s radius %g topRadius 0 color %s name v%d_h"
        % (fmt(join), fmt(tip), HEAD_RADIUS, c, n))
    drawn += 1

shifts = numpy.array(shifts)
session.logger.info(
    "%d residues shared, %d arrows drawn (every %d, >= %.1f A). "
    "displacement median %.1f A, 90th pct %.1f A, max %.1f A, scale %gx"
    % (len(shared), drawn, STRIDE, MIN_SHIFT,
       float(numpy.median(shifts)), float(numpy.percentile(shifts, 90)),
       float(shifts.max()), SCALE))
