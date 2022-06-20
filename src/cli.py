import gevent.monkey
gevent.monkey.patch_all()

from helper_functions import create_directories, Config
from data.data import Data
import config as C
import typer



app = typer.Typer()


@app.command()
def build(output_directory: str = typer.Option(..., "--output"),
          courses: str = typer.Option(...),
          download_filetypes: str = typer.Option("", "--download"),
          convert_filetypes: str = typer.Option("", "--convert"),
          max_size: int = typer.Option(10)):

    courses = list({int(c) for c in courses.split(",")})
    download_list = [i for i in download_filetypes.split(",")]
    convert_dict = [i.split(":")
                    for i in convert_filetypes.split(",") if i != ""]
    convert_dict = {i[0]: i[1] for i in convert_dict}

    config = Config(output_directory, courses)

    create_directories(config)
    print("Trying to log in")
    data = Data(config)

    if data.cookies == None:
        print("No good cookies found")
        exit()

    if (len(download_list) != 0 and len(convert_dict.keys()) != 0):
        print("Loading table of contents")
        data.load_toc()
        print("Converting and downloading files")
        data.convert_and_download(convert_dict, download_list)
        print("Reload all files")
        data.load_basics()
    else:
        print("Loading basics")
        data.load_basics()

    print("Generating html")
    x = data.get_html()

    print("Writing files")
    with open(f"{config.export_dir}/index.html", "w+") as f:
        f.write(x)

    print("DONE")


if __name__ == "__main__":
    app()
