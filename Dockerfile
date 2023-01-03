FROM prefecthq/prefect:2-python3.10

COPY requirements.txt .

RUN pip install --upgrade pip setuptools --no-cache-dir
RUN pip install --trusted-host pypi.python.org --no-cache-dir .

ARG PREFECT_API_KEY
ENV PREFECT_API_KEY=$PREFECT_API_KEY

ARG PREFECT_API_URL
ENV PREFECT_API_URL=$PREFECT_API_URL

ENV PYTHONUNBUFFERED True

ENTRYPOINT ["prefect", "agent", "start", "-q", "default"]