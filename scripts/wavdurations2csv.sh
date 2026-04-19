#!/usr/bin/env bash
# Write a pipe-separated filename|duration CSV for every .wav in the CWD.
set -euo pipefail

out="wavdurations.csv"
echo "filename|duration" > "$out"

shopt -s nullglob
for file in *.wav; do
    duration=$(soxi -D -- "$file")
    printf '%s|%s\n' "$file" "$duration" >> "$out"
done
