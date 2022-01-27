# Copyright (c) 2022 Interview Kickstart, LLC
# Simple python server for troubleshooting exercise
# Instructions in README.md

from queue import Queue
import json
import logging
import re
import signal
import socket
import time
import datetime

logging.basicConfig(level=logging.INFO, filename="server.log", filemode="w")

CONF_FILE = "serverconf.json"
config = {}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
configfile = open(CONF_FILE)


def load_config():
    global config
    global configfile
    configfile.seek(0)
    logging.info(f"Loading configuration from {CONF_FILE}")
    config = json.load(configfile)
    logging.info(f"config loaded:\n{config}")


def bind_service():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = config.get("host", "")  # defaults to localhost
    port = config.get("port", 8080)
    logging.info(f"Binding service on port {port}")
    sock.bind((host, port))
    sock.listen(config.get("backlog_queue_size", 2048))


def handle_interrupt(sig, frame):
    global config
    logging.info("Caught SIGINT, reloading server config.")
    load_config()
    if config.get("rebind_on_config_reload"):
        bind_service()


signal.signal(signal.SIGINT, handle_interrupt)
load_config()
bind_service()
active_connections = Queue()
failures = 0

# server loop
while True:
    try:
        while active_connections.qsize() > config.get("max_keepalive_connections", 2048):
            active_connections.get().close()
        conn, addr = sock.accept()
        active_connections.put(conn)
        logging.info(f"Received connection from {addr}")
        date = datetime.datetime.now()
        datestring = date.strftime("%a, %d %b %Y %H:%M:%S %z")
        data = conn.recv(config.get("chunk_size", 1024))
        if not data:
            logging.info("Empty request, skipping.")
            continue
        request = str(data, "utf-8")
        logging.info(f"Received request:\n{request}")
        if re.search("^GET .* HTTP/\d\.\d[\n\r]", request):
            logging.info(f"Sending html response")
            content = f"""<html>
	<body>
		<h1>Hello!</h1>
		<p>The http server is working.</p>
		<p>Page last loaded {datestring}.</p>
	</body>
</html>
"""
            headers = f"""HTTP/1.0 200 OK
Server: Python
Date: {datestring}
Content-type: text/html
Content-Length: {len(content)} 
Last-Modified: {datestring}

"""
            conn.sendall(bytes(headers + content, "utf-8"))
    except Exception:
        failures += 1
        backoff = config.get("failure_backoff_sec", 2)
        logging.exception(
            f"Failure #{failures} when receiving client connection, using {backoff} "
            "second backoff before retrying."
        )
        time.sleep(backoff)
