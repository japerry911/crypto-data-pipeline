from prefect import flow, get_run_logger
from google.cloud.bigquery import CreateDisposition, WriteDisposition, SourceFormat
from prefect_gcp.credentials import GcpCredentials
from prefect_gcp.bigquery import bigquery_load_cloud_storage


@flow(name="Load-Files-from-GCS-to-BigQuery")
def load_files_from_gcs_to_bigquery(gcs_filenames: list[str]):
    logger = get_run_logger()

    logger.info("---Starting to Load Files from GCS to BigQuery---")

    GCS_PREFIX = "gs://sky-pipe-load-data"
    gcp_credentials = GcpCredentials.load("gcp-credentials")

    logger.info(f"Loading {len(gcs_filenames)} GCS files to BQ Warehouse")
    for gcs_filename in gcs_filenames:
        logger.info(f"Loading {gcs_filename} to BQ Warehouse")
        bigquery_load_cloud_storage(
            dataset="landing",
            table="coin_market_cap",
            uri=f"{GCS_PREFIX}/{gcs_filename}",
            gcp_credentials=gcp_credentials,
            location="us-central1",
            job_config={
                "autodetect": True,
                "source_format": SourceFormat.PARQUET,
                "create_disposition": CreateDisposition.CREATE_IF_NEEDED,
                "write_disposition": WriteDisposition.WRITE_APPEND,
            },
        )

    logger.info("---Finished Loading Files from GCS to BigQuery---")
