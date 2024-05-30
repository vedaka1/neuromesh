FROM dockerhub.timeweb.cloud/python:3.12.1-slim-bullseye

WORKDIR /app

ENV PYTHONPATH=.

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip
RUN pip install poetry==1.7.1

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY src/ .
COPY .env .

CMD [ "python", "main.py" ]