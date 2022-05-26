import os
from config import *
from jinja2 import Environment, FileSystemLoader

class Config:
    def __init__(self) -> None:
        self.run_dir = os.getcwd()
        self.export_dir = export_directory
        self.downloads_dir = export_directory + "/downloads"
        self.temp_dir = export_directory + "/temp"
        self.custom_vtk_url_map = custom_vtk_url_map
        self.browsers = browsers
        self.orgunitids = courses

    def set_export_directory(self, export_directory):
        self.export_dir = export_directory
        self.downloads_dir = export_directory + "/downloads"
        self.temp_dir = export_directory + "/temp"

CONFIG = Config()

JINJA_ENV : Environment = Environment(loader=FileSystemLoader("templates"))

LOCAL_STORAGE_PATH = local_storage_path
LOCAL_STORAGE_TABLE = local_storage_table

UNIQUE_ID_COUNTER = 0
def UNIQUE_ID():
    global UNIQUE_ID_COUNTER
    UNIQUE_ID_COUNTER += 1;
    return f"unique:{UNIQUE_ID_COUNTER}"
