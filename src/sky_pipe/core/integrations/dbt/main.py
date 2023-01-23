import json

from prefect import flow, get_run_logger, task
from prefect_dbt.cloud import DbtCloudCredentials
from prefect_dbt.cloud.jobs import \
    trigger_dbt_cloud_job_run_and_wait_for_completion
from prefect_gcp.secret_manager import GcpSecret


@flow(name="Run-dbt-Job")
def run_dbt_job(job_id: str):
    logger = get_run_logger()

    logger.info("---Starting dbt job execution and tests---")

    logger.info("Fetching dbt secrets from GCP and initializing credentials")
    api_key, account_id = fetch_dbt_gcp_secret_values()
    dbt_credentials = DbtCloudCredentials(
        api_key=api_key,
        account_id=account_id,
    )

    logger.info("Triggering dbt job and waiting for it to complete")
    trigger_dbt_cloud_job_run_and_wait_for_completion(
        dbt_cloud_credentials=dbt_credentials,
        job_id=job_id,
    )

    logger.info("---Finished running dbt job execution and tests---")


@task(name="Fetch-dbt-GCP-Secret-Values")
def fetch_dbt_gcp_secret_values() -> (str, str):
    # noinspection PyUnresolvedReferences
    # ToDo: make dynamic for dev/prod environment executions
    dbt_secrets_json = json.loads(GcpSecret.load("dbt-secrets").read_secret())

    return dbt_secrets_json["api_key"], dbt_secrets_json["account_id"]
