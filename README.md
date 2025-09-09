# AI Chatbot Proof of Concept: Data Preparation Pipeline

This repository contains a Proof of Concept (POC) demonstrating a complete data preparation pipeline. The goal is to take raw data from a CSV file, process it, and convert it into vector embeddings suitable for use in an AI chatbot, semantic search application, or other Retrieval-Augmented Generation (RAG) systems.

The primary technologies used are **Python**, **Pandas**, and the **Google Gemini API** for embedding generation.

This guide provides two distinct implementation methods for this pipeline: a quick and easy approach using a single **Google Colab** notebook, and a more structured, local approach using **Visual Studio Code**.

---

## High-Level Workflow

![Data Preparation Workflow]("STEP 1/flow2.png")

The entire process is broken down into three main stages:

1.  **Convert CSV to JSON**: The initial `original.csv` data is converted into a more flexible `output.json` format. This structures the data for easier processing.

2.  **Clean JSON Data**: The raw JSON output may contain `NaN` values for empty fields, which is invalid in the strict JSON standard. This step cleans the file by replacing all `NaN` values with `null`, ensuring compatibility with databases and APIs. The result is saved as `output_cleaned.json`.

3.  **Generate Embeddings**: The cleaned text data is sent to the Google Gemini API (`text-embedding-004` model) to generate high-quality vector embeddings. The final output, `embeddings.json`, contains the original text, its corresponding vector, and relevant metadata.

---

## Method 1: Google Colab (Quickstart)

This method is ideal for quick testing and execution without any local setup. The entire pipeline is encapsulated in a single script designed to be run in one Colab cell.

**Public Colab Link for Immediate Testing: [CSV to Embeddings Pipeline](https://colab.research.google.com/drive/1_y-uXGNMpdQCpXXPoNmpOo6P1e_5Osno?usp=sharing)**

### 📝 Prerequisites

*   A Google Account.
*   A Google Gemini API Key, which you can obtain from [Google AI Studio](https://aistudio.google.com/app/apikey).
*   Your source CSV file ready on your computer.

### 🚀 Instructions

1.  **Open the Colab Notebook**: Use the link above or go to [colab.research.google.com](https://colab.research.google.com) and create a new notebook.
2.  **Configure API Key**: For security, add your Gemini API key to Colab's Secrets Manager.
    *   Click the **Key icon** on the left sidebar.
    *   Add a new secret named `GEMINI_API_KEY` and paste your key as the value.
    *   Ensure the toggle is enabled to make it accessible to the notebook.
3.  **Copy and Run Code**:
    *   Copy the entire contents of the script located at: `STEP 1/google_collab_implementation/colab_embedding_pipeline.py`.
    *   Paste the code into a single cell in your notebook.
4.  **Execute and Upload**:
    *   Run the cell. The script will first install dependencies.
    *   It will then display a file upload button. Click it and select the CSV file you want to process.

 The script will automatically execute the full CSV -> JSON -> Clean -> Embeddings workflow, and will trigger a download of the final `embeddings.json` file when complete.

---

## Method 2: VS Code (Local Development)

This method is suited for a local development environment and provides a more structured, multi-script approach.

### 📝 Prerequisites

*   Python (version 3.8+ recommended).
*   A Google Gemini API Key.
*   Your source CSV file, placed in the `STEP 1/vscode_implementation/` directory and named `original.csv`.

### 🚀 Instructions

1.  **Set Up Environment**:
    *   Navigate to the `STEP 1/vscode_implementation/` directory in your terminal.
    *   Create and activate a Python virtual environment (recommended):
        ```bash
        python -m venv .venv
        source .venv/bin/activate # On macOS/Linux
        # .\.venv\Scripts\activate # On Windows
        ```
    *   Install the required packages:
        ```bash
        pip install -r requirements.txt
        ```
2.  **Configure API Key**:
    *   In the same directory, create a file named `.env`.
    *   Add your API key to this file in the following format:
        ```
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```
3.  **Run the Scripts in Order**:
    Execute the following scripts from the `STEP 1/vscode_implementation/` directory one by one.

    1.  **Convert CSV to Raw JSON**:
        ```bash
        python 1_convert_csv.py
        ```
        *Output: `output.json`*

    2.  **Clean the JSON File**:
        ```bash
        python 2_clean_json.py
        ```
        *Output: `output_cleaned.json`*

    3.  **Generate Embeddings from Cleaned JSON**:
        ```bash
        python 3_generate_embeddings.py
        ```
        *Output: `embeddings.json`*

---

## Final Output: `embeddings.json`

The final output of this pipeline is a JSON file containing a list of objects, where each object is ready to be loaded into a vector database. The structure of each object is:

```json
{
  "id": 0,
  "text": "Production Year: 1995 | Operator: Buffalo China, Inc. | ...",
  "vector": [
    -0.0035424572,
    0.0684739,
    -0.01528264,
    ...
  ],
  "metadata": {
    "year": 1995,
    "operator": "Buffalo China, Inc.",
    "county": "Erie"
  }
}
```

This structured data is now optimized for semantic search and AI-driven chat applications.
