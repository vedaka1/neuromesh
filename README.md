# Neuromesh
API + TG Bot to access to AI models

## Project features
* Subscription system
* Centralized logging with Loki and Grafana
* Clean Architecture
* RabbitMQ as a tasks queue
* Text generation
* Image generation

## How to run
* Set RabbitMQ environment variables `./.env`
    ```python
    RABBITMQ_USER=
    RABBITMQ_PASSWORD=
    RABBITMQ_HOST=
    RABBITMQ_PORT=
    ```
    Set API environment variables for development `./api/.env`
    ```python
    MODE=

    POSTGRES_HOST=localhost
    POSTGRES_PORT=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_DB=

    API_KEY_KADINSKY=
    API_SECRET_KEY_KADINSKY=

    AUTH_DATA_SBER=
    CLIENT_ID_SBER=
    CLIENT_SECRET_SBER=

    API_KEY_CHATGPT=

    BOT_TOKEN=
    BROKER_URL=
    ```
    Set API environment variables `./api/.env.production`
    ```python
    MODE=

    POSTGRES_HOST=postgres
    POSTGRES_PORT=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_DB=

    API_KEY_KADINSKY=
    API_SECRET_KEY_KADINSKY=

    AUTH_DATA_SBER=
    CLIENT_ID_SBER=
    CLIENT_SECRET_SBER=

    API_KEY_CHATGPT=

    BOT_TOKEN=
    BROKER_URL=
    ```
    Set Bot environment variables `./tgbot/.env`
    ```python
    BOT_TOKEN=
    ```
    ### Development
    * Run `make app` or `docker compose up -d` in the project directory
    ### Production
    * Run `make prod` or `docker compose -f docker-compose.production.yml up -d` in the project directory

## API Routes
* Users ![image](./docs/images/users.png)
* Subscriptions ![image](./docs/images/subscriptions.png)
* Neural Networks ![image](./docs/images/neural_networks.png)
## Centralized logs with Grafana Loki
![image](./docs/images/grafana.png)
