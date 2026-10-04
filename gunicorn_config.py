# Gunicorn Configuration
# Save as: gunicorn_config.py

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker Processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = os.path.join(os.path.dirname(__file__), 'logs', 'access.log')
errorlog = os.path.join(os.path.dirname(__file__), 'logs', 'error.log')
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'hoovale'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment in production)
# keyfile = "/path/to/keyfile.key"
# certfile = "/path/to/certfile.crt"

# Application
max_requests = 1000
max_requests_jitter = 50
