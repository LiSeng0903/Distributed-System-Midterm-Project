#!/bin/bash

num=$1

alphabet=({a..z})

for ((i=0; i<num; i++)); do
  if [ $i -ge ${#alphabet[@]} ]; then
    echo "Error: The input number exceeds the alphabet limit (26)."
    exit 1
  fi
  filename="${alphabet[i]}.txt"
  python3 generate_random_file.py 10 "$output_dir/$filename"
done
