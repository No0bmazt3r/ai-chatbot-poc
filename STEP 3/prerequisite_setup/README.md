# MongoDB Atlas Setup Guide for Malaysian Users

This guide provides detailed steps for setting up a free MongoDB Atlas cluster, optimized for users in Malaysia.

---

## Step 1: Create Your Atlas Account

First, you need to create your Atlas account by navigating to the [MongoDB Atlas Cloud registration page](https://www.mongodb.com/cloud/atlas/register) and signing up.

## Step 2: Deploy Your Cluster

![Data Preparation Workflow](../1.png)

After logging in, you will be prompted to deploy your first database.

### Choose Your Cluster Type
1.  You will see several options like **M10**, **Serverless**, and **M0 Free**.
2.  Select the **M0 Free** option. It is perfect for learning and development.
    *   No credit card required.
    *   Includes 512 MB storage, shared RAM, and shared vCPU.

### Configuration Settings

#### Basic Configuration
1.  **Name**: You can leave the default name `Cluster0` or enter a preferred cluster name. 
    *   **Important**: The cluster name cannot be changed once it is created.

#### Provider and Region Selection
2.  **Cloud Provider**: Select **AWS**. It should be pre-selected.
3.  **Region**: Choose **Singapore (ap-southeast-1)**. 
    *   This is the closest and recommended server location for users in Malaysia, providing the best performance.

#### Additional Settings
4.  **Preload sample dataset**: You can check this box if you want sample data to explore (this is optional).

### Advanced Configuration (Optional)
5.  For this guide, the basic configuration is sufficient. If you need more customization in the future, you can select "Go to Advanced Configuration".

## Step 3: Create Your Cluster

6.  Click the green **"Create Deployment"** button to begin provisioning your cluster. This will take a few minutes.

## Step 4: Final Setup (Security)

While the cluster is being created, you will be prompted to configure security settings.

### Create Database User
1.  **Username**: Enter a memorable username.
2.  **Password**: Create a strong password. You can use the "autogenerate" feature.
3.  **Important**: Securely save these credentials. You will need them to connect to your database.
4.  Click **"Create User"**.

### Configure Network Access
5.  Scroll down to the IP Access List section.
6.  Click **"Add My Current IP Address"** for better security if you will always be working from the same network. For more flexible access for this POC, add `0.0.0.0/0`.
    *   **IP Address**: `0.0.0.0/0`
    *   **Description**: `Allow access from anywhere`
    *   This setting allows global access, which is convenient for development but should be used with caution in production environments.

### Complete Setup
7.  Click **"Finish and Close"**.

---

Your MongoDB Atlas cluster is now being created and will be ready for use shortly!
