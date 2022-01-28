import json
import logging

CONF_FILE = "serverconf.json"
configfile = open(CONF_FILE)

def load_config():
    global configfile
    configfile.seek(0)
    logging.info(f"Loading configuration from {CONF_FILE}")
    config = json.load(configfile)
    logging.info(f"config loaded:\n{config}")
    return config
