import gevent.monkey
gevent.monkey.patch_all()
from time import time
import sys
from data.data import Data
import os
import shutil
from jinja2 import Environment, FileSystemLoader
from helper_functions import *
from globals import CONFIG as c



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

    with open(f"{c.export_dir}/index.html", "w+") as f:
        f.write(x)


def download():
    global data

    print("Starting conversion and downloading")
    data.convert_and_download({"pptx": "pdf", "ppt": "pdf"}, tuple())
    print("Conversion and downloading done")

def download_all():
    global data

    print("Starting conversion and downloading")
    data.convert_and_download({"pptx": "pdf", "ppt": "pdf"}, ("png", "pdf", "html"))
    print("Conversion and downloading done")


if __name__ == "__main__":
    cmd = sys.argv[1]

    if cmd == "build":
        build()

    elif cmd == "download":
        build()
        download()
        build()

    elif cmd == "export":
        if (len(sys.argv) < 4):
            print("\nUsage of export is: ufora export [DIRECTORY] [ORGUNITID]")
            exit()

        directory = sys.argv[2]
        orgunitid = int(sys.argv[3])

        c.set_export_directory(directory)
        c.orgunitids = (orgunitid,)
        build()
        download_all()
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
