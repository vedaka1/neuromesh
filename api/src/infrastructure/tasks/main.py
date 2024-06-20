from infrastructure.config import settings
from taskiq_aio_pika import AioPikaBroker

broker = AioPikaBroker(settings.BROKER_URL)
