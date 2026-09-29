#!/usr/bin/env bash
# Render every examples/*/figure.cxc (or the folders given as arguments).
#
# If a ChimeraX with REST control is running (startup.cxc enables it on
# port 60000), each script runs in that session and errors are printed.
# Otherwise each script runs in a fresh `chimerax --exit` process. macOS
# has no OSMesa, so --nogui cannot save images; the GUI must exist.
#
# Usage:  scripts/render.sh                 # all examples
#         scripts/render.sh examples/03_*   # a subset
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
CHIMERAX="${CHIMERAX:-$(command -v chimerax || echo /Applications/ChimeraX.app/Contents/MacOS/ChimeraX)}"
PORT="${CHIMERAX_PORT:-60000}"

if [ $# -eq 0 ]; then
  set -- "$REPO"/examples/*/
fi

live=0
if curl -s -o /dev/null "http://127.0.0.1:${PORT}/run?command=version"; then live=1; fi

fail=0
for d in "$@"; do
  d="$(cd "$d" && pwd)"
  [ -f "$d/figure.cxc" ] || { echo "skip $d (no figure.cxc)"; continue; }
  echo "== $(basename "$d")"
  if [ $live -eq 1 ]; then
    out="$(curl -s -G "http://127.0.0.1:${PORT}/run" --data-urlencode "command=close session; cd $d; open figure.cxc")"
    if echo "$out" | grep -qiE "error|expected|unknown|invalid|traceback"; then
      echo "$out" | grep -iE "error|expected|unknown|invalid|traceback" -B3 -A3
      fail=1
    fi
  else
    ( cd "$d" && "$CHIMERAX" --exit figure.cxc >/dev/null 2>&1 )
  fi
  for png in "$d"/*.png; do
    [ -f "$png" ] || continue
    if [ ! -s "$png" ]; then echo "   EMPTY $png"; fail=1; fi
  done

  # Trim the background border and stamp 300 dpi. ChimeraX pads its own
  # framing and writes 144 dpi, so a raw export wastes pixels and reports
  # the wrong print resolution.
  [ "${NO_FINISH:-0}" = "1" ] || bash "$REPO/scripts/finish.sh" "$d" >/dev/null
done
exit $fail
