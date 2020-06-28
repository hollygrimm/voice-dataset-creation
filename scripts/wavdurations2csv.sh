#!/bin/bash

echo "filename|duration" > wavdurations.csv;

for file in *.wav; do
    duration=$(eval soxi -D "$file");
    echo "${file}|$duration" >> wavdurations.csv;
done