# ==============================================================================
# STEP 2: GENERATE EMBEDDINGS FROM JSON
# ==============================================================================
# What it does:
# This script loads the `output.json` file created by the previous script.
# It then iterates through each record, converts it into a clean text string,
# and calls the Gemini API to generate a numerical embedding for that text.
# The final output, including the text, vector, and metadata, is saved to
# `embeddings.json`.
#
# Why it's here:
# This is the core logic of the pipeline. It transforms your raw data into
# AI-ready vector embeddings, which can be used for search, retrieval-augmented
# generation (RAG), and other machine learning tasks.
#
# How to run:
# > python 2_generate_embeddings.py
# ==============================================================================

import os
import google.generativeai as genai
import json
import pandas as pd
import time
from dotenv import load_dotenv

# --- CONFIGURATION ---
# Load environment variables from a .env file (for the API key)
load_dotenv()

# The name of the JSON file to read from.
JSON_INPUT_FILE = "output_cleaned.json"
# The name of the final output file.
EMBEDDINGS_OUTPUT_FILE = "embeddings.json"
# The Gemini model to use for generating embeddings.
EMBEDDING_MODEL = "models/text-embedding-004"
# The maximum number of records to process. Set to a high number for all.
RECORD_LIMIT = 10000
# ---------------------


# BLOCK 1: SETUP API KEY
# ------------------------------------------------------------------------------
# What it does:
# Retrieves the Gemini API key from the environment variables and configures the
# `genai` library to use it. Using environment variables is a security best
# practice that avoids hard-coding secrets in your code.
# ------------------------------------------------------------------------------
print("BLOCK 1: Configuring API key...")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in environment variables.")
    print("👉 Please create a .env file and add: GEMINI_API_KEY='YOUR_KEY_HERE'")
else:
    genai.configure(api_key=api_key)
    print("✅ API key configured successfully.")
print("="*50)


# BLOCK 2: HELPER FUNCTIONS
# ------------------------------------------------------------------------------
# What they do:
# These functions modularize the script's logic, making it cleaner and more
# maintainable. Each function has a single, clear responsibility.
# ------------------------------------------------------------------------------
print("BLOCK 2: Defining helper functions...")

def load_json_file(filename):
    """Loads data from a specified JSON file."""
    if not os.path.exists(filename):
        print(f"❌ ERROR: JSON file '{filename}' not found.")
        print("👉 Please run the '1_convert_csv_to_json.py' script first.")
        return None
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data)} records from '{filename}'.")
        return data
    except json.JSONDecodeError:
        print(f"❌ ERROR: Could not decode JSON from '{filename}'. The file may be corrupt.")
        return None

def record_to_text(record):
    """Converts a single JSON record (dictionary) into a clean text string."""
    parts = []
    for key, value in record.items():
        if pd.isna(value) or value is None or str(value).strip() == "":
            continue
        clean_key = str(key).replace("_", " ")
        clean_value = str(value).replace("\n", " ")
        parts.append(f"{clean_key}: {clean_value}")
    return " | ".join(parts)

def get_embedding(text):
    """Generates an embedding for a given text string using the Gemini API."""
    try:
        if len(text) > 20000: # Truncate text to stay within API limits
            text = text[:20000]
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"\n❌ API call for embedding failed: {e}")
        return []

print("✅ Helper functions are ready.")
print("="*50)


# BLOCK 3: MAIN PROCESSING LOGIC
# ------------------------------------------------------------------------------
# What it does:
# This is the main function that orchestrates the entire embedding process.
# It loads the data, iterates through it, calls the helper functions to process
# each record, and saves the final result, while providing progress updates.
# ------------------------------------------------------------------------------
print("BLOCK 3: Starting the embedding generation process...")

def process_records():
    """Loads, processes, and generates embeddings for the records."""
    if not api_key: # Stop if the API key wasn't configured
        return

    data = load_json_file(JSON_INPUT_FILE)
    if not data:
        return

    total_available = len(data)
    actual_limit = min(RECORD_LIMIT, total_available)
    data_to_process = data[:actual_limit]

    print(f"📊 Processing {actual_limit:,} of {total_available:,} available records.")
    print("-" * 50)

    results = []
    start_time = time.time()

    for i, record in enumerate(data_to_process):
        text_to_embed = record_to_text(record)
        if not text_to_embed:
            print(f"⚠️ Skipped record #{i + 1} (was empty after cleaning).")
            continue

        vector = get_embedding(text_to_embed)
        if not vector:
            print(f"⚠️ Skipped record #{i + 1} (embedding generation failed).")
            continue

        # Assemble the final structured data for this record
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

        # Log progress every 100 records for user feedback
        if (i + 1) % 100 == 0:
            percentage = ((i + 1) / actual_limit) * 100
            elapsed = time.time() - start_time
            avg_time = elapsed / (i + 1)
            eta_minutes = (actual_limit - (i + 1)) * avg_time / 60
            print(f"🔥 Progress: {i + 1:,}/{actual_limit:,} ({percentage:.1f}%) | ETA: {eta_minutes:.1f} min")

        # Add a small delay every 10 records to avoid hitting API rate limits
        if (i + 1) % 10 == 0:
            time.sleep(1)

    total_time_minutes = (time.time() - start_time) / 60
    print(f"\n✅ Processing complete in {total_time_minutes:.1f} minutes.")
    print(f"✅ Generated {len(results):,} embeddings.")

    # Save the final list of results to the output file
    with open(EMBEDDINGS_OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Final embeddings saved to '{EMBEDDINGS_OUTPUT_FILE}'.")

# This ensures the main function is called when the script is run directly.
if __name__ == "__main__":
    process_records()
    print("="*50)
    print("🎉 All steps completed!")