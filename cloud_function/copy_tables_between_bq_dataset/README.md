# Cloud Function for Copying Tables Between BigQuery Datasets
This Cloud Function is designed to copy tables between BigQuery datasets triggered by messages on a Cloud Pub/Sub topic.

# Overview
The Cloud Function copy_tables_from_dataset is triggered by messages on a specified Cloud Pub/Sub topic. When a message is received, the function copies all tables from a source dataset to a destination dataset within the same project.

# Dependencies
google-cloud-bigquery: Python client library for BigQuery.
base64: Python library for base64 encoding and decoding.

# Configuration
Before deploying the Cloud Function, ensure the following configurations:

Cloud Pub/Sub: Create a Pub/Sub topic and subscription for triggering the Cloud Function.
Source Dataset: Specify the source dataset name and project ID in the source_project and source_dataset variables.
Destination Dataset: Specify the destination dataset name and project ID in the destination_project and destination_dataset variables.

# Deployment
Deploy the Cloud Function using the Google Cloud Console, Cloud SDK, or Cloud Deployment Manager. Associate the Cloud Function with the Pub/Sub topic for triggering.

# Usage
After deployment, Cloud Pub/Sub messages published to the specified topic will trigger the Cloud Function. The function will then copy all tables from the source dataset to the destination dataset in BigQuery.
##  Setting cloud scheduler
- ![Setting cloud scheduler](https://github.com/cyao59/technology-watch/blob/main/cloud_function/copy_tables_between_bq_dataset/setting_cloud_scheduler.png)
##  Setting Cloud Function for Copying Tables Between BigQuery Datasets
- ![Setting cloud function](https://github.com/cyao59/technology-watch/blob/main/cloud_function/copy_tables_between_bq_dataset/setting_cloud_function.png)

# Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

Feel free to customize this README further based on your specific requirements or add additional sections as needed.