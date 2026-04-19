#!/usr/bin/env bash
# Resample every WAV under wavs/ to 22.05 kHz mono into wavs_22050/.
set -euo pipefail

src_dir="wavs"
dst_dir="wavs_22050"

if [[ ! -d "$src_dir" ]]; then
    echo "Source directory '$src_dir' not found." >&2
    exit 1
fi

mkdir -p "$dst_dir"

find "$src_dir" -type f -name "*.wav" -print0 \
    | while IFS= read -r -d '' wavfilepath; do
        rel="${wavfilepath#"$src_dir"/}"
        outputwavfilepath="$dst_dir/$rel"
        mkdir -p "$(dirname -- "$outputwavfilepath")"
        echo "$outputwavfilepath"
        ffmpeg -nostdin -i "$wavfilepath" -ar 22050 -ac 1 -f wav -y "$outputwavfilepath"
    done
