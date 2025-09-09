# STEP 3.2: Full Setup - Database, Data Import, and Vector Index

This guide details the full setup process for MongoDB Atlas. You will create your database structure, connect to it, import the data generated in STEP 1, enrich the data using an aggregation pipeline, and finally create the essential vector search index.

---

## Part 1: Create Database and Collections in Atlas

First, create the database and collections directly within the MongoDB Atlas web interface.

1.  **Navigate to Database Deployments**: Log in to your [MongoDB Atlas account](https://cloud.mongodb.com/) and click the **"Browse Collections"** button for your cluster.
2.  **Create Database and Collections**: Click **"Create Database"** and create a database named `vector_db` with two collections inside it: `documents` and `embeddings`.

---

## Part 2: Connect and Import Data with Compass

Next, connect to your database using the Compass GUI and import the JSON files from STEP 1.

1.  **Download Compass**: Get the official GUI from the [MongoDB Compass Download Page](https://www.mongodb.com/try/download/compass).
2.  **Get Connection String**: In Atlas, click **"Connect"** on your cluster, select **"Compass"**, and copy the connection string.
3.  **Connect in Compass**: Open Compass, paste the string, **replace `<password>` with your database user's password**, and connect.
4.  **Import `output_cleaned.json`**: Select the `vector_db.documents` collection, go to **Collection > Import Data**, and import the `output_cleaned.json` file from the `STEP 1/vscode_implementation` directory.
5.  **Import `embeddings.json`**: Select the `vector_db.embeddings` collection, go to **Collection > Import Data**, and import the `embeddings.json` file from the `STEP 1/vscode_implementation` directory.

---

## Part 3: Enrich Data with an Aggregation Pipeline

This pipeline enriches the minimal metadata in the `embeddings` collection with the full, detailed information from the `documents` collection.

1.  In Compass, navigate to the `vector_db` database and select the **`embeddings`** collection.
2.  Click the **"Aggregations"** tab.
3.  Build the following pipeline stage by stage:

    **Stage 1: `$lookup`**
    *   *What it does*: Finds the matching record from the `documents` collection based on the operator name.
    ```javascript
    {
      from: "documents",
      localField: "metadata.operator",
      foreignField: "Operator",
      as: "doc_info"
    }
    ```

    **Stage 2: `$set`**
    *   *What it does*: Takes the first matched document from the `doc_info` array and places it in a new `doc` field for easy access.
    ```javascript
    {
      doc: {
        $arrayElemAt: ["$doc_info", 0]
      }
    }
    ```

    **Stage 3: `$set`**
    *   *What it does*: Replaces the old, minimal `metadata` object with a new, fully enriched one using fields from the looked-up document.
    ```javascript
    {
      doc_id: "$doc._id",
      metadata: {
        year: "$doc.Production Year",
        production_date_entered: "$doc.Production Date Entered",
        operator: "$doc.Operator",
        county: "$doc.County",
        town: "$doc.Town",
        field: "$doc.Field",
        producing_formation: "$doc.Producing Formation",
        active_oil_wells: "$doc.Active Oil Wells",
        inactive_oil_wells: "$doc.Inactive Oil Wells",
        active_gas_wells: "$doc.Active Gas Wells",
        inactive_gas_wells: "$doc.Inactive Gas Wells",
        injection_wells: "$doc.Injection Wells",
        disposal_wells: "$doc.Disposal Wells",
        self_use_well: "$doc.Self-use Well",
        oil_produced_bbl: "$doc['Oil Produced, bbl']",
        gas_produced_mcf: "$doc['Gas Produced, Mcf']",
        water_produced_bbl: "$doc['Water produced, bbl']",
        taxable_gas_mcf: "$doc['Taxable Gas, Mcf']",
        purchaser_codes: "$doc['Purchaser Codes']",
        location: "$doc.Location"
      }
    }
    ```

    **Stage 4: `$unset`**
    *   *What it does*: Cleans up by removing the temporary fields used during the pipeline.
    ```javascript
    ["doc_info", "doc"]
    ```

    **Stage 5: `$merge`**
    *   *What it does*: This is the final, critical action. It takes the results of the pipeline and merges them back into the `embeddings` collection, updating each document in place.
    ```javascript
    {
      into: "embeddings",
      on: "_id",
      whenMatched: "merge",
      whenNotMatched: "fail"
    }
    ```

4.  After building the pipeline, you can preview the results. Once you confirm they are correct, the pipeline will run and update all documents in the `embeddings` collection.

---

## Part 4: Create the Vector Search Index

Now that your data is enriched, you can create the index to enable semantic search.

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

5.  **Index Name**: Give the index a name, such as `vector_index`, and click **"Create Index"**.

---

## ✅ Full Setup Complete

Congratulations! Your MongoDB Atlas database is now fully configured, populated with enriched data, and equipped with a powerful vector search index. It is ready to be used as the backend for your AI application.