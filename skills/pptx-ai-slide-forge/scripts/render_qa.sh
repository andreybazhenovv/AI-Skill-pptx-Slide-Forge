#!/usr/bin/env bash
# pptx-ai-slide-forge :: render deck slides to PNG for visual QA.
#
# Usage:
#   ./render_qa.sh /abs/path/deck.pptx [outdir]
#
# Renders via Keynote (AppleScript). Output naming (IMPORTANT):
#   Keynote names files after the OUTPUT DIRECTORY basename, not the deck:
#   <outdir>/<outdir-basename>.001.png, .002.png, ... (one per slide)
#   e.g. outdir "qa" → qa/qa.001.png; outdir "qa3" → qa3/qa3.001.png.
#
# KNOWN PITFALL (verified 2026-10-29, macOS): Microsoft PowerPoint's AppleScript
#   `save ... as save as PNG`
# exits 0 but silently writes NOTHING (destination folder and the app's sandbox
# container both stay empty). Do not retry PowerPoint — use this Keynote path.
# Keynote re-interprets the pptx, so line wraps can differ slightly from
# PowerPoint; leave width buffers on text boxes when building (see
# references/qa-and-toolchain.md).
#
# LibreOffice (`soffice`) and poppler (`pdftoppm`) are NOT required by this skill.

set -euo pipefail

DECK="${1:?usage: render_qa.sh /abs/path/deck.pptx [outdir]}"
OUT="${2:-qa}"

if [ ! -f "$DECK" ]; then
    echo "deck not found: $DECK" >&2
    exit 2
fi

mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"
DECK="$(cd "$(dirname "$DECK")" && pwd)/$(basename "$DECK")"

osascript <<EOF
tell application "Keynote"
  activate
  open (POSIX file "$DECK")
  delay 6
  export front document to POSIX file "$OUT" as slide images with properties {image format:PNG, all stages:false, skipped slides:true}
  delay 3
  close front document without saving
  quit
end tell
EOF

BASE="$(basename "$OUT")"
echo "renders: $OUT/$BASE.001.png, $BASE.002.png, ..."
