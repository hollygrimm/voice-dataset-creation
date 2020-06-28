#!/bin/bash

find wavs/ -type f -name "*.wav" -exec sh -c '
for wavfilepath; do
    outputwavfilepath=wavs_22050/${wavfilepath#wavs/}
    echo $outputwavfilepath
    ffmpeg -i ${wavfilepath}  -ar 22050 -ac 1 -f wav -y ${outputwavfilepath};
done
' _ {} +