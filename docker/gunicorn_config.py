import os

bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
workers = int(os.environ.get("GUNICORN_WORKERS", 4))
worker_class = "sync"
timeout = 120
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info")

# 优雅重启
graceful_timeout = 30
max_requests = 1000
max_requests_jitter = 100
