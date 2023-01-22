from time import perf_counter

from prefect import flow, get_run_logger

from sky_pipe.core.integrations.coin_market_cap.main import fetch_coin_market_cap_data


@flow(name="CoinMarketCap Main Flow")
def main():
    logger = get_run_logger()

    logger.info("---Starting CoinMarketCap Main Flow---")
    start_time = perf_counter()

    logger.info("Running Coin Market Cap Fetch Data")
    fetch_coin_market_cap_data()

    end_time = perf_counter()
    total_time = end_time - start_time

    logger.info(f"---Completed CoinMarketCap Main Flow in {total_time:.4f} seconds")


if __name__ == "__main__":
    main()
