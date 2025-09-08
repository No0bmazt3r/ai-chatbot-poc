# ==============================================================================
# GEMINI EMBEDDING PIPELINE FOR GOOGLE COLAB
# ==============================================================================
# This script is designed to be run in a single Google Colab cell.
# It performs the following steps:
# 1. Installs necessary Python libraries.
# 2. Converts a user-uploaded CSV file into a JSON file.
# 3. Generates text embeddings for each JSON record using the Gemini API.
# 4. Saves the final embeddings to a JSON file and triggers a download.
# ==============================================================================

# BLOCK 1: INSTALL DEPENDENCIES
# ------------------------------------------------------------------------------
# What it does:
# Installs the required Python libraries (`google-generativeai` for the Gemini API
# and `pandas` for data manipulation) directly into the Colab environment.
# The `-q` flag makes the installation "quiet" by reducing the output.
# Why it's here:
# Colab environments are temporary and don't come with all libraries pre-installed.
# This command ensures the script has the tools it needs to run.
# ------------------------------------------------------------------------------
print("BLOCK 1: Installing dependencies...")
!pip install google-generativeai pandas -q
print("Dependencies installed.")
print("="*50)


# BLOCK 2: IMPORT LIBRARIES AND CONFIGURE API KEY
# ------------------------------------------------------------------------------
# What it does:
# Imports all the necessary functions and classes from the installed libraries.
# It also retrieves the Gemini API key from Colab's secret manager and configures
# the `genai` library to use it for all subsequent API calls.
# Why it's here:
# This sets up the foundational tools and authentication needed for the script
# to interact with files and the Gemini API securely.
# ------------------------------------------------------------------------------
print("BLOCK 2: Importing libraries and configuring API key...")
import os
import google.generativeai as genai
import json
import pandas as pd
import time
from google.colab import userdata, files

# Retrieve the API key from Colab secrets
# IMPORTANT: Make sure you have a secret named "GEMINI_API_KEY" in your Colab notebook
api_key = userdata.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("API key configured.")
print("="*50)


# BLOCK 3: CONVERT CSV TO JSON
# ------------------------------------------------------------------------------
# What it does:
# Reads the `original.csv` file (which you should have uploaded to Colab)
# into a pandas DataFrame. It then converts this table-like structure into a
# list of JSON objects, where each object represents a row from the CSV.
# Finally, it saves this list to a new file named `output.json`.
# Why it's here:
# JSON is a more flexible format for handling semi-structured data and is easier
# to work with programmatically when preparing data for an API. This step
# standardizes the input for the embedding process.
# ------------------------------------------------------------------------------
print("BLOCK 3: Converting CSV to JSON...")
try:
    # Define the name of your CSV file. Change if yours is different.
    csv_file = "original.csv"
    df = pd.read_csv(csv_file)

    # Convert the DataFrame to a list of dictionaries (JSON records)
    data_json = df.to_dict(orient="records")

    # Write the JSON data to a file with nice formatting (indent=4)
    with open("output.json", "w") as f:
        json.dump(data_json, f, indent=4)

    print(f"CSV '{csv_file}' converted to 'output.json' with {len(data_json)} records.")
except FileNotFoundError:
    print(f"ERROR: The file '{csv_file}' was not found.")
    print("Please upload your CSV file to the Colab session storage.")
print("="*50)


# BLOCK 4: HELPER FUNCTIONS FOR EMBEDDING
# ------------------------------------------------------------------------------
# What they do:
# - `load_json_with_repair`: Safely loads the `output.json` file. If the JSON is
#   malformed (which can sometimes happen), it attempts a few common fixes.
# - `record_to_text`: Converts a single JSON object (a row) into a clean,
#   human-readable string. This string is what will be sent to Gemini.
# - `get_embedding`: Takes a text string, sends it to the Gemini embedding model
#   (`text-embedding-004`), and returns the resulting numerical vector.
# Why they're here:
# These functions break the complex process into small, manageable, and reusable
# pieces. This makes the main logic cleaner and easier to understand.
# ------------------------------------------------------------------------------
print("BLOCK 4: Defining helper functions...")

def load_json_with_repair(filename):
    """Loads a JSON file, attempting to repair it if it's malformed."""
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"Loaded {len(data)} records from '{filename}' normally.")
        return data
    except json.JSONDecodeError:
        print("JSON is malformed. Attempting a repair...")
        with open(filename, "r") as f:
            content = f.read()
        # Simple repair: try to fix common issues like trailing commas
        content = content.replace(',\n}', '\n}')
        try:
            data = json.loads(content)
            print(f"Repaired and loaded {len(data)} records.")
            return data
        except Exception as e:
            print(f"Auto-repair failed: {e}. Please check your JSON file.")
            return None

