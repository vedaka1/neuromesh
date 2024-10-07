import os

# WSGI application
wsgi_app = "presentation.main:create_app()"

# Worker class
worker_class = "uvicorn.workers.UvicornWorker"

# Binding
host = os.getenv("SERVER_HOST", "0.0.0.0")
port = os.getenv("SERVER_PORT", "8000")
bind = f"{host}:{port}"

# Number of workers
workers = 2

# Daemon
daemon = False
