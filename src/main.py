from time import time
import gevent.monkey
gevent.monkey.patch_all()
from data.data import Data
from globals import DOWNLOADS_DIR, ED, LOCAL_STORAGE_PATH, LOCAL_STORAGE_TABLE, RUN_DIR, TEMP_DIR
import os
import shutil
from jinja2 import Environment, FileSystemLoader



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


create_directories()
    

data = Data()
data.load_basics()

x = data.get_html()

with open(f"{ED}/index.html", "w+") as f:
    f.write(x)

exit()

# rendered = env.get_template("index.html").render(title="azerazerazr", vakken=data.courses)


# index = rendered 

# Write index
# with open(f"{ED}/index.html", "w+") as f:
    # f.write(index)


# x = Data()



# x.load_toc()

# print(x.courses[0].display_name)


