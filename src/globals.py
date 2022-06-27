from config import *
from jinja2 import Environment, FileSystemLoader

JINJA_ENV : Environment = Environment(loader=FileSystemLoader("templates"))

LOCAL_STORAGE_PATH = local_storage_path
LOCAL_STORAGE_TABLE = local_storage_table

UNIQUE_ID_COUNTER = 0
def UNIQUE_ID():
    global UNIQUE_ID_COUNTER
    UNIQUE_ID_COUNTER += 1;
    return f"unique:{UNIQUE_ID_COUNTER}"
