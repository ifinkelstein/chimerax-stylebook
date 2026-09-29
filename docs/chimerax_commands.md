# ChimeraX 1.12 command reference for figure work

Syntax below is copied from the official ChimeraX user docs (links at the end). Conventions: several commands per line separated by `;`, command names and keywords can be truncated to a unique prefix, quote strings or paths that contain spaces, `~cmd` undoes many commands. Trailing `#` comments on a command line are **not** allowed in `.cxc` files; put comments on their own line.

Color specs: named colors (`cornflowerblue`, or any name defined with `color name`), hex `#rrggbb` or `#rrggbbaa`, `r,g,b[,a]` on a 0–100 scale.

## 1. Coloring by chain, model, polymer; named colors; palettes

```
color [spec] [colorname] [target string] [transparency percent]
color bychain
color bypolymer
color bymodel
color byhetero
color /A cornflowerblue ; color /B gold ; color /C #b188a7
color /d & helix sky blue target c
```

Target letters (no separators): `a` atoms/bonds, `b` bonds only, `c` or `r` cartoons, `s` surfaces, `p` pseudobonds, `f` ring fill and nucleotide slabs/ladders, `l` labels.

Named colors (this repo defines them in `palettes/lab_colors.cxc`):

```
color name cname color-spec
color delete cname
color list custom
```

Palette option syntax (shared by `color byattribute`, `coulombic`, `mlp`, `key`):

```
palette palette-name                       palette rainbow, palette Blues-5
palette color1:color2:color3               colors spread evenly over the range
palette "value1,color1:value2,color2"      explicit stops
palette ^palette-name                      reverse
range low,high | full
```

Built-in palettes: `rainbow`, `redblue`, `bluered`, `cyanmaroon`, `grayscale`, `lipophilicity`, `alphafold`, `esmfold`, `pae`, `paegreen`, plus ColorBrewer as `Name-N` (qualitative Set1/Set2/Dark2/Paired..., sequential Blues/Greens/YlOrRd..., diverging RdBu/PuOr/PiYG/BrBG...). Viridis, magma, cividis are **not** built in. Define them as explicit stops; example 06 and example 13 show the stop syntax.

Gotcha: an explicit `range` overrides values in a `value,color` palette.

## 2. B-factor coloring and color keys

```
color byattribute [a:|r:|c:]attr [spec] [target] [average residues] [palette ...] [range ...] [key true|false] [noValueColor color]
color bfactor /A range 2,30
color bfactor protein palette blue:white:red
```

`average residues` colors atoms by per-residue mean. `key true` opens the Color Key tool preloaded.

Color key (legend). Orientation follows `size`: taller than wide is vertical. Coordinates are window fractions from lower left, so a key placed for the on-screen window stays put when you save at higher resolution with the same aspect.

```
key color1:label1 color2:label2 ... [pos x,y] [size w,h] [fontSize N] [colorTreatment blended|distinct] [labelSide left/top|right/bottom] [justification left|right|decimal] [labelOffset px] [border true|false] [ticks true|false]
key palette-name :label1 :label2 ...
key red:low white: blue:high
key blues-5 :0 :25 :50 :75 :100
key delete
```

For a categorical legend use `colorTreatment distinct`. Labels containing spaces must be quoted as a whole pair: `"lab_target:target DNA"`. In a vertical key the first entry is at the bottom.

## 3. AlphaFold models and pLDDT

```
alphafold fetch Q99ZW2 [alignTo #1/A] [trim true|false] [colorConfidence true|false] [pae true|false]
open alphafold:Q99ZW2
alphafold match #1
alphafold pae #1 [file scores.json] [plot true] [colorDomains true]
color bfactor #1 palette alphafold
key alphafold :0 :50 :70 :90 :100
```

pLDDT is stored in the B-factor column. `alphafold` palette thresholds are 0, 50, 70, 90, 100. `alphafold pae ... colorDomains true` assigns a residue attribute `pae_domain` you can color by. `alphafold contacts` draws PAE-colored pseudobonds between residues.

