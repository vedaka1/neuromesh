# !/bin/bash

alembic upgrade head
uvicorn presentation.main:create_app --host 0.0.0.0 --port 8000 --reload
