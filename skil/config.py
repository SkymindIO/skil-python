import json
import os


def mkdir(x):
    if not os.path.isdir(x):
        os.mkdir(x)


_USER_PATH = os.path.expanduser('~')
_DL4J_DIR = os.path.join(_USER_PATH, '.deeplearning4j')
mkdir(_DL4J_DIR)
_BASE_DIR = os.path.join(_DL4J_DIR, 'pyskil')
mkdir(_BASE_DIR)

_SKIL_DIR = os.path.join(_BASE_DIR, '.skil')

DEFAULT_SKIL_CONFIG = {
    'host': 'localhost',
    'port': '9008',
    'username': 'admin',
    'password': 'admin'
}

SKIL_CONFIG = {}


def save_skil_config(config):
    global SKIL_CONFIG
    SKIL_CONFIG = config
    with open(_SKIL_DIR, 'w') as f:
        json.dump(SKIL_CONFIG, f)


def load_skil_config():
    global SKIL_CONFIG
    if os.path.isfile(_SKIL_DIR):
        with open(_SKIL_DIR, 'r') as f:
            SKIL_CONFIG = json.load(f)
    else:
        SKIL_CONFIG = DEFAULT_SKIL_CONFIG
