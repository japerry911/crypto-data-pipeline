from datetime import datetime
import tempfile
import uuid

import pandas as pd
from prefect import flow, get_run_logger, task
from prefect_gcp.cloud_storage import GcsBucket


@flow(name="Load-to-Parquet-and-Upload-to-GCS")
def load_to_parquet_and_upload_to_gcs(data: list[dict]) -> str:
    logger = get_run_logger()

    logger.info("---Starting Load to Parquet and Upload to GCS---")

    logger.info("Converting data to Pandas DataFrame")
    df = convert_data_to_pandas_dataframe(data=data)

    logger.info("Loading DF to Parquet and Uploading to GCS")
    gcs_filename = load_df_to_parquet_and_upload_to_gcs(df=df)

    logger.info("---Finished Loading Data to Parquet File in GCS---")

    return gcs_filename


@task(name="Load-DF-to-Parquet-and-Upload-to-GCS")
def load_df_to_parquet_and_upload_to_gcs(df: pd.DataFrame):
    gcs_bucket_block = GcsBucket.load("gcs-bucket-sky-pipe-load-data")

    DATETIME_UPLOADED = datetime.now().strftime("%Y-%d-%m_%H:%M:%S")

    destination_gcs_path = (
        f"coin-market-cap/{DATETIME_UPLOADED}/{datetime.now().isoformat()}"
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

    return destination_gcs_path


@task(name="Convert-Data-to-Pandas-DataFrame")
def convert_data_to_pandas_dataframe(data: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(data=data)
