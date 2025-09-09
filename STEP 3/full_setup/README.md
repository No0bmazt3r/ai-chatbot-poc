# STEP 3.2: Full Setup - Database, Data Import, and Vector Index

This guide details the full setup process for MongoDB Atlas. You will create your database structure, connect to it, import the data generated in STEP 1, and create the essential vector search index.

---

## Part 1: Create Database and Collections in Atlas

Before connecting, it's best to create the database and collections directly within the MongoDB Atlas web interface.

1.  **Navigate to Database Deployments**:
    *   Log in to your [MongoDB Atlas account](https://cloud.mongodb.com/).
    *   On the main screen, click the **"Browse Collections"** button for your cluster.

2.  **Create the Database and First Collection**:
    *   Click the **"Create Database"** button.
    *   Enter the following names:
        *   **Database Name**: `vector_db`
        *   **Collection Name**: `documents`
    *   Click **"Create"**.

3.  **Create the Second Collection**:
    *   Your `vector_db` database will now appear on the left. Hover over it and click the **`+`** sign to create another collection.
    *   **Collection Name**: `embeddings`
    *   Click **"Create"**.

Your database structure is now ready for the data.

---

## Part 2: Connect to Your Database with MongoDB Compass

Now, you will get your connection credentials and connect using the Compass GUI.

1.  **Get Your Connection String**:
    *   Return to your main cluster view by clicking **"Database"** in the top-left.
    *   Click the **"Connect"** button for your cluster.
    *   Select **"Compass"** as the connection method and copy the connection string.

2.  **Connect in Compass**:
    *   Open MongoDB Compass.
    *   Paste the connection string and **replace `<password>` with your actual database user password**.
    *   Click **"Connect"**.

---

## Part 3: Import Your Local Data

With Compass connected, you will import the two JSON files you generated in STEP 1.

1.  **Import Cleaned Data to `documents`**:
    *   In Compass, select the `vector_db` database on the left, then click on the `documents` collection.
    *   From the top menu, select **Collection > Import Data**.
    *   In the dialog, click **"Select a file"** and choose the `output_cleaned.json` file located in the `STEP 1/vscode_implementation` directory.
    *   Ensure the file type is set to **JSON** and click **"Import"**.

2.  **Import Embeddings to `embeddings`**:
    *   Now, select the `embeddings` collection on the left.
    *   Again, select **Collection > Import Data** from the top menu.
    *   Choose the `embeddings.json` file from the `STEP 1/vscode_implementation` directory.
    *   Ensure the file type is **JSON** and click **"Import"**.

Your data is now live in your cloud database.

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
          "type": "filter",
          "path": "metadata.county"
        }
      ]
    }
    ```

5.  **Index Name**: Give the index a name, such as `vector_index`.
6.  Click **"Create Index"**. The index will now build in the background.

---

## ✅ Full Setup Complete

Congratulations! Your MongoDB Atlas database is now fully configured, populated with your local data, and equipped with a powerful vector search index. It is ready to be used as the backend for your AI application.