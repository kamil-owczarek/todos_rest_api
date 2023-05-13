# Todos REST API

## Table of Contents

- [Overview](#overview)
- [Folder structure](#folder-structure)
- [Python dependencies](#python-dependencies)
- [Base model](#base-model)
- [Endpoints](#endpoints)
- [How to execute unit tests](#how-to-execute-unit-tests)
- [Prepare database and table](#prepare-database-and-table)
- [Prepare API configuration](#prepare-api-configuration)
  - [Local environmental variables](#local-environmental-variables)
  - [Azure Key Vault secrets](#azure-key-vault-secrets)
- [How to run API](#how-to-run-api)
  - [Local console](#local-console)
  - [With Docker usage](#with-docker-usage)
- [How to call endpoints](#how-to-call-endpoints)


## Overview
The repository is built out of API implementation to manage todos items. The API used the REST API architecture pattern. The source code is written in Python with the FastAPI framework usage.

## Folder structure
```bash
api_                        # Source folder 
|   |_ src                  # Contains source cod
|   |   |_ adapters         # Contains connections with the outside systems
|   |   |_ auth             # Authentication logic, like JWT token generation
|   |   |_ azure            # Logic to connect with Azure services
|   |   |_ config           # Configuration base class
|   |   |_ domain           # Data models
|   |   |_ entrypoints      # FastAPI implementation, routes
|   |   |_ service_layer    # Logic to handle by API
|   |   |_ utils            # Utilities
|   |_ tests                # Contains tests
|       |_ unit             # Unit tests of core API behaviours
|       |_ conftest.py      # Tests configuration file
|  
sql                         # SQL scripts
```

## Python dependencies
To manage Python dependencies, the [Poetry](https://python-poetry.org/) tool has been used.
To install dependencies locally type:
```
cd api/
poetry install
```
Poetry installs dependencies under a virtual environment that is created by default. In some cases, there is a need to activate the virtual environment manually. To do that, type:
```
#bash 
source <path_to_venv>/Scripts/activate

#PS
<path_to_venv>\Scripts\activate.ps1
```

## Base model
API handle data from a relational database with the below structure:
> Data types can differ between database

| Column name | Type | Remark |
| - | - | - |
| ID | INTEGER | PRIMARY KEY |
| TITLE | VARCAHR | - |
| DESCRIPTION | VARCHAR | - |
| COMPLETED | BOOLEAN | - |

## Endpoints
API exposes seven endpoints. The below list shortly describe them. For more information reach the documentation endpoint.

| Endpoint | HTTP method | Description |
| - | - | - |
| /docs | GET | OpenAPI documentation |
| /token | GET | JWT token generation |
| /items/{item_id} | GET | Retrieve single Item |
| /items | GET | Retrieve list of Items |
| /items | POST | Upload Item |
| /items/{item_id} | PATCH | Update Item |
| /items/{item_id} | DELETE | Delete Item |

## How to execute unit tests
Unit tests had been implemented with [pytest](https://docs.pytest.org/en/7.3.x/) library. The Poetry tool can handle the unit test configuration. Due to that follow [Python dependencies](#python-dependencies) part to install all dependencies. 
After dependencies installation and virtual environment activation, type the below commands to execute unit tests:
> Poetry will handle pytest configuration, so any additional commands are not required.

```
cd api/
pytest
```
After unit tests execution, you will the result in the console. Also, the XML with the result will be generated.
![unit-test-result](/docs/unit_test_result.png)

## Prepare database and table
To use API there is a need to prepare a relational database. For now, only communication with the PostgreSQL database is allowed. You can use any instance of the PostgreSQL database. The most important is to prepare the table with proper schema. For table preparation, there is [a script]((/sql/prepare_data.sql)) under the [sql folder](/sql/). The script creates the table if not exist and fills up the table with example data.

## Prepare API configuration
There are two options to read API configuration:
- local environmental variables
- Azure Key Vault

Both options require specific steps.

### Local environmental variables
To run API with local environmental variables there is a need to fill up and create the below environmental variables:
```
export credential_type=local    # Determines whether it is a local or a cloud credential type 
export db_user=
export db_password=
export db_host=
export db_port=
export db_name=
export db_table_name=           # If not provided, default value is "items"
export jwt_secret=
export jwt_algorithm=           # If not provided, default value is "HS256"
export jwt_token_expiration=    # If not provided, default value is "600"
```

### Azure Key Vault secrets
> Prerequisites: Create Azure cloud account and [Azure Key Vault service](https://learn.microsoft.com/en-us/azure/key-vault/general/quick-create-portal).

To run API with Azure Key Vault secrets usage, firstly you need to prepare the below secrets:
> Please keep the naming convention, because secrets are loading into the Settings model.

```
jwt-secret
db-user
db-password
db-host
db-port
db-name
```

Then, prepare environment variables:
```
export credential_type=cloud
export key_vault_url=
export azure_secrets='["jwt-secret", "db-user", "db-password", "db-host", "db-port", "db-name"]'
```

To access the Azure cloud from the local environment, the Azure credentials are required:
```
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_CLIENT_SECRET
```
You can easily create them by installing [Azure CLI](#https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) and logging into Azure cloud via `az login` command.


## How to run API
### Local console
To run API locally follow the below steps:
1. Install [dependencies](#python-dependencies).
2. Prepare table from [previous part](#prepare-database-and-table). Be sure that your database is running.
3. Decide from where API will read [the configuration](#prepare-api-configuration).
4. If all previous steps are done, prompt the below commands:
```
cd api/
uvicorn src.entrypoints.fastapi_app:app --port 8081
```
5. Go to [next section](#how-to-call-endpoints), to check how to communicate with API.

### With Docker usage
> Prerequisites: Install [Docker engine](#https://docs.docker.com/engine/install/) and [Docker compose plugin](#https://docs.docker.com/compose/install/).

To run API with Docker follow the below steps:
1. PostgreSQL database and table preparation is included in [docker-compose.yml](/docker-compose.yml) file. If you want to use your own database, please remove the part with PostgreSQL creation from [docker-compose.yml](/docker-compose.yml) file. In case of your own database usage, follow [database and table preparation](#prepare-database-and-table) section.
2. Decide from where API will read [the configuration](#prepare-api-configuration). The mentioned environment variables should be part of [docker-compose.yml](/docker-compose.yml) file. Under ``environment`` properties there are variables for both configurations. You can remove unnecessary variables after configuration option choose. Example ``docker-composey.yml`` configuration:
```
# docker-compose.yml

version: '3.8'

services:
  api:
    build: ./api
    command: uvicorn src.entrypoints.fastapi_app:app --host 0.0.0.0 --port 8081
    ports:
      - 8081:8081
    environment:
      - db_host=db
      - credential_type=cloud
      - key_vault_url=https://<kv_name>.vault.azure.net/
      - azure_secrets=["jwt-secret", "db-user", "db-password", "db-port", "db-name"]
      - AZURE_CLIENT_ID=<azure_client_id>
      - AZURE_TENANT_ID=<azure_tenant_id>
      - AZURE_CLIENT_SECRET=<azure_client_secret>
      - db_table_name=items
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
      - ./sql/prepare_data.sql:/docker-entrypoint-initdb.d/prepare_data.sql
    expose:
      - 127.0.0.1:5432
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=test1234
      - POSTGRES_DB=postgres

volumes:
  postgres_data:
```

3. If all previous steps are done, prompt the below commands to build and deploy Docker containers:
```
docker-compose up -d --build
```
4. Verify that containers are in a running state:
```
docker ps --filter "status=running"
```
![docker-containers](/docs/docker_running_containers.png)
5. Go to [next section](#how-to-call-endpoints), to check how to communicate with API.

## How to call endpoints
To communicate with API, the JWT token-based authentication is implemented. The logic ensures that each request to a server is accompanied by a signed token which the server verifies for authenticity.

Using OpenAPI documentation you are able to test the API. Follow the below steps:
1. Call documentation endpoint in a browser: ```https://127.0.0.1:8081/docs```.
2. Execute token endpoint to generate JWT token.
![token-generation](/docs/token_generation.png)
3. Add a token to authorize requests. The token will be automatically added to the header for every next call. By default, token expires after 60 minutes and there is a need to generate a new token.
![auth](/docs/auth.png)
4. Call endpoints to communicate with the server.
![singe-get](/docs/single_get.png)

To communicate with API using other tools, like Postman, curl, etc. the steps are similar:
1. Call token endpoint ```https://127.0.0.1:8081/token``` to generate JWT token.
2. Add token to authorization header:
```
'Authorization: Bearer <token>'
```
3. Execute API call, e.g.:
```
curl -X 'GET' \
  'http://127.0.0.1:8081/items/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <token>'
```
