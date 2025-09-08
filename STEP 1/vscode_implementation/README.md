# VS Code Implementation Guide

This guide explains how to run the Python scripts in your local VS Code environment to convert a CSV file and generate Gemini embeddings.

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

3.  The Python script `2_generate_embeddings.py` is already set up to load this variable automatically.

### Step 3: Run the Scripts in Order

You must run the scripts one after the other.

1.  **First, convert the CSV to JSON**:
    ```bash
    python 1_convert_csv_to_json.py
    ```
    This will create an `output.json` file.

2.  **Next, generate the embeddings**:
    ```bash
    python 2_generate_embeddings.py
    ```
    This will read `output.json` and create the final `embeddings.json` file.

## ✅ Expected Outcome

After running both scripts, you will have two new files in your directory:

*   `output.json`: The intermediate JSON representation of your CSV.
*   `embeddings.json`: The final output containing the text, embedding vectors, and metadata for each record.
