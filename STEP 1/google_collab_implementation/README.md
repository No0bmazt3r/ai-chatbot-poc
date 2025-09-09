# Google Colab Implementation Guide

This guide explains how to use the provided Python script in Google Colab to convert a CSV file to JSON and then generate embeddings for each record using the Gemini API.

## High-Level Workflow

![Data Preparation Workflow](flow2.png)

## 📝 Prerequisites

1.  **A Google Account**: To use Google Colab.
2.  **A Gemini API Key**: You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
3.  **Your CSV File**: Have your CSV file ready on your local machine.

## 🚀 Steps to Run

### Step 1: Set Up Your Colab Notebook

1.  **Open Google Colab**: Go to [colab.research.google.com](https://colab.research.google.com) and create a new notebook.
2.  **Prepare Your CSV**: Have your CSV file ready on your computer. You do not need to upload it manually; the script will prompt you to do so.

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
4.  When prompted, click the **"Choose Files"** button and select your CSV file.

## 🔎 What the Script Does

The script will execute the following actions in order:

1.  **Install Libraries**: It will automatically install `google-generativeai` and `pandas`.
2.  **Prompt for Upload**: It will display a button to let you upload your CSV file.
3.  **Convert CSV to JSON**: It reads the uploaded CSV, converts it into a structured JSON format, and saves it as `output.json`.
4.  **Generate Embeddings**:
    *   It loads the `output.json` file.
    *   It processes each record, converting it into a clean text format.
    *   It sends the text to the Gemini API to get a numerical representation (embedding).
    *   It saves all the generated embeddings into a final `embeddings.json` file.
5.  **Download the Final File**: Once finished, it will automatically trigger a download prompt in your browser for the `embeddings.json` file.

You can monitor the progress in the output of the Colab cell.
