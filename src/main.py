import gevent.monkey
gevent.monkey.patch_all()

from helper_functions import *
from jinja2 import Environment, FileSystemLoader
import shutil
import os
from globals import DOWNLOADS_DIR, ED, LOCAL_STORAGE_PATH, LOCAL_STORAGE_TABLE, RUN_DIR, TEMP_DIR
from data.data import Data
import sys
from time import time



data: Data = None


def build():
    global data

    create_directories()
    print("Trying to log in")
    data = Data()

    if data.cookies == None:
        print("No good cookies found")
        exit()

    print("Loading basics")
    data.load_basics()

    print("Writing files")
    x = data.get_html()

    with open(f"{ED}/index.html", "w+") as f:
        f.write(x)


def download():
    global data

    print("Starting conversion and downloading")
    data.convert_and_download({"pptx": "pdf", "ppt": "pdf"})
    print("Conversion and downloading done")


if __name__ == "__main__":
    cmd = sys.argv[1]

    if cmd == "build":
        build()

    elif cmd == "download":
        build()
        download()
        build()

    exit()


# rendered = env.get_template("index.html").render(title="azerazerazr", vakken=data.courses)


# index = rendered

# Write index
# with open(f"{ED}/index.html", "w+") as f:
    # f.write(index)


# x = Data()


# x.load_toc()

# print(x.courses[0].display_name)
