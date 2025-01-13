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
