# Sky-Pipe

### Summary

Sky-Pipe is a Prefect Dataflow Pipeline that integrates `Google Cloud Platform` and `dbt`.
Specifically, the Sky-Pipe fetches daily exchange data from CoinMarketCap.com and
loads this data into Google Cloud Platform, and transforms it with dbt. This pipeline
also utilizes `GitHub Actions` for dev ops.

### Technologies Used

- Google Cloud Platform
    - Google Cloud Run Jobs
    - Google Cloud Storage
    - Google Cloud Secrets Manager
    - Google Cloud BigQuery
    - Google Cloud Artifact Registry
- Python 3.10
- Prefect
    - Flow
    - Task
    - Logging
- Prefect-GCP
    - Cloud Run Job
    - GCP Secrets
    - Google Cloud Storage 
    - GCP Credentials
    - GCP BigQuery
<br/>
<br/>

### Prefect Flow Steps

1. Fetch data from CoinMarketCap.com
2. Write data to Pandas DataFrame
3. Load DataFrame to Parquet file
4. Upload Parquet file to Google Cloud Storage bucket
5. Load Parquet file from Google Cloud Storage to BigQuery via Load Job
6. Trigger dbt job to run transformations within BigQuery
<br/>
<br/>

### GitHub Actions

- Workflows
  - Deploy Agent
    - deploys Prefect Agent Docker Image and deploys Prefect Agent to 
    Google Compute Engine
  - Deploy Flows and Blocks
    - deploys Prefect Flows Docker Image and the actual Prefect Flow Deployment
    for CoinMarketCap.com.
- Actions
  - Container-Image
    - deploys Docker Image to Artifact Registry
  - Deploy Container to Compute Engine
    - deploys Docker Image from Artifact Registry to Compute Engine
  - Deploy-Flows
    - deploys Prefect Deployments to Prefect Cloud
