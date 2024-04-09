# Setting cloud function with cloud storage
![Setting Cloud Function](https://github.com/cyao59/technology-watch/blob/main/cloud_function/gcs_to_bQ/setting_cloud_function.png)

# Cloud Function for Loading CSV Files from Google Cloud Storage to BigQuery
This Cloud Function is designed to automate the process of loading CSV files from Google Cloud Storage (GCS) into BigQuery. It utilizes the Google Cloud Python client libraries for BigQuery and Cloud Storage.

# Overview
The Cloud Function gcs_to_bq is triggered by events in a specified GCS bucket. When a CSV file is uploaded to the bucket, the function reads the file using Pandas, determines the schema based on the data types of the columns, creates or updates a corresponding table in BigQuery, and then loads the data from the CSV file into the BigQuery table.

# Dependencies
google-cloud-bigquery: Python client library for BigQuery.
google-cloud-storage: Python client library for Cloud Storage.
pandas: Python library for data manipulation and analysis.
# Configuration
Before deploying the Cloud Function, ensure the following configurations:

Google Cloud Project: Replace the project_id variable with your Google Cloud project ID.
BigQuery Dataset: Set the dataset_name variable to the name of your BigQuery dataset.
Job Configuration: Adjust the job_config variable according to your requirements for loading data into BigQuery.
Trigger: Configure Cloud Storage to trigger the Cloud Function whenever a CSV file is uploaded to a specific bucket.
# Deployment
Deploy the Cloud Function using the Google Cloud Console, Cloud SDK, or Cloud Deployment Manager. Ensure that the necessary IAM permissions are granted to the service account associated with the Cloud Function for accessing BigQuery and Cloud Storage.

# Usage
After deployment, any CSV files uploaded to the specified Cloud Storage bucket will trigger the Cloud Function, which will then load the data into the corresponding BigQuery table.

# Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

Feel free to customize this README further based on your specific requirements or add additional sections as needed.
