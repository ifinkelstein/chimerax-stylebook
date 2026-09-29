#!/usr/bin/env bash
# Make a small looping GIF from a rendered .mp4, for embedding in the
# README. GitHub will not autoplay an .mp4 linked from a repo README, so
# movies get a GIF preview next to the full-resolution file.
#
# Two-pass palette generation, because a GIF's 256 colours chosen per
# frame produce visible dithering noise on a white background.
#
# Usage:  scripts/gif.sh file.mp4 [width] [fps]
set -euo pipefail
src="$1"; w="${2:-360}"; fps="${3:-10}"
out="${src%.mp4}.gif"
pal="$(mktemp -t gifpal).png"
ffmpeg -v error -y -i "$src" -vf "fps=$fps,scale=$w:-1:flags=lanczos,palettegen=stats_mode=diff" "$pal"
ffmpeg -v error -y -i "$src" -i "$pal" \
  -lavfi "fps=$fps,scale=$w:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3" \
  -loop 0 "$out"
rm -f "$pal"
printf "%s  %s\n" "$out" "$(du -h "$out" | cut -f1)"
