# Working on this repo

- Every figure is a `.cxc` script in `examples/<nn>_<name>/figure.cxc`, rendered to a PNG in the same folder. Never produce a PNG by clicking.
- Re-render with `scripts/render.sh`. It uses the running ChimeraX over REST when one is listening on port 60000, because `chimerax --exit` hides errors.
- ChimeraX rejects trailing `#` comments on a command line. Comments go on their own line.
- `view pad` takes a small fraction (0.05 to 0.6). Larger values zoom out to nothing.
- Set `windowsize` before `view`, and save with only `width` so the aspect follows the window.
- Check `info chains` before writing a chain selection. Chain IDs are case sensitive and rarely the obvious letter.
- Colors come from `palettes/lab_colors.cxc` by semantic name. Do not write hex into a figure script.
- Use `key` for legends and `2dlabels` for text. `label` is per residue and must never be applied to a range.
- When adding a structure to an example, add its accession and primary citation to the credits table in README.md.
