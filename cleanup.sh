#!/bin/bash

FOLDERS=("data" "results" "logs")

for folder in "${FOLDERS[@]}"; do
  echo "Cleaning $folder/"
  if [ -d "$folder" ]; then
    find "$folder" -mindepth 1 -exec rm -rf {} +
    echo "✔ $folder/ cleaned"
  else
    echo "⚠ $folder/ does not exist"
  fi
done
