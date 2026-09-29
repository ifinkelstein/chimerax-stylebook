# Where this style comes from

Three published bodies of work shaped the rules in the README. This page records what we took from each and why, so the choices are auditable rather than arbitrary. Go read the originals; the citations are in the README credits.

## Taylor lab CRISPR cryo-EM papers

The most useful lesson is that one figure should not use one render setting. Their panels fall into three classes and each gets its own treatment.

Map overviews use an opaque surface with no model inside, never mesh, lit with ambient occlusion so crevices darken, and no silhouettes. The map is segmented so each domain carries its own color.

Surface and state-comparison panels use flat lighting and no silhouettes, with protein surfaces made partly transparent while nucleic acids stay opaque and saturated in front of them. States sit side by side at one orientation and one scale.

Atomic zoom panels turn silhouettes on and drop the context protein to light gray so it reads as a line drawing, then paint only the residues under discussion. Bases appear as filled slabs, hydrogen bonds as dashed lines, and per-entity density is drawn semi-transparent in each entity's own color over an opaque model.

Their domain color code is constant across papers and is republished as a one-dimensional domain bar in every figure, which is what makes ten colors in a panel legible. We copy the discipline, not the specific hues: our palette is Okabe-Ito so it survives color-blind readers and matches our matplotlib figures.

For a series of states they use an ordered sequential ramp and reuse it for the progression arrow and the class-occupancy chart. Worth stealing whenever a figure shows a reaction coordinate.

## BindCraft

Two conventions carry over almost unchanged.

Gray means given, reference, or context. The target protein is a gray or muted surface, a design model overlaid on an experimental structure is gray, and anything not under discussion is gray. Color is reserved for the subject of the panel. Two or three colors per structural panel, not ten.

Confidence never goes on the model. No pLDDT rainbow, no PAE coloring in the structural figures; those live in histograms. We keep pLDDT coloring available as an example because it is genuinely useful for judging a prediction, but the rule is that a figure making a structural claim should not be colored by confidence.

Their maps are transparent surfaces with the model visible inside, not mesh, and the design-versus-experiment overlay prints the Cα RMSD as plain text with nothing else in the panel.

## Human Bindome preprint

A proteome-scale binder atlas from the BindCraft authors. Two things are worth adopting. First, the three-role color scheme of gray target, colored binder, and a third color for functionally annotated residues, which extends BindCraft's two-role scheme without breaking it. Second, projecting an aggregate per-residue statistic onto one representative structure as a continuous ramp, rather than showing one complex. Our per-residue data example follows that idea.

Caveat: the preprint's figure images were not retrievable, so this reading comes from caption text and the web viewer source. Treat the render details as inferred.

## Where we diverge

We use Okabe-Ito rather than any of the three source palettes, because color-blind safety and consistency with our plotting stack matter more to us than matching a specific paper. We use the `key` command for legends instead of hand-drawn Illustrator chips, so that the legend is reproducible from the script. And we keep every figure's `.cxc` in version control, which none of the sources do publicly.
