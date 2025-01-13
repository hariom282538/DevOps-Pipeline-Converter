````markdown
# GitLab CI Linter (Python)

This tool validates GitLab CI configuration files (`.gitlab-ci.yml`) to ensure they adhere to proper syntax, structure, and best practices. It uses a JSON schema for robust validation and includes custom checks for common issues.

## Features

*   **YAML Syntax Validation:** Uses `PyYAML` for parsing and checking YAML syntax.
*   **Schema Validation:** Validates the structure and content of `.gitlab-ci.yml` files against a JSON schema using `jsonschema`.
*   **Custom Validation Rules:** Includes custom checks for:
    *   **Image Names:** Validates image names against the `[registry/][image]` format.
    *   **Script Sections:** Ensures that `script` sections are lists.
    *   **Cache Keys:** Verifies that `cache:key` is either a string or a dictionary.
*   **Multiple File Support:** Can validate multiple `.gitlab-ci.yml` files at once.
*   **Clear Error Reporting:** Provides informative error messages with file names and line numbers.
*   **Exit Codes:** Returns 0 for success (all files valid) and 1 for failure (any file invalid).

## Requirements

*   Python 3.6+
*   `PyYAML`
*   `jsonschema`

## Installation

```bash
pip install pyyaml jsonschema
````

## Usage

```bash
python gitlab_ci_linter.py <yaml_file1> <yaml_file2> ...
```

Example:

```bash
python gitlab_ci_linter.py .gitlab-ci.yml
python gitlab_ci_linter.py .gitlab-ci.yml other-config.yml
```

## Creating/Extending the Schema (`gitlab-ci-schema.json`)

The linter relies on a JSON schema (`gitlab-ci-schema.json`) to define the structure of valid `.gitlab-ci.yml` files. A *partial* schema is included in this repository. You'll likely need to extend it to cover all the features you use in your GitLab CI configurations.

Here's how you can approach it:

1.  **Start with the provided `gitlab-ci-schema.json`:** It covers the basics (stages, image, script, variables, cache).
2.  **Consult the GitLab CI documentation:** The official GitLab CI documentation is the best source of information about the valid syntax and options.
3.  **Use a JSON schema editor or generator:** There are online tools and IDE extensions that can help you create and edit JSON schemas.
4.  **Iteratively add properties:** Start by adding properties for the features you use most frequently. Test the linter after each addition to ensure it's working as expected.

**Example Schema Extension (Adding `services`):**

```json
{
  // ... existing schema ...
  "properties": {
    // ... other properties ...
    "services": {
      "type": "array",
      "items": {
        "oneOf": [
          {"type": "string"},
          {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "alias": {"type": "string"},
              "entrypoint": {"type": "array", "items": {"type": "string"}},
              "command": {"type": "array", "items": {"type": "string"}}
            },
            "additionalProperties": true
          }
        ]
      }
    }
  },
  // ... rest of schema ...
}
```

## Contributing

Contributions are welcome\! Please open an issue or submit a pull request.

## License

[MIT License](https://www.google.com/url?sa=E&source=gmail&q=LICENSE) (or your preferred license)

````

**Expanded `gitlab-ci-schema.json` (More Complete):**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "image": { "oneOf": [{ "type": "string" }, { "type": "object" }] },
    "services": {
      "type": "array",
      "items": {
        "oneOf": [
          {"type": "string"},
          {"type": "object", "additionalProperties": true}
        ]
      }
    },
    "stages": { "type": "array", "items": { "type": "string" } },
    "variables": { "type": "object", "additionalProperties": true },
    "before_script": { "type": "array", "items": { "type": "string" } },
    "after_script": { "type": "array", "items": { "type": "string" } },
    "cache": {
      "type": "object",
      "properties": {
        "key": { "oneOf": [{ "type": "string" }, { "type": "object" }] },
        "paths": { "type": "array", "items": { "type": "string" } },
        "policy": { "type": "string", "enum": ["push", "pull", "pull-push"] }
      },
      "additionalProperties": true
    },
    "include": {
      "type": "array",
      "items": {
        "oneOf": [
          {"type": "string"},
          {"type": "object", "additionalProperties": true}
        ]
      }
    },
    "default": { "type": "object", "additionalProperties": true },
    "workflow": { "type": "object", "additionalProperties": true }
  },
  "patternProperties": {
    "^[a-zA-Z0-9-_]+$": { # Stage/Job names
      "type": "object",
      "properties": {
        "stage": { "type": "string" },
        "script": { "type": "array", "items": { "type": "string" } },
        "image": { "oneOf": [{ "type": "string" }, { "type": "object" }] },
        "services": {
          "type": "array",
          "items": {
            "oneOf": [
              {"type": "string"},
              {"type": "object", "additionalProperties": true}
            ]
          }
        },
        "only": { "oneOf": [{ "type": "array", "items": { "type": "string" } }, { "type": "object" }] },
        "except": { "oneOf": [{ "type": "array", "items": { "type": "string" } }, { "type": "object" }] },
        "variables": { "type": "object", "additionalProperties": true },
        "cache": {
          "type": "object",
          "properties": {
            "key": { "oneOf": [{ "type": "string" }, { "type": "object" }] },
            "paths": { "type": "array", "items": { "type": "string" } },
            "policy": { "type": "string", "enum": ["push", "pull", "pull-push"] }
          },
          "additionalProperties": true
        },
        "artifacts": { "type": "object", "additionalProperties": true },
        "dependencies": { "type": "array", "items": { "type": "string" } },
        "before_script": { "type": "array", "items": { "type": "string" } },
        "after_script": { "type": "array", "items": { "type": "string" } },
        "allow_failure": { "type": ["boolean", "string"] },
        "when": { "type": "string", "enum": ["on_success", "on_failure", "always", "manual"] },
        "environment": { "oneOf": [{ "type": "string" }, { "type": "object" }] },
        "timeout": { "type": ["string", "integer"] },
        "trigger": { "type": "object", "additionalProperties": true },
        "rules": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": true
            }
        }
      },
      "additionalProperties": true
    }
  },
  "additionalProperties": true
}
````
