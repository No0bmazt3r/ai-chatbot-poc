# VS Code Implementation Guide

This guide explains how to run the Python scripts in your local VS Code environment to convert a CSV file, clean the resulting JSON, and generate Gemini embeddings.

## High-Level Workflow

![Data Preparation Workflow](../flow2.png)

## 📝 Prerequisites

1.  **Python**: Make sure Python is installed on your system (version 3.8 or newer is recommended).
2.  **A Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
3.  **Your CSV File**: Place your CSV file in this directory and name it `original.csv`.

## 🚀 Steps to Run

### Step 1: Set Up Your Project

1.  **Open this Folder in VS Code**: Open the `vscode_implementation` folder directly in VS Code.
2.  **Create a Virtual Environment (Recommended)**:
    Open the VS Code terminal (`Ctrl + ``) and run:
    ```bash
    python -m venv .venv
    ```
    Activate it:
    *   **Windows**: `.\.venv\Scripts\activate`
    *   **macOS/Linux**: `source .venv/bin/activate`

3.  **Install Dependencies**:
    In the same terminal, run:
    ```bash
    pip install -r requirements.txt
    ```

### Step 2: Configure Your API Key

For security, you should **never** hard-code your API key in a script. Use an environment variable.

1.  **Create a `.env` file** in this directory.
2.  **Add your API key** to the file like this:

    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

3.  The embedding script is already set up to load this variable automatically.

### Step 3: Run the Scripts in Order

You must run the scripts one after the other.

1.  **First, convert the CSV to JSON**:
    ```bash
    python 1_convert_csv.py
    ```
    This will create an `output.json` file, which may contain `NaN` values.

2.  **Next, clean the JSON file**:
    ```bash
    python 2_clean_json.py
    ```
    This reads `output.json` and creates a valid `output_cleaned.json` by replacing `NaN` with `null`.

3.  **Finally, generate the embeddings**:
    ```bash
    python 3_generate_embeddings.py
    ```
    This will read the cleaned JSON and create the final `embeddings.json` file.

## ✅ Expected Outcome

After running all scripts, you will have three new files:

*   `output.json`: The raw, intermediate JSON (with `NaN`).
*   `output_cleaned.json`: The cleaned, valid JSON (with `null`).
*   `embeddings.json`: The final output with text, vectors, and metadata.
