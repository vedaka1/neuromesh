from taskiq_aio_pika import AioPikaBroker

from infrastructure.config import settings

broker = AioPikaBroker(settings.BROKER_URL)
