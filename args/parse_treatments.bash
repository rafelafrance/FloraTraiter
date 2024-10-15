#!/bin/bash

for path in data/treatments/*; do
  output=$(basename "$path")
  echo "$output"
  ./flora/parse_treatments.py \
      --treatment-dir="$path" \
      --html-file=data/output/html_output/"$output".html \
      --json-dir=data/output/json_output/"$output"_json \
      --csv-file=data/output/csv_output/"$output".csv
done
