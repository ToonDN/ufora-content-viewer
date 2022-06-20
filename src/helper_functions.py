import os
import shutil
import config as C


class Config:
    def __init__(self, export_directory: str, orgunitids: "list(str)") -> None:
        self.run_dir = os.getcwd()
        self.export_dir = export_directory
        self.downloads_dir = export_directory + "/downloads"
        self.temp_dir = export_directory + "/temp"
        self.orgunitids = orgunitids

    def set_export_directory(self, export_directory):
        self.export_dir = export_directory
        self.downloads_dir = export_directory + "/downloads"
        self.temp_dir = export_directory + "/temp"

def create_directories(c : Config):
    print(c.downloads_dir)
    # Create root dir
    if not os.path.exists(c.export_dir):
        os.makedirs(c.export_dir)

    # Create and copy components dir
    if not os.path.exists(f"{c.export_dir}/components"):
        shutil.copytree(f"{c.run_dir}/components", f"{c.export_dir}/components")

    # Create downloads dir
    if not os.path.exists(c.downloads_dir):
        os.makedirs(c.downloads_dir)

    # Create temp directory
    if not os.path.exists(c.temp_dir):
        os.makedirs(c.temp_dir)