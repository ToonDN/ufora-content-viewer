from globals import DOWNLOADS_DIR, ED, LOCAL_STORAGE_PATH, LOCAL_STORAGE_TABLE, RUN_DIR, TEMP_DIR
import os
import shutil

def create_directories():
    # Create root dir
    if not os.path.exists(ED):
        os.makedirs(ED)

    # Create and copy components dir
    if not os.path.exists(f"{ED}/components"):
        shutil.copytree(f"{RUN_DIR}/components", f"{ED}/components")

    # Create downloads dir
    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)

    # Create temp directory
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)