def record_to_text(record):
    """Converts a single JSON record into a descriptive text string."""
    parts = []
    for key, value in record.items():
        # Skip empty or null values to keep the text clean
        if pd.isna(value) or value is None or str(value).strip() == "":
            continue
        # Clean up keys and values for better readability
        clean_key = str(key).replace("_", " ")
        clean_value = str(value).replace("\n", " ")
        parts.append(f"{clean_key}: {clean_value}")
    return " | ".join(parts)

def get_embedding(text, model="models/text-embedding-004"):
    """Generates an embedding for a given text using the Gemini API."""
    try:
        # The API has a limit on text length; truncate if necessary
        if len(text) > 20000:
            text = text[:20000]
        # Call the Gemini API to get the embedding
        result = genai.embed_content(
            model=model,
            content=text,
            task_type="retrieval_document" # Specifies the use case for the embedding
        )
        return result['embedding']
    except Exception as e:
        print(f"Embedding generation failed: {e}")
        return []

print("Helper functions are ready.")
print("="*50)


# BLOCK 5: MAIN PROCESSING LOGIC
# ------------------------------------------------------------------------------
# What it does:
# This is the core of the script. It orchestrates the entire embedding process:
# 1. Calls `load_json_with_repair` to get the data.
# 2. Iterates through each record from the JSON file.
# 3. Uses `record_to_text` to prepare the data for the API.
# 4. Uses `get_embedding` to generate the embedding vector.
# 5. Bundles the original text, the vector, and some metadata into a new object.
# 6. Prints progress updates, including an estimated time of arrival (ETA).
# 7. Adds a small delay (`time.sleep`) to avoid overwhelming the API.
# 8. Saves the final list of embedded objects to `embeddings.json`.
# Why it's here:
# This block ties everything together and executes the main goal of the script.
# The progress updates are crucial for long-running tasks.
# ------------------------------------------------------------------------------
print("BLOCK 5: Starting the embedding generation process...")

def process_records(limit=10000):
    """Loads, processes, and generates embeddings for records up to a given limit."""
    data = load_json_with_repair("output.json")
    if not data:
        print("Halting process due to loading error.")
        return

    total_available = len(data)
    actual_limit = min(limit, total_available)
    data_to_process = data[:actual_limit]

    print(f"Processing {actual_limit:,} of {total_available:,} available records.")
    print("-" * 50)

    results = []
    start_time = time.time()

    for i, record in enumerate(data_to_process):
        text_to_embed = record_to_text(record)
        if not text_to_embed:
            print(f"Skipped record {i + 1} because it was empty after cleaning.")
            continue

        vector = get_embedding(text_to_embed)
        if not vector:
            print(f"Skipped record {i + 1} due to an embedding error.")
            continue

        # Structure the final output object
        result = {
            "id": i,
            "text": text_to_embed,
            "vector": vector,
            "metadata": {
                "year": record.get("Production Year"),
                "operator": record.get("Operator"),
                "county": record.get("County")
            }
        }
        results.append(result)

        # Log progress every 100 records
        if (i + 1) % 100 == 0:
            percentage = ((i + 1) / actual_limit) * 100
            elapsed = time.time() - start_time
            avg_time_per_record = elapsed / (i + 1)
            remaining_records = actual_limit - (i + 1)
            eta_minutes = (remaining_records * avg_time_per_record) / 60
            print(f"Progress: {i + 1:,}/{actual_limit:,} ({percentage:.1f}%) | ETA: {eta_minutes:.1f} min")

        # Rate limit: pause for 1 second every 10 records to be kind to the API
        if (i + 1) % 10 == 0:
            time.sleep(1)

    total_time_minutes = (time.time() - start_time) / 60
    print(f"\nProcessing complete in {total_time_minutes:.1f} minutes.")
    print(f"Generated {len(results):,} embeddings.")

    # Save the final results to a file
    with open("embeddings.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Embeddings saved to 'embeddings.json'.")

# Set the maximum number of records you want to process.
# For example, `process_records(1000)` will only process the first 1,000.
process_records(limit=10000)

print("="*50)


# BLOCK 6: DOWNLOAD THE FINAL FILE
# ------------------------------------------------------------------------------
# What it does:
# Uses Colab's `files` module to trigger a browser download for the
# `embeddings.json` file you just created.
# Why it's here:
# This is the easiest way to get the final, valuable output from the temporary
# Colab environment onto your local machine for storage or further use.
# ------------------------------------------------------------------------------
try:
    files.download("embeddings.json")
    print("Download for 'embeddings.json' initiated.")
except FileNotFoundError:
    print("Could not download 'embeddings.json' because the file was not created.")
print("="*50)
print("All steps completed!")