## 4. Custom per-residue data: defattr and setattr

Attribute file (tab separated data lines, header lines first):

```
attribute: myscore
recipient: residues
match mode: 1-to-1
	#1/A:12	0.83
	#1/A:13	0.11
```

```
open scores.defattr
color byattribute r:myscore #1 palette ^RdYlBu-7 range 0,1 key true
save scores.defattr attrName r:myscore format defattr
setattr #1/A:100-120 residues myflag 1 create true
cartoon byattribute r:myscore #1 0:0.25 1:2.0     (worm radius by attribute)
```

Residue-level attribute names may need the `r:` prefix in `color byattribute` when ambiguous.

## 5. Electrostatics and hydrophobicity

```
surface #1/A
coulombic #1/A palette redblue range -10,10 key true
coulombic protein palette ^RdBu-7 range -8,8
mlp #1 palette lipophilicity range -20,20 key true
```

Coulombic adds hydrogens and charges to a copy; the structure is not modified. Default palette is red-white-blue, range -10 to 10 kcal/(mol e).

## 6. Cryo-EM maps

```
open emdb:24838
volume #2 style surface level 0.1 color lab_map_gray transparency 0.6 step 1
volume #2 style mesh level 0.1 color #666666
volume zone #2 nearAtoms #1/C range 2.5
surface zone #2 nearAtoms #1:1333,1335 distance 4
surface dust #2 size 8
fitmap #1 inMap #2 [resolution 3] [search 100]
measure mapstats #2
```

`volume ... transparency` is 0–1 whereas the `transparency` command is a percent. Local resolution: open the local-res map as #3 then `color sample #2 map #3 palette ^rainbow range 3,8 key true`, or `measure mapvalues #3 atoms #1 attribute localres` followed by `color byattribute a:localres`. `color zone #2 near #1 distance 3` colors a map surface by the nearby model colors. Clipping: `clip near 0` / `clip front 10 position :1333` / `clip off`; `clip model #!2 false` excludes a model.

## 7. Superposition, RMSD, morph

```
matchmaker #2 to #1 [bring #3] [pairing bb|bs|ss] [showAlignment true]
mm #2/B to #1/A
color byattribute seq_rmsd #1,2 palette blue:white:red range 0,5 key true
align #2@CA toAtoms #1@CA
rmsd #2@CA to #1@CA
morph #1,2 frames 40 [same true] [method corkscrew]
coordset #3 1,40 ; wait 40
```

`showAlignment true` creates the `seq_rmsd` residue attribute from the RMSD header. Morph produces a trajectory model; scripts need `wait N` after multi-frame commands.

## 8. Interfaces, contacts, zones, 3D labels

```
hbonds (/A & protein) restrict (/C & nucleic) reveal true showDist false color lab_black radius 0.08 dashes 6
hbonds delete
contacts /B restrict /A reveal true
interfaces select /A contacting /B bothSides true
measure buriedarea /A withAtoms2 /B
select zone /C:1-3 4.5 protein residues true
show sel atoms ; style sel stick ; color sel & C lab_gray_p target a
cartoon suppressBackboneDisplay false
label :1333,1335 residues text "{0.name}{0.number}" height 1.2 color black bgColor white offset 0,1,0
label delete
```

3D `label` is per atom/residue. Never apply it to a whole domain or chain; use `2dlabels` or `key` for that.

## 9. Nucleic acids

```
nucleotides nucleic ladder radius 0.35 [showStubs true] [hideAtoms true]
nucleotides /C,D slab shape box
nucleotides /C,D tube/slab
nucleotides /B fill
nucleotides nucleic atoms
cartoon style nucleic xsection oval width 1.2 thickness 0.4
color /D:20-22 lab_pam target cf
color /C:15 lab_vermillion target acf
```

