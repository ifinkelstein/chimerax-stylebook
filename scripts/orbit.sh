#!/usr/bin/env bash
# Render a ring of candidate orientations for a figure and stitch them
# into one contact sheet, so you can pick a view by looking instead of
# guessing. Especially worth it for active-site zooms, where one helix in
# the wrong place hides the thing the panel is about.
#
# Requires a ChimeraX listening on the REST port (startup.cxc does that).
#
# Usage:  scripts/orbit.sh examples/16_active_site [n] [axis]
#         n     number of views around the circle (default 8)
#         axis  y (default) or x
set -euo pipefail
dir="$(cd "$1" && pwd)"; n="${2:-8}"; axis="${3:-y}"
port="${CHIMERAX_PORT:-60000}"
tmp="$(mktemp -d)"
step=$((360 / n))

cmd="close session; cd $dir; open figure.cxc; 2dlabels delete all"
for i in $(seq 0 $((n - 1))); do
  [ "$i" -gt 0 ] && cmd="$cmd; turn $axis $step"
  cmd="$cmd; save $tmp/v$(printf %02d "$i").png width 560"
done
curl -s -G "http://127.0.0.1:${port}/run" --data-urlencode "command=$cmd" \
  | grep -iE "^error|Expected" || true

# Four per row, appended without montage so no font is needed
out="$dir/orbit.png"
rows=()
i=0
while [ $i -lt "$n" ]; do
  set -- $(ls "$tmp"/v*.png | sed -n "$((i + 1)),$((i + 4))p")
  magick "$@" +append "$tmp/row$i.png"
  rows+=("$tmp/row$i.png")
  i=$((i + 4))
done
magick "${rows[@]}" -append "$out"
rm -rf "$tmp"
echo "$out  (each tile is $axis rotated $step degrees from the previous)"
