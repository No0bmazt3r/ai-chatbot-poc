# ==============================================================================
# STEP 1: CONVERT CSV TO JSON
# ==============================================================================
# What it does:
# This script loads a CSV file named 'original.csv' using the pandas library,
# converts its contents into a structured JSON format (a list of records),
# and saves the result to a file named 'output.json'.
#
# Why it's here:
# This is the first step in the data preparation pipeline. Converting the data
# from a tabular CSV format to a semi-structured JSON format makes it much
# easier to process each row as a distinct 'document' for the subsequent
# embedding step.
#
# How to run:
# > python 1_convert_csv_to_json.py
# ==============================================================================

import pandas as pd
import json
import os

# --- CONFIGURATION ---
# The name of the input CSV file. Make sure this file is in the same directory.
CSV_FILE = "original.csv"
# The name of the output JSON file that will be created.
JSON_OUTPUT_FILE = "output.json"
# ---------------------

def convert_csv_to_json():
    """Reads a CSV file and writes its content to a JSON file."""
    print(f"Starting conversion of '{CSV_FILE}' to JSON...")

    # Check if the CSV file actually exists before trying to read it.
    if not os.path.exists(CSV_FILE):
        print(f"\nERROR: The file '{CSV_FILE}' was not found in this directory.")
        print("Please add your CSV file to this folder and name it correctly.")
        return

    try:
        # Load the CSV file into a pandas DataFrame.
        # A DataFrame is a powerful, table-like data structure.
        df = pd.read_csv(CSV_FILE)

        # Convert the DataFrame to a list of dictionaries.
        # The `orient="records"` argument specifies the format: `[{column: value}, ...]`
        data_json = df.to_dict(orient="records")

        # Write the JSON data to the output file.
        # `with open(...)` ensures the file is properly closed even if errors occur.
        # `json.dump` serializes the Python list into a JSON formatted string.
        # `indent=4` makes the JSON file human-readable with pretty-printing.
        with open(JSON_OUTPUT_FILE, "w") as f:
            json.dump(data_json, f, indent=4)

        print(f"Success! Converted {len(data_json):,} records.")
        print(f"Output saved to '{JSON_OUTPUT_FILE}'.")

    except Exception as e:
        # Catch any other potential errors during file processing.
        print(f"\nAn unexpected error occurred: {e}")

# This block ensures that the `convert_csv_to_json` function is called only
# when the script is executed directly (not when imported as a module).
if __name__ == "__main__":
    convert_csv_to_json()