# ==============================================================================
# STEP 3: CLEAN JSON (NaN to null)
# ==============================================================================
# What it does:
# This script reads the `output.json` file, which may contain non-standard `NaN`
# values, and converts them to the standard JSON `null` value. It then saves
# the cleaned data to a new file, `output_cleaned.json`.
#
# Why it's necessary:
# The official JSON specification does not include `NaN` (Not a Number).
# Strict JSON parsers and vector databases will fail if they encounter `NaN`.
# The correct representation for a missing value in JSON is `null`. This script
# ensures the file is compliant before the embedding step.
#
# How to run:
# > python 3_clean_json.py
# ==============================================================================

import json

# --- CONFIGURATION ---
INPUT_FILENAME = "output.json"
OUTPUT_FILENAME = "output_cleaned.json"
# ---------------------

def clean_json_nan_values():
    """Reads a JSON file, replaces NaN with null, and saves to a new file."""
    print(f"Starting the cleaning process for '{INPUT_FILENAME}'...")

    try:
        print(f"Step 1: Reading raw content from '{INPUT_FILENAME}'.")
        with open(INPUT_FILENAME, 'r') as f:
            raw_content = f.read()

        print("Step 2: Replacing all occurrences of 'NaN' with 'null'.")
        cleaned_content = raw_content.replace('NaN', 'null')

        print("Step 3: Validating the cleaned content...")
        try:
            json.loads(cleaned_content)
            print("Validation successful. The content is now valid JSON.")
        except json.JSONDecodeError as e:
            print(f"ERROR: Validation failed after replacement: {e}")
            return

        print(f"Step 4: Saving the cleaned data to '{OUTPUT_FILENAME}'.")
        with open(OUTPUT_FILENAME, 'w') as f:
            f.write(cleaned_content)

        print(f"\nSuccess! Cleaned JSON saved to '{OUTPUT_FILENAME}'.")

    except FileNotFoundError:
        print(f"ERROR: The input file '{INPUT_FILENAME}' was not found. Run step 1 first.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    clean_json_nan_values()
