import os
import shutil
from globals import CONFIG as c

def create_directories():
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