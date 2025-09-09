# STEP 3.2: Full Setup - Database, Data Import, and Vector Index

This guide details the full setup process for MongoDB Atlas. You will create your database structure, connect to it, import the data generated in STEP 1, and create the essential vector search index.

---

## Part 1: Download and Install MongoDB Compass

MongoDB Compass is the official graphical user interface (GUI) for MongoDB. It allows you to easily manage your database, import data, and build indexes.

1.  **Go to the Download Page**:
    *   Visit the official [MongoDB Compass Download Page](https://www.mongodb.com/try/download/compass).

2.  **Download and Install**:
    *   The website should automatically detect your operating system (Windows, macOS, or Linux).
    *   Download the installer and follow the on-screen instructions to install it.

---

## Part 2: Create Database and Collections in Atlas

Before connecting, create the database and collections directly within the MongoDB Atlas web interface.

1.  **Navigate to Database Deployments**:
    *   Log in to your [MongoDB Atlas account](https://cloud.mongodb.com/).
    *   On the main screen, click the **"Browse Collections"** button for your cluster.

2.  **Create the Database and Collections**:
    *   Click the **"Create Database"** button.
    *   Enter the following names:
        *   **Database Name**: `vector_db`
        *   **Collection Name**: `documents`
    *   Click **"Create"**.
    *   Hover over your new `vector_db` database on the left and click the **`+`** sign to create a second collection named `embeddings`.

---

## Part 3: Connect and Import Data with Compass

Now, you will connect to your database and import the JSON files from STEP 1.

1.  **Get Connection String**: In Atlas, click **"Connect"** on your cluster, select **"Compass"**, and copy the connection string.
2.  **Connect in Compass**: Open Compass, paste the string, **replace `<password>` with your database user's password**, and connect.
3.  **Import `output_cleaned.json`**: 
    *   In Compass, select the `vector_db.documents` collection.
    *   Go to the menu **Collection > Import Data**.
    *   Select the `output_cleaned.json` file from the `STEP 1/vscode_implementation` directory and click **"Import"**.
4.  **Import `embeddings.json`**: 
    *   Select the `vector_db.embeddings` collection.
    *   Go to **Collection > Import Data**.
    *   Select the `embeddings.json` file from `STEP 1/vscode_implementation` and click **"Import"**.

---

## Part 4: Create the Vector Search Index

This final, crucial step creates the index that enables semantic search on your newly imported embeddings.

1.  In Compass, ensure you have the `vector_db.embeddings` collection selected.
2.  Click on the **"Indexes"** tab.
3.  Click **"Create Index"**.
4.  Select the **"JSON Editor"** tab and paste in the following configuration:

    ```json
    {
      "fields": [
        {
          "type": "vector",
          "path": "vector",
          "numDimensions": 768,
          "similarity": "cosine"
        },
        {
          "type": "filter",
          "path": "metadata.year"
        },
        {
          "type": "filter",
          "path": "metadata.operator"
        },
        {
          "type":- "filter",
          "path": "metadata.county"
        }
      ]
    }
    ```

5.  **Index Name**: Give the index a name, such as `vector_index`.
6.  Click **"Create Index"**. The index will now build in the background.

### Understanding the Index Configuration:
*   `"path": "vector"`: Tells Atlas to index the `vector` field from our `embeddings.json` data.
*   `"numDimensions": 768`: This number is critical. It **must exactly match the output dimension of the embedding model** used to generate the vectors. The Google model we used in STEP 1, `text-embedding-004`, produces vectors with **768 dimensions**.
*   `"similarity": "cosine"`: Defines the algorithm to use for comparing vectors. Cosine similarity is a standard and effective choice for text-based semantic search.
*   `"type": "filter"`: We are also making the fields inside our `metadata` object searchable, so you can filter your vector search queries (e.g., find similar documents but only from a specific `year`).

---

## ✅ Full Setup Complete

Congratulations! Your MongoDB Atlas database is now fully configured, populated with your local data, and equipped with a powerful vector search index. It is ready to be used as the backend for your AI application.
