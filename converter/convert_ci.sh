#!/bin/bash

# Function to convert Jenkinsfile to .gitlab-ci.yml
convert_jenkinsfile() {
  local jenkinsfile="$1"
  local output_file="$2"

  if [[ ! -f "$jenkinsfile" ]]; then
    echo "Error: Jenkinsfile '$jenkinsfile' not found."
    return 1
  fi

  echo "Converting Jenkinsfile '$jenkinsfile' to '$output_file'..."

  # Basic conversion logic (highly simplified and requires significant improvement)
  sed -E 's/pipeline {/stages:/g' "$jenkinsfile" \
    | sed -E 's/agent any/image: docker:latest/g' \
    | sed -E 's/stages {/before_script:/g' \
    | sed -E 's/stage\(\'([^\']+)\'\) {/  -\1/g' \
    | sed -E 's/steps {/script:/g' \
    | sed -E 's/sh \'([^\']+)\'/    - \1/g' \
    | sed -E 's/}/ /g' \
    > "$output_file"

  echo "Conversion finished (basic). Output written to '$output_file'."
}

# Function to convert TeamCity DSL to .gitlab-ci.yml (very basic stub)
convert_teamcity() {
  local teamcity_dsl="$1"
  local output_file="$2"

  if [[ ! -f "$teamcity_dsl" ]]; then
    echo "Error: TeamCity DSL file '$teamcity_dsl' not found."
    return 1
  fi

  echo "Converting TeamCity DSL '$teamcity_dsl' to '$output_file' (very basic)..."

  # This is a placeholder. TeamCity DSL conversion is complex.
  echo "# Conversion from TeamCity DSL is not yet implemented effectively." > "$output_file"
  echo "# Manual adjustments are REQUIRED." >> "$output_file"
  cat "$teamcity_dsl" >> "$output_file" # Just copy the input for now

  echo "Conversion finished (very basic). Output written to '$output_file'."
}


# Main script
if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <input_file> <output_file> [type]"
  echo "       type: jenkins (default), teamcity"
  exit 1
fi

input_file="$1"
output_file="$2"
type="${3:-jenkins}" # Default to Jenkinsfile

case "$type" in
  jenkins)
    convert_jenkinsfile "$input_file" "$output_file"
    ;;
  teamcity)
    convert_teamcity "$input_file" "$output_file"
    ;;
  *)
    echo "Error: Invalid type '$type'. Must be 'jenkins' or 'teamcity'."
    exit 1
    ;;
esac

exit 0
