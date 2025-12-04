#!/bin/bash

# --- Universal File Renamer Script ---
# This script renames ALL files in its current directory
# to a given prefix, while preserving their original extensions.
# Example: photo.jpg -> sample1.jpg, doc.png -> sample2.png

echo "Welcome to the Universal File Renamer!"
echo "WARNING: This script will try to rename *ALL* files in the folder where it is run."
echo "It will rename them to 'prefix1.ext', 'prefix2.ext', etc."
echo "It will NOT rename folders or itself."
echo "Please be careful! Backup your files first if they are important."
echo

# Get the script's own name to avoid renaming it
script_name=$(basename "$0")

# Ask the user for the file prefix
read -p "Enter the base name you want (e.g., 'sample'): " prefix

# Initialize a counter
i=1

# Loop through all items in the directory
# Using 'find . -maxdepth 1 -type f' is safer for filenames with spaces
find . -maxdepth 1 -type f | while read -r old_path; do
  
  # Remove the leading './' from find's output
  old_name=$(basename "$old_path")

  # --- Safety Checks ---
  # 1. Check that it's not this script file
  # (find already checks for file type, so no need for -f)
  if [ "$old_name" != "$script_name" ]; then

    # --- Get Extension ---
    extension="${old_name##*.}"
    
    new_name=""
    # Check if the file has an extension
    if [ "$extension" == "$old_name" ] && [ "${old_name:0:1}" != "." ]; then
      # File has NO extension (e.g., "README")
      new_name="${prefix}${i}"
    else
      # File has an extension (e.g., "image.jpg" or ".config")
      new_name="${prefix}${i}.${extension}"
    fi

    # --- Rename ---
    # Check if the new file name already exists to avoid overwriting
    if [ -f "$new_name" ]; then
      echo "SKIPPING: '$new_name' already exists. Cannot rename '$old_name'."
    else
      # Rename the file
      mv "$old_name" "$new_name"
      echo "Renamed: '$old_name'  ->  '$new_name'"
    fi

    # Increment the counter for the next file
    i=$((i + 1))
  fi
done

echo
echo "All done! $((i-1)) files were processed."