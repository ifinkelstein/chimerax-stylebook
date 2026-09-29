# Draw displacement arrows between two superposed states.
#
# For each named region, take the centroid of its Calpha atoms in the
# start state and in the end state, and draw an arrow between them: a
# cylinder shaft plus a cone head, built with the shape command. Also
# writes a legend listing each measured displacement, because the number
# is the useful part and an arrow alone cannot be measured off the page.
#
# Honesty rules baked in here:
#   the two states must already be superposed on a common reference, and
#   the reference must be a part that does not move, or every arrow is
#   measuring the fit rather than the motion. In figure.cxc the
#   superposition is on the RuvC core, so arrows are motions relative to
#   that core.
#   arrows are drawn at true length, never scaled up for drama. If a
#   motion is too small to see, the number is still printed.
#   regions below MIN_SHIFT get no arrow, because a short arrow reads as
#   a real direction when it is coordinate error.
#   arrows are one neutral colour, not the domain colour. An arrow is
#   annotation drawn on top of the structure; colouring it like the
#   structure makes readers take it for part of the model.
#
# Run inside ChimeraX:  runscript draw_arrows.py

import numpy
from chimerax.core.commands import run

START = "#1"          # start state, already superposed
END = "#2"            # end state
CHAIN = "B"
MIN_SHIFT = 1.5       # Angstrom; below this, draw no arrow
SHAFT_RADIUS = 0.9
HEAD_RADIUS = 2.4
HEAD_FRACTION = 0.28  # of total arrow length
ARROW_COLOR = "#222222"

# Regions to track. Keep this short: one arrow per thing you will discuss.
REGIONS = [
    ("HNH", "775-908"),
    ("L1", "765-780"),
    ("L2", "906-918"),
    ("REC2", "180-307"),
    ("REC3", "497-713"),
]


def centroid(model, resrange):
    run(session, "select %s/%s:%s@CA" % (model, CHAIN, resrange), log=False)
    sel = session.selection.items("atoms")
    coords = None
    if sel and len(sel[0]) > 0:
        coords = sel[0].scene_coords.mean(axis=0)
    run(session, "select clear", log=False)
    return coords


def fmt(p):
    return "%.2f,%.2f,%.2f" % (p[0], p[1], p[2])


measured = []
for name, resrange in REGIONS:
    a = centroid(START, resrange)
    b = centroid(END, resrange)
    if a is None or b is None:
        session.logger.warning("%s: not modelled in both states, skipped" % name)
        continue

    shift = float(numpy.linalg.norm(b - a))
    measured.append((name, shift))

    if shift < MIN_SHIFT:
        session.logger.info("%s: %.1f A, below threshold, no arrow drawn" % (name, shift))
        continue

    join = a + (b - a) * (1.0 - HEAD_FRACTION)
    run(session, "shape cylinder fromPoint %s toPoint %s radius %g color %s name %s_shaft"
        % (fmt(a), fmt(join), SHAFT_RADIUS, ARROW_COLOR, name))
    run(session, "shape cone fromPoint %s toPoint %s radius %g topRadius 0 color %s name %s_head"
        % (fmt(join), fmt(b), HEAD_RADIUS, ARROW_COLOR, name))
    session.logger.info("%s: %.1f A" % (name, shift))

# Legend of measured displacements, largest first
measured.sort(key=lambda nv: -nv[1])
y = 0.62
run(session, '2dlabels text "centroid displacement" xpos 0.03 ypos %.3f size 17 '
             'color black bold true' % (y + 0.05))
for name, shift in measured:
    tag = "" if shift >= MIN_SHIFT else "  (not drawn)"
    run(session, '2dlabels text "%s   %.1f Å%s" xpos 0.03 ypos %.3f size 16 color #222222'
        % (name, shift, tag, y))
    y -= 0.04
