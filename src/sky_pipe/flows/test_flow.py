from prefect import flow


@flow(name="Test_Flow", log_prints=True)
def test_flow():
    print("Hello from Prefect, woohoo!")


if __name__ == "__main__":
    test_flow()
