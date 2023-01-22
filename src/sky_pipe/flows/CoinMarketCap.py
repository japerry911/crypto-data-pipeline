from time import perf_counter

from prefect import flow, get_run_logger

from sky_pipe.core.integrations.coin_market_cap.main import fetch_coin_market_cap_data
from sky_pipe.core.integrations.google_cloud_storage.main import (
    load_to_parquet_and_upload_to_gcs,
)
from sky_pipe.core.integrations.google_bigquery.main import (
    load_files_from_gcs_to_bigquery,
)


@flow(name="CoinMarketCap Main Flow")
def main():
    logger = get_run_logger()

    logger.info("---Starting CoinMarketCap Main Flow---")
    start_time = perf_counter()

    logger.info("Running Coin Market Cap Fetch Data")
    raw_data = fetch_coin_market_cap_data()

    logger.info("Loading data into Parquet and then uploading to Google Cloud Storage")
    gcs_filename = load_to_parquet_and_upload_to_gcs(data=raw_data)

    logger.info("Loading file(s) from GCS to BQ Warehouse")
    load_files_from_gcs_to_bigquery(gcs_filenames=[gcs_filename])

    end_time = perf_counter()
    total_time = end_time - start_time

    logger.info(f"---Completed CoinMarketCap Main Flow in {total_time:.4f} seconds")


if __name__ == "__main__":
    main()