Ladder rungs and slabs are only drawn for residues whose base atoms are displayed. The base presets run `show nucleic atoms` first for that reason. Target `f` covers rungs and slabs, `c` the backbone ribbon, `a` sticks.

## 10. Rendering

```
lighting soft | full | simple | flat | gentle
lighting simple shadows true multiShadow 128 depthCue false
graphics silhouettes true width 1.5 depthJump 0.01
material dull | shiny | default
cartoon style protein modeHelix default arrows true xsection oval width 1.6 thickness 0.4
cartoon style helix modeHelix tube radius 2 sides 24
camera ortho
set bgColor white
windowsize 1000 750
view [spec] [pad 0.05] ; view orient ; view name v1 ; view v1
turn y 30 ; cofr #1/A:840
save fig.png width 2400 supersample 3 [transparentBackground true]
save fig.cxs
```

Presets: soft = ambient occlusion, no direct light (the house default). full = shadows plus AO, good on dark backgrounds. Set `windowsize` before `view` so the on-screen framing matches the saved aspect; if `save` gets both width and height that differ from the window aspect, the content changes.

## 11. 2D annotations

```
2dlabels text "REC lobe" xpos 0.05 ypos 0.92 size 24 color lab_black bold true
2dlabels arrow start 0.5,0.1 end 0.7,0.3 color black weight 1.5 headStyle solid
2dlabels delete all
scalebar 50 thickness 6 xpos 0.05 ypos 0.05 color black
2dlabels text "50 Å" xpos 0.05 ypos 0.09 size 20 color black
```

Coordinates are window fractions from the lower left.

## 12. Presets and aliases

Preferences > Startup > Custom presets folder: `.cxc` or `.py` files. Files directly in the folder are category Custom; first-level subfolders become categories; underscores become spaces. Point it at this repo's `presets/` and you get Presets > Base > Publication White, etc.

```
preset base "publication white"
alias pub open ~/projects/chimerax-stylebook/presets/Base/publication_white.cxc
alias ribcolor color $1 $2 target c
```

## 13. Batch and remote control

```
chimerax --exit figure.cxc
chimerax --cmd "open 4oo8; save out.png width 2000; exit"
chimerax --script "render.py arg1"
chimerax --nogui --exit script.cxc       analysis only; on macOS it cannot save images
```

`--offscreen` (OSMesa) is Linux only. On macOS run with the GUI; the window appears briefly.

Inside a session: `open script.cxc`, `runscript script.cxc arg1` (`$1` substitution), `perframe`, `log save log.html`.

REST control lets a shell or a coding agent drive the open window:

```
remotecontrol rest start port 60000
curl -G --data-urlencode "command=open 4oo8; lighting soft; save /tmp/out.png width 2000" http://127.0.0.1:60000/run
remotecontrol rest stop
```

The response contains the log text, including errors, which `chimerax --exit` does not print to the terminal. `scripts/cx` and `scripts/render.sh` in this repo wrap this.

## Sources

Official docs, all under https://www.cgl.ucsf.edu/chimerax/docs/user/commands/ : color, palettes, colornames, colortables, key, defattr, setattr, alphafold, coulombic, mlp, volume, surface, transparency, fitmap, measure, clip, matchmaker, align, rmsd, morph, coordset, movie, wait, hbonds, clashes, interfaces, select, atomspec, show, style, size, label, 2dlabels, scalebar, nucleotides, cartoon, lighting, graphics, material, camera, set, windowsize, view, cofr, turn, perframe, save, alias, preset, open, runscript, remotecontrol, log. Also https://www.cgl.ucsf.edu/chimerax/docs/user/preferences.html, https://www.cgl.ucsf.edu/chimerax/docs/user/options.html, https://www.cgl.ucsf.edu/chimerax/docs/user/formats/defattr.html, the ChimeraX recipes at https://rbvi.github.io/chimerax-recipes/ , and Dawid Zyla's post https://www.dzyla.com/science/making-figures-manuscript-chimerax/ .
