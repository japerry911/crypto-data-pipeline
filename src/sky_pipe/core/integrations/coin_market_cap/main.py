from datetime import datetime
from time import sleep

import requests
from prefect import flow, get_run_logger, task
from prefect_gcp.secret_manager import GcpSecret


@flow(name="Fetch-Coin-Market-Cap-Data")
def fetch_coin_market_cap_data():
    logger = get_run_logger()

    logger.info("---Starting Data Fetch from CoinMarketCap---")

    logger.info("Fetching API Key for CoinMarketCap")
    api_key = fetch_coin_market_cap_api_key()

    logger.info("Fetch all Crypto IDs, Names, and USD Prices")
    raw_data = fetch_all_crypto_price_data(api_key=api_key)

    logger.info(f"---Fetched a total of {len(raw_data)} rows of data---")

    return raw_data


@task(name="Fetch-All-Crypto-Price-Data")
def fetch_all_crypto_price_data(api_key: str) -> list[dict[str, str]]:
    logger = get_run_logger()

    # ToDo: make dynamic for dev/prod environment executions
    API_BASE_URL = "https://sandbox-api.coinmarketcap.com"
    API_VERSION = "v1"
    LIMIT = 5_000
    DATETIME_FETCHED = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    use_url = f"{API_BASE_URL}/{API_VERSION}/cryptocurrency/listings/latest"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }
    base_params = {
        "start": 1,
        "limit": LIMIT,
    }

    page_number = 1
    returned_length = None
    return_data_list = []

    while returned_length is None or returned_length == LIMIT:
        logger.info(f"Request Page {page_number}")
        response = requests.get(use_url, headers=headers, params=base_params)
        logger.info("Request Successful")

        response_json = response.json()
        data_list = response_json["data"]

        returned_length = len(data_list)

        return_data_list.extend(
            parse_cryptocurrency_listings_response(
                data_list=data_list,
                datetime_fetched=DATETIME_FETCHED,
            )
        )

        # Reduce chances of Rate Limit / max 30 requests per minute
        sleep(2)

    return return_data_list


@task(name="Fetch-Coin-Market-Cap-API-Key")
def fetch_coin_market_cap_api_key() -> str:
    # noinspection PyUnresolvedReferences
    # ToDo: make dynamic for dev/prod environment executions
    return GcpSecret.load("sandbox-coinmarketcap-api-key").read_secret()


def parse_cryptocurrency_listings_response(
    data_list: list[dict],
    datetime_fetched: str,
) -> list[dict]:
    return_list = []

    for row in data_list:
        return_list.append(
            {
                "id": str(row["id"]),
                "name": row["name"],
                "cmc_rank": str(row["cmc_rank"]),
                "usd_price": str(row["quote"]["USD"]["price"]),
                "datetime_fetched": datetime_fetched,
            }
        )

    return return_list
