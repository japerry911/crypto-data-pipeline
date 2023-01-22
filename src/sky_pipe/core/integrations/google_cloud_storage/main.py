from datetime import datetime
import tempfile
import uuid

import pandas as pd
from prefect import flow, get_run_logger, task
from prefect_gcp.cloud_storage import GcsBucket


@flow(name="Load-to-Parquet-and-Upload-to-GCS")
def load_to_parquet_and_upload_to_gcs(data: list[dict]):
    logger = get_run_logger()

    logger.info("---Starting Load to Parquet and Upload to GCS---")

    logger.info("Converting data to Pandas DataFrame")
    df = convert_data_to_pandas_dataframe(data=data)

    logger.info("Loading DF to Parquet and Uploading to GCS")
    load_df_to_parquet_and_upload_to_gcs(df=df)


@task(name="Load-DF-to-Parquet-and-Upload-to-GCS")
def load_df_to_parquet_and_upload_to_gcs(df: pd.DataFrame):
    gcs_bucket_block = GcsBucket.load("gcs-bucket-sky-pipe-load-data")

    DATE_UPLOADED = datetime.now().date().strftime("%Y-%m-%d")

    destination_gcs_path = (
        f"coin-market-cap/{DATE_UPLOADED}/{datetime.now().isoformat()}"
        f"-{uuid.uuid4()}"
    )
    local_temp_file = tempfile.NamedTemporaryFile(
        prefix=str(uuid.uuid4()),
        suffix=".parquet",
    )

    df.to_parquet(path=local_temp_file.name)

    # noinspection PyUnresolvedReferences
    gcs_bucket_block.upload_from_path(
        from_path=local_temp_file.name,
        to_path=destination_gcs_path,
    )


@task(name="Convert-Data-to-Pandas-DataFrame")
def convert_data_to_pandas_dataframe(data: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(data=data)
