# Cloud Function for Data Quality Check Triggered by Cloud Scheduler and Pub/Sub
This Cloud Function is designed to perform data quality checks triggered by messages on a Cloud Pub/Sub topic. It utilizes Google Cloud Scheduler to publish messages to the Pub/Sub topic at specified intervals.

# Overview
The Cloud Function data_quality_check is triggered by messages on a specified Cloud Pub/Sub topic. When a message is received, the function decodes the message payload, retrieves SQL queries stored in a Google Cloud Storage bucket, performs data quality checks using these queries, and inserts the results into a monitoring table in BigQuery.

# Dependencies
- google-cloud-pubsub: Python client library for Pub/Sub.
- google-cloud-storage: Python client library for Cloud Storage.
- google-cloud-bigquery: Python client library for BigQuery.
- variables.py: Python module containing project variables.
- functions.py: Python module containing helper functions.

# Configuration
Before deploying the Cloud Function, ensure the following configurations:

Cloud Scheduler: Configure Cloud Scheduler to publish messages to the Cloud Pub/Sub topic at the desired intervals.
Cloud Pub/Sub: Create a Pub/Sub topic and subscription for triggering the Cloud Function.
Variables: Update the variables.py file with project-specific variables such as project_id, table_monitoring, destination_dataset, and destination_table.
Functions: Implement the functions in functions.py for listing SQL queries from the Cloud Storage bucket, creating a monitoring table if it doesn't exist, and inserting data into the monitoring table.
Deployment
Deploy the Cloud Function using the Google Cloud Console, Cloud SDK, or Cloud Deployment Manager. Associate the Cloud Function with the Pub/Sub topic for triggering.

# Usage
After deployment, Cloud Scheduler will publish messages to the Pub/Sub topic at specified intervals, triggering the Cloud Function. The function will then perform data quality checks using SQL queries stored in the Cloud Storage bucket and insert the results into the monitoring table in BigQuery.

##  Setting cloud scheduler
- ![Setting cloud scheduler](https://github.com/cyao59/technology-watch/blob/main/cloud_function/monitoring_pubsub_gcs_to_bq/setting_cloud_scheduler.png)

## Setting cloud function with cloud scheduler and pub sub
- ![Setting cloud function with cloud scheduler and pub sub](https://github.com/cyao59/technology-watch/blob/main/cloud_function/gcs_to_bQ/setting_cloud_function.png)


# Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

Feel free to customize this README further based on your specific requirements or add additional sections as needed.