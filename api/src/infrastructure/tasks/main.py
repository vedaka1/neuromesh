from infrastructure.config import config
from taskiq_aio_pika import AioPikaBroker

broker = AioPikaBroker(config.BROKER_URL_ENV)
