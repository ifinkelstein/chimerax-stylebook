#!/usr/bin/env bash
# Post-process rendered PNGs: trim the uniform background border down to a
# fixed margin, then stamp 300 dpi metadata.
#
# ChimeraX frames a scene with its own padding and writes 144 dpi metadata,
# so a raw export wastes pixels on empty background and reports the wrong
# print resolution. Trimming raises the effective resolution at a given
# print width; the dpi stamp is metadata only and never resamples.
#
# A folder containing a file named .series holds panels that must stay
# comparable. Those are trimmed to one shared bounding box covering all of
# them, so the structures keep a common scale and register. Everything else
# is trimmed per file.
#
# Usage:  scripts/finish.sh [folder ...]     (default: all of examples/)
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
MARGIN="${MARGIN:-40}"     # px of background to keep on each side
DPI="${DPI:-300}"

[ $# -eq 0 ] && set -- "$REPO"/examples/*/

for d in "$@"; do
  d="${d%/}"
  pngs=("$d"/*.png)
  [ -e "${pngs[0]}" ] || continue
  echo "== $(basename "$d")"

  # A .series file may list the panel filenames that belong to the series,
  # one per line. Empty means every PNG in the folder.
  series=()
  if [ -f "$d/.series" ]; then
    while read -r line; do [ -n "$line" ] && series+=("$d/$line"); done < "$d/.series"
    [ ${#series[@]} -eq 0 ] && series=("${pngs[@]}")
    others=()
    for p in "${pngs[@]}"; do
      keep=1
      for s in "${series[@]}"; do [ "$p" = "$s" ] && keep=0; done
      [ $keep -eq 1 ] && others+=("$p")
    done
  fi

  if [ -f "$d/.series" ]; then
    # Union of every panel's content box, so all panels crop identically
    read -r ux uy uw uh < <(
      for p in "${series[@]}"; do
        magick "$p" -bordercolor "$(magick "$p" -format '%[pixel:p{0,0}]' info:)" \
          -border 1 -fuzz 2% -format "%@\n" info: | tr 'x+' ' '
      done | awk '{x1=$3; y1=$4; x2=$3+$1; y2=$4+$2;
                   if(NR==1||x1<mx)mx=x1; if(NR==1||y1<my)my=y1;
                   if(NR==1||x2>Mx)Mx=x2; if(NR==1||y2>My)My=y2}
                  END{print mx, my, Mx-mx, My-my}'
    )
    for p in "${series[@]}"; do
      magick "$p" -crop "${uw}x${uh}+${ux}+${uy}" +repage \
        -bordercolor "$(magick "$p" -format '%[pixel:p{0,0}]' info:)" -border "$MARGIN" \
        -units PixelsPerInch -density "$DPI" "$p"
    done
    for p in ${others[@]+"${others[@]}"}; do
      magick "$p" -bordercolor "$(magick "$p" -format '%[pixel:p{0,0}]' info:)" \
        -fuzz 2% -trim +repage -border "$MARGIN" \
        -units PixelsPerInch -density "$DPI" "$p"
    done
  else
    for p in "${pngs[@]}"; do
      magick "$p" -bordercolor "$(magick "$p" -format '%[pixel:p{0,0}]' info:)" \
        -fuzz 2% -trim +repage -border "$MARGIN" \
        -units PixelsPerInch -density "$DPI" "$p"
    done
  fi

  for p in "${pngs[@]}"; do
    identify -format "   %f  %wx%h  %x dpi\n" "$p"
  done
done
