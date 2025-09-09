# STEP 3.2: Full Setup & Vector Index Configuration

This guide follows the prerequisite setup. Here, you will connect to your newly created MongoDB Atlas cluster, create the necessary database structure, and configure the vector search index. This index is the core component that enables fast semantic search on your embeddings.

---

## Part 1: Download and Install MongoDB Compass

If you haven't already, you need to install MongoDB Compass. It is the official graphical user interface (GUI) for MongoDB and allows you to easily manage your database.

1.  **Go to the Download Page**:
    *   Visit the [MongoDB Compass Download Page](https://www.mongodb.com/try/download/compass).

2.  **Download and Install**:
    *   The website should auto-select the correct version for your operating system.
    *   Download the installer and follow the on-screen instructions to install it on your system.

---

## Part 2: Connect to Your Atlas Cluster with Compass

Now you will use Compass to connect to the cloud database you created.

1.  **Get Your Connection String**:
    *   Navigate to your [MongoDB Atlas dashboard](https://cloud.mongodb.com/).
    *   Find your cluster and click the **"Connect"** button.
    *   In the connection methods pop-up, select **"Compass"**.
    *   A connection string will be displayed. Click the **"Copy"** button to copy it to your clipboard. It will look something like this:
        ```
        mongodb+srv://your_username:<password>@your_cluster.mongodb.net/
        ```

2.  **Connect in Compass**:
    *   Open MongoDB Compass.
    *   The connection string from your clipboard may automatically appear in the connection field. If not, paste it in.
    *   **Crucially, replace `<password>` in the string with the actual password** you created for your database user in the prerequisite step.
    *   Click **"Connect"**. You should now be connected to your Atlas cluster.

---

## Part 3: Create Your Database and Collection

Your chatbot needs a dedicated place to store its data. You will now create a database and a "collection" (which is similar to a table in a SQL database).

1.  In Compass, navigate to the **"Databases"** tab in the main view.
2.  Click the **"Create Database"** button.
3.  Enter the following names:
    *   **Database Name**: `chatbot_poc`
    *   **Collection Name**: `documents`
4.  Click **"Create Database"**. You will now see `chatbot_poc` in your list of databases.

---

## Part 4: Create the Vector Search Index

This is the most important step. You will create a special index that allows MongoDB to perform efficient similarity searches on your text embeddings.

1.  Click on the `chatbot_poc` database, then select the `documents` collection.
2.  Navigate to the **"Indexes"** tab for the collection.
3.  Click the **"Create Index"** button.
4.  In the creation dialog, select the **"JSON Editor"** tab.
5.  Delete the default content and paste the following JSON configuration exactly as it is:

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

6.  **Index Name**: Give the index a name, for example, `vector_index`.
7.  Click **"Create Index"**.

### Understanding the Index Configuration:
*   `"path": "vector"`: Tells Atlas to index the `vector` field from our `embeddings.json` data.
*   `"numDimensions": 768`: Specifies that our vectors have 768 dimensions, which is the standard for the `text-embedding-004` model we used.
*   `"similarity": "cosine"`: Defines the algorithm to use for comparing vectors. Cosine similarity is a standard choice for text embeddings.
*   `"type": "filter"`: We are also making the fields inside our `metadata` object searchable, so you can filter your vector search queries (e.g., find similar documents but only from a specific `year`).

---

## ✅ Full Setup Complete

Your MongoDB Atlas database is now fully configured and ready. The `chatbot_poc.documents` collection is prepared to have the `embeddings.json` data imported, and the vector index is in place to power your AI application.
