import yaml
import json
import jsonschema
from jsonschema import validate
import re
import os

# Load the .gitlab-ci.yml schema (you'll need to create this)
try:
    with open("gitlab-ci-schema.json", "r") as f:  # Create this file (see below)
        schema = json.load(f)
except FileNotFoundError:
    print("Error: gitlab-ci-schema.json not found. Please create it.")
    exit(1)
except json.JSONDecodeError:
    print("Error: Invalid JSON in gitlab-ci-schema.json.")
    exit(1)

def validate_yaml(yaml_file):
    try:
        with open(yaml_file, "r") as f:
            yaml_data = yaml.safe_load(f)

        if yaml_data is None:
            print(f"Warning: {yaml_file} is empty or contains only comments.")
            return True # Consider this valid to avoid errors on empty files

        validate(instance=yaml_data, schema=schema)

        # Custom validations beyond schema validation
        if not check_image_names(yaml_data):
          return False
        if not check_script_sections(yaml_data):
          return False
        if not check_cache_key(yaml_data):
          return False

        print(f"{yaml_file}: YAML is valid.")
        return True

    except yaml.YAMLError as e:
        print(f"{yaml_file}: YAML parsing error: {e}")
        return False
    except jsonschema.exceptions.ValidationError as e:
        print(f"{yaml_file}: YAML validation error: {e}")
        return False
    except Exception as e:
        print(f"{yaml_file}: An unexpected error occurred: {e}")
        return False

def check_image_names(yaml_data):
  if "image" in yaml_data:
    image_name = yaml_data["image"]
    if not re.match(r"^([a-zA-Z0-9-_.]+/)?([a-zA-Z0-9-_.]+)$", image_name):
      print(f"Invalid image name: {image_name}. Should match [repo/]<image> format")
      return False
  for stage in yaml_data.get("stages", []):
    stage_data = yaml_data.get(stage, {})
    if "image" in stage_data:
        image_name = stage_data["image"]
        if not re.match(r"^([a-zA-Z0-9-_.]+/)?([a-zA-Z0-9-_.]+)$", image_name):
            print(f"Invalid image name in stage {stage}: {image_name}. Should match [repo/]<image> format")
            return False
  return True

def check_script_sections(yaml_data):
    for stage in yaml_data.get("stages", []):
      stage_data = yaml_data.get(stage, {})
      if "script" in stage_data and not isinstance(stage_data["script"], list):
        print(f"Error: The 'script' section in stage '{stage}' must be a list.")
        return False
    return True

def check_cache_key(yaml_data):
    if "cache" in yaml_data:
        cache_data = yaml_data["cache"]
        if "key" in cache_data and not isinstance(cache_data["key"], str) and not isinstance(cache_data["key"], dict):
            print(f"Error: The 'key' section in 'cache' must be a string or a dictionary.")
            return False
    return True

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python gitlab_ci_linter.py <yaml_file1> <yaml_file2> ...")
        exit(1)

    yaml_files = sys.argv[1:]
    all_valid = True
    for yaml_file in yaml_files:
      if not os.path.exists(yaml_file):
        print(f"Error: File not found: {yaml_file}")
        all_valid = False
        continue
      if not validate_yaml(yaml_file):
          all_valid = False

    if all_valid:
        exit(0)  # Exit with success code if all files are valid
    else:
        exit(1)  # Exit with error code if any file is invalid
