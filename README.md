# ChimeraX stylebook

A house style for molecular figures in [UCSF ChimeraX](https://www.cgl.ucsf.edu/chimerax/) **1.12**: a color palette, a set of presets, and seventeen worked examples that render from scratch with one command. Built for the Finkelstein lab, useful to anyone who wants figures from different people in the same paper to look like they belong together.

> **Built with LLM assistance.** The scripts, presets and documentation in this repository were drafted with Claude (Anthropic) and then verified by rendering: every example here was actually executed in ChimeraX 1.12 and the resulting PNG inspected. Command syntax was checked against the [official ChimeraX documentation](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/), and every structure accession against the RCSB and EMDB APIs. Treat the stylistic opinions as opinions, and check anything you plan to publish.

Tested on ChimeraX 1.12 (released 11 June 2026) on macOS arm64. Older versions are untested here and some commands may differ.

Every figure in `examples/` is a plain text `.cxc` script committed next to the PNG it produces. Nothing here was made by clicking.

![domain architecture](examples/01_domain_architecture/domain_architecture.png)

## Why bother

Three problems this fixes. Figures from two students look like they came from two papers. A reviewer asks for one change and nobody can reproduce the figure six months later. And the same domain is blue in Figure 1 and green in Figure 4.

The fix is boring: name your colors once, keep the render settings in a preset, and commit the script.

## Install

```
git clone https://github.com/ifinkelstein/chimerax-stylebook.git ~/projects/chimerax-stylebook
```

In ChimeraX, open Favorites > Settings > Startup and set:

- **Custom presets folder** to `~/projects/chimerax-stylebook/presets`. The subfolders become menu categories, so Base > Publication White appears under Presets in the toolbar.
- **Execute these commands at startup** to `open ~/projects/chimerax-stylebook/startup.cxc`. That loads the named colors, defines a few aliases, and starts the REST listener so scripts and coding agents can drive your open window.

Check it worked:

```
chimerax --exit examples/01_domain_architecture/figure.cxc
```

## The rules

**1. White background for publication, dark for talks.** Never submit the dark version, never project the white one. Two presets, `Base/publication_white` and `Base/dark_talk`.

**2. Choose the render mode per panel, not per figure.** A figure with a map overview and an atomic zoom needs two different settings. Silhouettes on for zooms where outlines separate foreground from context; off for map surfaces where they trace noise. Soft ambient-occlusion lighting for almost everything; flat lighting for transparent-surface overviews; full lighting with shadows only on dark backgrounds.

**3. Gray means given, reference, or context.** The target protein, the design model in an overlay, every domain not under discussion. Color is reserved for the subject of the panel. Two or three colors in a zoom; the full domain code only in an overview that prints its legend.

**4. Okabe-Ito for categories, viridis or cividis for continuous values.** The palette is color-blind safe and matches our matplotlib figures, so a panel of plots and a panel of structures sit together without clashing. Never rainbow. The one sanctioned exception is electrostatic potential, where red-white-blue is a field convention and a novel palette would mislead.

**5. Name colors semantically, in one file.** Figure scripts say `color /B lab_sgrna`, not `color /B #E69F00`. Change the mapping in `palettes/lab_colors.cxc` and every figure updates.

**6. Nucleic acids stay opaque and saturated** even when the protein surface goes transparent. They are usually the thing the reader needs to track.

**7. Legends come from the `key` command, not from Illustrator.** A legend drawn by hand is a legend that goes stale. Put it in a margin, never over the structure.

**8. Label with `2dlabels` and `key`, never with `label` on a range.** The `label` command is per residue. Pointing it at a 130-residue domain draws 130 overlapping labels and produces a black smear. Ask how we know.

**9. Confidence does not go on the model.** No pLDDT or PAE coloring in a figure that makes a structural claim. Put confidence in its own panel, as BindCraft does. Example 05 shows the coloring because judging a prediction is a legitimate separate use.

**10. State comparisons share one orientation, one scale, one set of colors.** Superpose on a reference, set the view once, then render one PNG per state by hiding the others. Never re-frame between panels.

**11. Set `windowsize` before `view`.** Saving at a different aspect ratio than the window changes what is in the frame, not just how big it is.

**12. Export big, then trim.** ChimeraX pads its own framing and writes 144 dpi metadata, so a raw export wastes pixels on background and reports the wrong print resolution. `scripts/render.sh` trims the border to a fixed margin and stamps 300 dpi. Panels here land at 1500 to 2600 px wide, which is 5 to 8.7 inches at 300 dpi.

**13. Motion is a claim, and a weak one.** A morph is an interpolation between two observed endpoints; the frames in between are not structures. Label it as such. Arrows drawn between states are relative to whatever you superposed on, so name the reference. Draw arrows at true length and drop the ones too short to mean anything.

**14. Commit the script.** Every published figure has its `.cxc` in version control and its PDB or EMDB accession in the filename or the header comment.

## Repository layout

```
palettes/
  lab_colors.cxc      named colors: categorical, pastel, semantic aliases
  cas9_domains.cxc    SpCas9 domain color map, applied to a selected chain
presets/
  Base/               publication_white, dark_talk, surface_binder
examples/             seventeen worked figures, each a figure.cxc plus its output
docs/
  chimerax_commands.md   verified 1.12 command reference for figure work
  reference_styles.md    what we borrowed from which published work
scripts/
  render.sh           re-render every example, then trim and stamp dpi
  orbit.sh            render a ring of orientations as one contact sheet
  finish.sh           trim background border, stamp 300 dpi
  gif.sh              make a README-sized GIF from a rendered mp4
  cx                  send commands to a running ChimeraX over REST
startup.cxc           load colors and aliases, start REST control
```

## Examples

Each folder holds `figure.cxc` and the PNG it produces. Run one with `chimerax --exit figure.cxc` from inside its folder, or re-render everything with `scripts/render.sh`.

| | Example | Shows |
|---|---|---|
| 01 | [Domain architecture](examples/01_domain_architecture/) | Categorical coloring, `key` legend, semantic color names |
| 02 | [State comparison](examples/02_state_comparison/) | `matchmaker`, one orientation across three panels |
| 03 | [Cryo-EM map](examples/03_cryoem_map/) | `color zone` onto a map, `volume zone`, density over model |
| 04 | [Target and binder](examples/04_binder_target/) | The gray-target convention, transparency on a surface |
| 05 | [AlphaFold pLDDT](examples/05_alphafold_plddt/) | `alphafold fetch`, B-factor coloring, the alphafold palette |
| 06 | [Per-residue data](examples/06_per_residue_data/) | `defattr` from a Python calculation, viridis, explicit range |
| 07 | [Electrostatics](examples/07_electrostatics/) | `coulombic`, diverging palette, symmetric range |
| 08 | [Interface zoom](examples/08_interface_zoom/) | Gray context, sticks, `hbonds`, per-residue 3D labels |
| 09 | [Nucleic acid styles](examples/09_nucleic_acid_styles/) | ladder, slab, fill and atoms compared |
| 10 | [Dark talk slide](examples/10_dark_talk/) | The same structure restyled for projection |
| 11 | [State ramp](examples/11_state_ramp/) | An ordered ramp for a reaction coordinate, with a reusable legend strip |
| 12 | [Morph movie](examples/12_morph_movie/) | `morph`, captions that change, pauses on each endpoint |
| 13 | [Conservation](examples/13_conservation/) | ConSurf grades from a MAFFT alignment, colorblind-safe palette |
| 14 | [Camera movies](examples/14_camera_movies/) | Spin, rock and zoom, and when each is honest |
| 15 | [Motion arrows](examples/15_motion_arrows/) | Displacement arrows at true length, with measured distances |
| 16 | [Active site](examples/16_active_site/) | A tight catalytic-site zoom: metal, coordination dashes, 3D labels |
| 17 | [Vector field](examples/17_vector_field/) | Per-residue displacement arrows, subsampled and colored by magnitude |

### 02 State comparison

Apo, binary and R-loop at one orientation and one scale. The protein is pale so the nucleic acids carry the change.

<p>
<img src="examples/02_state_comparison/state1_apo.png" width="32%">
<img src="examples/02_state_comparison/state2_binary.png" width="32%">
<img src="examples/02_state_comparison/state3_rloop.png" width="32%">
</p>

### 03 Cryo-EM map

Left, the map colored by the domain colors of the model inside it. Right, the HNH domain with its own density drawn semi-transparent on top.

<p>
<img src="examples/03_cryoem_map/map_overview.png" width="48%">
<img src="examples/03_cryoem_map/map_zoom.png" width="48%">
</p>

### 04 Target and binder

The anti-CRISPR AcrIIA4 in the PAM-recognition site. One saturated color, everything else neutral.

![binder and target](examples/04_binder_target/binder_target.png)

### 05 and 06 Data on structures

pLDDT from the AlphaFold model, and a per-residue distance computed in Python and loaded through a `defattr` file.

<p>
<img src="examples/05_alphafold_plddt/alphafold_plddt.png" width="48%">
<img src="examples/06_per_residue_data/per_residue_data.png" width="48%">
</p>

### 07 and 08 Surfaces and interfaces

Coulombic potential showing the nucleic-acid channel, and the PAM-recognition arginines with context reduced to a line drawing.

<p>
<img src="examples/07_electrostatics/electrostatics.png" width="48%">
<img src="examples/08_interface_zoom/interface_zoom.png" width="48%">
</p>

### 09 Nucleic acid representations

Pick by how much base detail the argument needs. Ladder for overviews, slab when stacking or a kink is the point, fill for contacts, atoms for the tightest zooms.

<p>
<img src="examples/09_nucleic_acid_styles/na_ladder.png" width="24%">
<img src="examples/09_nucleic_acid_styles/na_slab.png" width="24%">
<img src="examples/09_nucleic_acid_styles/na_fill.png" width="24%">
<img src="examples/09_nucleic_acid_styles/na_atoms.png" width="24%">
</p>

### 10 Dark talk slide

![dark talk](examples/10_dark_talk/dark_talk.png)

### 11 State ramp

Five states of multi-turnover SpCas9 as an ordered ramp rather than five categorical colors. The same ramp goes under the panels, into the progression arrow, and into any bar of state occupancy, so the reader learns it once.

<p>
<img src="examples/11_state_ramp/state1.png" width="19%">
<img src="examples/11_state_ramp/state2.png" width="19%">
<img src="examples/11_state_ramp/state3.png" width="19%">
<img src="examples/11_state_ramp/state4.png" width="19%">
<img src="examples/11_state_ramp/state5.png" width="19%">
</p>

![state ramp legend](examples/11_state_ramp/ramp_legend.png)

### 12 Morph movie

HNH nuclease domain docking, checkpoint state to catalytic state, with the caption changing and a pause on each endpoint. The caption says on its face that the intermediate frames are interpolation, not data.

![HNH morph](examples/12_morph_movie/hnh_morph.gif)

Full resolution: [hnh_morph.mp4](examples/12_morph_movie/hnh_morph.mp4)

Choosing the endpoints is the whole job. A morph silently drops every residue not modelled in both inputs. The obvious source series for this figure turned out to have HNH unmodelled in one state, so residues 764 to 924 were absent from the morph entirely and it animated nothing. The script shows how to check before rendering.

### 13 Conservation

ConSurf's grammar, which is good: nine percentile grades rather than a raw score, one direction from variable to conserved, a separate neutral category for residues with too little data, and a surface render so conserved patches read as patches. The palette is the part we change, to ColorBrewer BrBG reversed, which is colorblind-safe and survives grayscale.

<p>
<img src="examples/13_conservation/conservation_surface.png" width="48%">
<img src="examples/13_conservation/conservation_cartoon.png" width="48%">
</p>

Run `examples/13_conservation/build_alignment.sh` first. It fetches Cas9 orthologs from UniProt, keeps those close in length to SpCas9, and aligns them with MAFFT. Conservation is a property of the sequence set, not of the protein, so the figure names the set and you should too.

### 14 Camera movies

Spin for shape, rock for depth without disorientation, zoom to connect an overview to a close-up.

<p>
<img src="examples/14_camera_movies/spin.gif" width="32%">
<img src="examples/14_camera_movies/rock.gif" width="32%">
<img src="examples/14_camera_movies/zoom.gif" width="32%">
</p>

Full resolution: [spin.mp4](examples/14_camera_movies/spin.mp4), [rock.mp4](examples/14_camera_movies/rock.mp4), [zoom.mp4](examples/14_camera_movies/zoom.mp4)

Do not build the zoom with the `zoom` command. It multiplies magnification about the current centre, so on a buried target it flies through the surface and ends inside the protein looking at backfaces. Name the two framings and let `view` interpolate between them instead.

### 15 Motion arrows

Which parts moved, in what direction, and how far. This is the still-figure counterpart to the morph: use arrows when the reader needs to measure the motion, a morph when they need to feel it.

![motion arrows](examples/15_motion_arrows/motion_arrows.png)

Arrows are annotation, so they are one neutral color rather than the domain color. They run from start centroid to end centroid at true length, never scaled up, and anything under 1.5 Å is dropped because a short arrow reads as a real direction when it is coordinate error. The measured distances are printed beside the figure, since an arrow on a page cannot be measured.

### 16 Active site

The HNH nuclease site with its magnesium, the residues that hold it, the scissile phosphate and the ordered waters. This is the tightest panel class in the book and it inverts several rules: everything outside the site is hidden rather than faded, sticks take element colors because a reader finds oxygen by its red faster than by any scheme we could invent, and the backbone goes neutral and pale so it reads as a container.

![active site](examples/16_active_site/active_site.png)

Orientation here was chosen by looking, not guessing. `scripts/orbit.sh examples/16_active_site` renders a ring of candidate views and stitches them into one contact sheet, which is worth doing for any zoom where a single helix in the wrong place hides the subject.

### 17 Vector field

An arrow per residue, showing which parts of a domain move together and where the hinge sits. Three things make the usual version of this figure unreadable, and all three are fixed here: subsample so it is not a hairball, drop displacements too small to be signal, and color by magnitude so the key does real work instead of every arrow being the same red.

![vector field](examples/17_vector_field/vector_field.png)

The RuvC core carries almost no arrows, which is the internal check: it is the superposition reference, so it should not move. These arrows are true length because this motion is large. Scaling is normal for a smaller change, but then the factor belongs on the figure.

## Three ways to show motion

The book now has three, and they answer different questions.

| | Use when the reader needs to | Scale |
|---|---|---|
| [Morph movie](examples/12_morph_movie/) | feel the motion | interpolated, not data |
| [Motion arrows](examples/15_motion_arrows/) | measure it, per domain | true length |
| [Vector field](examples/17_vector_field/) | see the pattern, per residue | true length here, often scaled |

A paper usually wants the arrows in the figure and the morph in the supplement.

## Palette

Categorical colors are Okabe and Ito's eight-color set, which stays distinguishable under protanopia, deuteranopia and tritanopia. Pastel variants are 60 percent color on white, for large cartoon and surface areas where a saturated fill would overwhelm the accents.

| Name | Hex | Typical use |
|---|---|---|
| `lab_orange` | `#E69F00` | sgRNA, guide |
| `lab_skyblue` | `#56B4E9` | non-target strand |
| `lab_green` | `#009E73` | |
| `lab_yellow` | `#F0E442` | HNH |
| `lab_blue` | `#0072B2` | target strand |
| `lab_vermillion` | `#D55E00` | PAM, bridge helix, binder |
| `lab_purple` | `#CC79A7` | |
| `lab_gray` | `#999999` | context |

Semantic aliases (`lab_sgrna`, `lab_target`, `lab_hnh`, `lab_rec1`) point at these. Use the alias in figure scripts so a palette change is a one-line edit.

Continuous data uses viridis or cividis. Neither is built into ChimeraX, so write the stops explicitly, as example 06 does.

## Gotchas

**Chain IDs are case sensitive and are not what you expect.** In 4UN3 the protein is chain B and the sgRNA is chain A. In 5F9R the protein is chain B. In 7S4X and several other cryo-EM entries, `C` and `c` are two different fragments of the target strand. Run `info chains` before writing a selection.

**Several crystal entries have two copies in the asymmetric unit.** 4CMP, 4OO8, 4ZT0 and others. Delete the extra copy or you render a dimer with no biological meaning.

**Comments cannot trail a command.** ChimeraX parses `color name lab_x #D9D9D9 # a comment` as extra arguments and fails. Comments go on their own line.

**Nucleotide ladders and slabs need base atoms displayed.** The base presets run `show nucleic atoms` before `nucleotides ladder` for that reason. Apply `nucleotides` after any `hide` that touches nucleic acids.

**`view pad` is a fraction, not a multiplier.** `view pad 0.25` adds a quarter. `view pad 2.5` zooms out until the structure is a dot. It must also be in the same command as the spec: `view /A:775-908 pad 0.25`. On its own line it re-frames every displayed model rather than the selection.

**A bare `show pseudobonds` turns on missing-structure dashes too**, which at active-site zoom scatter little specks across the panel. Show only the pseudobonds you want: `show (:MG & /B:1403) target p`.

**Never hardcode a submodel ID.** `coulombic /A surfaces #1.1` looks right and silently colors nothing, because hydrogen-bond and missing-structure pseudobond groups take submodel numbers ahead of the surface. Omit the option and let the command find the surface, or check with `info models` first.

**On macOS, `--nogui` cannot save images.** There is no OSMesa, so headless rendering fails with an OpenGL error. Run `chimerax --exit script.cxc`, which opens a window briefly and closes it. `--offscreen` is Linux only.

**`chimerax --exit` swallows errors.** The terminal shows almost nothing. Either run the script through the REST listener, which returns the log including errors, or use `scripts/render.sh`, which does that for you.

## Working with a coding agent

`startup.cxc` starts a REST listener on port 60000, so a script or an AI assistant can drive the ChimeraX window you already have open:

```
scripts/cx 'open 4oo8; color /B lab_sgrna; save /tmp/out.png width 2000 supersample 3'
```

This is the fast loop: the agent sends commands, saves a PNG, looks at it, and adjusts. You can rotate the model by hand in between. When you have what you want, `log save log.html` and fold the commands back into the script.

## Credits

This stylebook is a synthesis of other people's published work. The conventions are theirs; the mistakes are ours. `docs/reference_styles.md` records what came from where.

### Figure style

- **David W. Taylor lab, UT Austin.** The three-render-modes-per-figure approach, the opaque segmented map, the gray line-drawing context in atomic zooms, per-entity transparent density over an opaque model, and the practice of keeping one domain color code across every paper. Seen in [Bravo et al., *Nature* 603:343 (2022)](https://doi.org/10.1038/s41586-022-04470-1), [Hibshman et al., *Nat Commun* 15:3663 (2024)](https://doi.org/10.1038/s41467-024-47830-3) and [Kiernan et al., *Nat Commun* 16:5681 (2025)](https://doi.org/10.1038/s41467-025-60668-7).
- **BindCraft.** [Pacesa et al., *Nature* 646:483 (2025)](https://doi.org/10.1038/s41586-025-09429-6). The gray-target and colored-binder convention, two or three colors per structural panel, and the discipline of keeping confidence metrics off the model.
- **The Human Bindome.** [Wenckstern, Díaz-Rovira et al., bioRxiv 2026.07.30.741542](https://www.biorxiv.org/content/10.64898/2026.07.30.741542v1). The three-role gray/binder/functional-site scheme, and projecting an aggregate per-residue statistic onto a single representative structure.
- **Dawid Zyla**, [Making figures for the manuscript with ChimeraX](https://www.dzyla.com/science/making-figures-manuscript-chimerax/). The base render settings and the argument for fixing a palette at the start of a project.
- **Oliver Clarke**, [chimerax-trimmings](https://github.com/olibclarke/chimerax-trimmings). The pattern of a lab preset folder plus startup aliases.
- **Lukas Schmidheini**, [ChimeraX-FigureStyle](https://github.com/LUKASinScience/ChimeraX-FigureStyle). A GUI plugin covering similar ground with saved templates; worth using if you prefer buttons to scripts.
- **Shyam Saladi**, [chimerax_viridis](https://github.com/smsaladi/chimerax_viridis). Perceptually uniform palettes for ChimeraX.
- **Matthias Vorländer**, [ChimeraX tutorial: Analysing AlphaFold Predictions and More](https://www.cgl.ucsf.edu/chimerax/data/vorlander-jan2025/ChimeraX_tutorial.html). The recommendation to save styles and per-project color codes as `.cxc` presets.
- **Masataka Okabe and Kei Ito**, [Color Universal Design](https://jfly.uni-koeln.de/color/). The categorical palette.
- **Claus O. Wilke**, [Fundamentals of Data Visualization](https://clauswilke.com/dataviz/). The palette reasoning, shared with our [dataviz-python](https://github.com/ifinkelstein/dataviz-python) repository.

### Software

- **UCSF ChimeraX**, developed by the Resource for Biocomputing, Visualization, and Informatics at UC San Francisco, with support from NIH R01-GM129325 and the Office of Cyber Infrastructure and Computational Biology, NIAID. Cite [Meng et al., *Protein Sci* 32:e4792 (2023)](https://doi.org/10.1002/pro.4792) and [Pettersen et al., *Protein Sci* 30:70 (2021)](https://doi.org/10.1002/pro.3943).

### Structures used in the examples

Every coordinate set here belongs to the group that determined it. Cite the primary paper, not this repository.

| Accession | Example | Determined by |
|---|---|---|
| [4CMP](https://www.rcsb.org/structure/4CMP) | 02 | Jinek et al., *Science* 343:1247997 (2014). [doi](https://doi.org/10.1126/science.1247997) |
| [4OO8](https://www.rcsb.org/structure/4OO8) | 01, 06, 07, 09, 10 | Nishimasu et al., *Cell* 156:935 (2014). [doi](https://doi.org/10.1016/j.cell.2014.02.001) |
| [4UN3](https://www.rcsb.org/structure/4UN3) | 08 | Anders et al., *Nature* 513:569 (2014). [doi](https://doi.org/10.1038/nature13579) |
| [4ZT0](https://www.rcsb.org/structure/4ZT0) | 02 | Jiang et al., *Science* 348:1477 (2015). [doi](https://doi.org/10.1126/science.aab1452) |
| [5F9R](https://www.rcsb.org/structure/5F9R) | 02 | Jiang et al., *Science* 351:867 (2016). [doi](https://doi.org/10.1126/science.aad8282) |
| [5VW1](https://www.rcsb.org/structure/5VW1) | 04 | Yang & Patel, *Mol Cell* 67:117 (2017). [doi](https://doi.org/10.1016/j.molcel.2017.05.024) |
| [7S4X](https://www.rcsb.org/structure/7S4X) and [EMD-24838](https://www.ebi.ac.uk/emdb/EMD-24838) | 03 | Bravo et al., *Nature* 603:343 (2022). [doi](https://doi.org/10.1038/s41586-022-04470-1) |
| [7Z4L](https://www.rcsb.org/structure/7Z4L) and [7Z4J](https://www.rcsb.org/structure/7Z4J) | 12, 15 | Pacesa et al., *Nature* 609:191 (2022). [doi](https://doi.org/10.1038/s41586-022-05114-0) |
| [9EAK](https://www.rcsb.org/structure/9EAK), [9EAL](https://www.rcsb.org/structure/9EAL), [9ED9](https://www.rcsb.org/structure/9ED9), [9EDA](https://www.rcsb.org/structure/9EDA), [9EDB](https://www.rcsb.org/structure/9EDB) | 11 | Kiernan et al., *Nat Commun* 16:5681 (2025). [doi](https://doi.org/10.1038/s41467-025-60668-7) |
| [AF-Q99ZW2-F1](https://alphafold.ebi.ac.uk/entry/Q99ZW2) | 05 | AlphaFold Protein Structure Database, EMBL-EBI and DeepMind. Cite [Jumper et al., *Nature* 596:583 (2021)](https://doi.org/10.1038/s41586-021-03819-2) and [Varadi et al., *Nucleic Acids Res* 52:D368 (2024)](https://doi.org/10.1093/nar/gkad1011) |

The conservation example aligns Cas9-family sequences retrieved from [UniProt](https://www.uniprot.org/) ([UniProt Consortium, *Nucleic Acids Res* 51:D523, 2023](https://doi.org/10.1093/nar/gkac1052)) with [MAFFT](https://mafft.cbrc.jp/alignment/software/) ([Katoh & Standley, *Mol Biol Evol* 30:772, 2013](https://doi.org/10.1093/molbev/mst010)). The nine-grade percentile scheme and the variable-to-conserved direction come from [ConSurf](https://consurf.tau.ac.il/) ([Ashkenazy et al., *Nucleic Acids Res* 44:W344, 2016](https://doi.org/10.1093/nar/gkw408)); the underlying score here is ChimeraX's own information-theoretic conservation, not ConSurf's rate4site evolutionary rate, and the palette is ColorBrewer BrBG reversed ([Brewer, ColorBrewer](https://colorbrewer2.org/)) rather than ConSurf's own. Movies are encoded with [FFmpeg](https://ffmpeg.org/); PNG trimming uses [ImageMagick](https://imagemagick.org/).

SpCas9 domain boundaries in `palettes/cas9_domains.cxc` follow Nishimasu et al. 2014 for the two-lobe scheme, with REC3 defined as residues 497 to 713 following the usage in [Skeens et al., *Sci Adv* 10:eadl1045 (2024)](https://doi.org/10.1126/sciadv.adl1045). Linker definitions are from Jiang et al. 2016. PAM-recognition and phosphate-lock assignments are from Anders et al. 2014.

Structure data from the RCSB Protein Data Bank ([Berman et al., *Nucleic Acids Res* 28:235, 2000](https://doi.org/10.1093/nar/28.1.235)) and EMDB ([wwPDB Consortium, *Nucleic Acids Res* 52:D456, 2024](https://doi.org/10.1093/nar/gkad1019)).

## License

Scripts and documentation: MIT. The rendered PNGs depict coordinate data from the PDB and EMDB, which is in the public domain; the papers that produced it are cited above and should be cited in any reuse.
