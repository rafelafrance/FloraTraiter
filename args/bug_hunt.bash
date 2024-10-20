#!/bin/bash

for path in data/treatments/*; do
  output=$(basename "$path")
  echo "$output"
  ./flora/bug_hunt.py \
      --html-file=data/output/html_output/"$output".html \
      --csv-file=data/output/csv_output/"$output".csv
done
