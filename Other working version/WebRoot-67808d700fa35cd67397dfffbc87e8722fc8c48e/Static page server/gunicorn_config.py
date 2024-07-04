import multiprocessing
import gevent


# Basic configuration
bind = "0.0.0.0:5000"  # Bind to all IPs on port 8000

threading =True

# Workers
workers = multiprocessing.cpu_count() * 2 + 1  # Number of worker processes
worker_class = "gevent"  # Asynchronous workers for handling many simultaneous clients
worker_connections = 1000  # Maximum number of simultaneous clients

# Timeouts
timeout = 30  # Workers silent for more than this many seconds are killed and restarted
graceful_timeout = 30  # Timeout for graceful workers restart
keepalive = 2  # The number of seconds to wait for requests on a Keep-Alive connection

# Logging
errorlog = "-"  # stderr
accesslog = "-"  # stdout
loglevel = "info"  # Logging level

# Performance tuning
# limit_request_line = 4094  # Limit the size of HTTP request line
# limit_request_fields = 100  # Limit the number of HTTP headers
# limit_request_field_size = 8190  # Limit the size of HTTP request header fields

# Security
preload_app = True  # Load application code before the worker processes are forked
# chdir = "/path/to/your/flask/app"  # Change to specified directory before loading app

# SSL Configuration
keyfile = "./certificates/key.pem"  # Path to the SSL key file
certfile = "./certificates/cert.pem"  # Path to the SSL certificate file


# Additional settings
# daemon = False  # Whether to daemonize the Gunicorn process
# pidfile = "./tmp/gunicorn.pid"  # Path to PID file
# umask = 0  # Umask to set before daemonizing
# user = None  # User to switch to after logging
# group = None  # Group to switch to after logging
