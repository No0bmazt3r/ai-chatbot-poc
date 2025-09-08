# Google Colab Implementation Guide

This guide explains how to use the provided Python script in Google Colab to convert a CSV file to JSON and then generate embeddings for each record using the Gemini API.

## 📝 Prerequisites

1.  **A Google Account**: To use Google Colab.
2.  **A Gemini API Key**: You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
3.  **Your CSV File**: The script assumes your file is named `original.csv`. If it has a different name, you will need to edit the script.

## 🚀 Steps to Run

### Step 1: Set Up Your Colab Notebook

1.  **Open Google Colab**: Go to [colab.research.google.com](https://colab.research.google.com) and create a new notebook.
2.  **Upload Your CSV**:
    *   On the left-hand side, click the **"Files"** icon (folder icon).
    *   Click the **"Upload to session storage"** button (file with an upward arrow).
    *   Select and upload your `original.csv` file.

### Step 2: Configure Your API Key

It is highly recommended to use Colab's **Secrets Manager** to keep your API key secure.

1.  Click the **"Key"** icon (key symbol) on the left sidebar.
2.  Click **"Add a new secret"**.
3.  **Name**: Enter `GEMINI_API_KEY`.
4.  **Value**: Paste your Gemini API key.
5.  **Enable the toggle** to make the secret available in this notebook.

### Step 3: Copy and Run the Code

1.  Copy the entire content of the `colab_embedding_pipeline.py` file.
2.  Paste it into a single cell in your Colab notebook.
3.  Run the cell by clicking the **"Play"** button or pressing **`Shift + Enter`**.

## 🔎 What the Script Does

The script will execute the following actions in order:

1.  **Install Libraries**: It will automatically install `google-generativeai` and `pandas` using `!pip`.
2.  **Convert CSV to JSON**: It reads `original.csv`, converts it into a structured JSON format, and saves it as `output.json` in your Colab environment.
3.  **Generate Embeddings**:
    *   It loads the `output.json` file.
    *   It processes each record, converting it into a clean text format.
    *   It sends the text to the Gemini API to get a numerical representation (embedding).
    *   It saves all the generated embeddings into a final `embeddings.json` file.
4.  **Download the Final File**: Once finished, it will automatically trigger a download prompt in your browser for the `embeddings.json` file.

You can monitor the progress in the output of the Colab cell.
