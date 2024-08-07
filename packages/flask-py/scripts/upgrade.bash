#!/bin/bash

# Skip the header line and read the rest of the file
tail -n +2 outdated.txt | while read -r line; do
    # Extract the package name (first column)
    package_name=$(echo $line | awk '{print $1}')
    echo "Upgrading $package_name"
    pip install --upgrade $package_name
done
