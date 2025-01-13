# DevOps-Pipeline-Converter

**How to Use:**

1.  **Save:** Save the script to a file (e.g., `convert_ci.sh`).
2.  **Make Executable:** `chmod +x convert_ci.sh`
3.  **Run:**

    *   **Jenkinsfile:** `./convert_ci.sh Jenkinsfile .gitlab-ci.yml`
    *   **TeamCity:** `./convert_ci.sh teamcity.kts .gitlab-ci.yml teamcity`

**Important Considerations:**

*   **Complexity:** CI/CD configurations are complex. This script provides a *very basic* starting point. It will *not* handle all cases and will likely require significant manual adjustments to the generated `.gitlab-ci.yml` file.
*   **Jenkinsfile Conversion Limitations:** The current Jenkinsfile conversion handles only a small subset of Jenkinsfile syntax. More sophisticated parsing (e.g., using `awk`, `jq`, or a dedicated Groovy parser) would be needed for more accurate conversion.
*   **TeamCity Conversion Difficulty:** TeamCity uses a Kotlin-based DSL. Converting it to `.gitlab-ci.yml` is a very complex task and would likely require a dedicated parser for the Kotlin DSL. A simple `sed` approach is not sufficient. Consider using a more robust approach like writing a Kotlin program or using a more advanced scripting language such as Python.
*   **Manual Adjustments:** You *must* review and adjust the generated `.gitlab-ci.yml` file.
