FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --with test --without-hashes

FROM python:3.10 as deploy-to-container

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN	apt-get update && apt-get -y install curl

RUN	curl -sL https://aka.ms/InstallAzureCLIDeb | bash

COPY ./src /app/src