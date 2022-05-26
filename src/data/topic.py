import asyncio
import json
import math
from aiohttp import ClientSession
import os
import aiofiles
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from globals import CONFIG as c
import globals as g

class Topic:
    def __init__(self, course_id, dic : dict) -> None:
        self.course_id = course_id
        self.title = dic.get('Title')
        self.id = dic.get('TopicId')
        self.typeIdentifier : str = dic.get('TypeIdentifier')
        self.url : str = dic.get('Url')
        self.lastModified = dic.get('LastModifiedDate')
        self.read = not dic.get('Unread', False)
        self.sortOrder = dic.get('SortOrder')
        self.fullid = f"{self.course_id}:topic{self.id}"

        if self.typeIdentifier == 'File':
            self.type = self.url.split('.')[-1]
        else:
            self.type = self.typeIdentifier


    def direct_download_url(self):
        return 	f"https://ufora.ugent.be/d2l/le/content/{self.course_id}/topics/files/download/{self.id}/DirectFileTopicDownload"

    @property
    def usable_url(self):
        if self.is_downloaded:
            return c.downloads_dir + '/' + [name for name in os.listdir(c.downloads_dir) if str(self.full_id) in name][0]

        if self.typeIdentifier == 'Link' and '/d2l/' not in self.url:
            return self.url
        else:
            return 'https://ufora.ugent.be' + self.url
        
    @property
    def full_id(self):
        return f"{self.course_id}_{self.id}"

    @property
    def is_downloaded(self):
        return str(self.full_id) in [name.split(".")[0] for name in os.listdir(c.downloads_dir)]

    async def convert_and_download(self, session : ClientSession, convert_mapping : dict, download_list : tuple):
        if not self.is_downloaded:
            if self.type in convert_mapping.keys():
                in_ft = self.type
                out_ft = convert_mapping.get(self.type)
                # Define filenames
                temp_file = f'{c.temp_dir}/{self.full_id}.{in_ft}'
                final_file = f'{c.downloads_dir}/{self.full_id}.{out_ft}'
                print(f"--- Downloading {self.title}")

                # Download file
                async with session.get(self.usable_url) as resp:
                    f = await aiofiles.open(temp_file, 'wb+')
                    await f.write(await resp.read())
                    await f.close()

                # Convert file
                if in_ft in ("ppt", "pptx") and out_ft == "pdf":
                    os.system(f"libreoffice --headless --invisible --convert-to pdf {temp_file} --outdir {c.downloads_dir} && rm {temp_file}")
                elif in_ft in ("mkv") and out_ft == "mp4":
                    os.system(f"ffmpeg -i {temp_file} {final_file}")
            elif (download_list == None or self.type in download_list) and self.type != "Link":
                ft = self.type
                # Define filenames
                temp_file = f'{c.temp_dir}/{self.full_id}.{ft}'
                final_file = f'{c.downloads_dir}/{self.full_id}.{ft}'
                print(f"--- Downloading {self.title}")

                # Download file
                async with session.get(self.usable_url) as resp:
                    f = await aiofiles.open(temp_file, 'wb+')
                    await f.write(await resp.read())
                    await f.close()
                os.system(f"mv {temp_file} {final_file}")

    def get_html(self):
        return g.JINJA_ENV.get_template("topic_tile.html").render(
            url=self.usable_url, 
            title=self.title, 
            type=self.type, 
            direct_download_url=self.direct_download_url(), 
            id1=g.UNIQUE_ID(), 
            localstoragekey1=f"{self.fullid}:text",
            id2=g.UNIQUE_ID(), 
            localstoragekey2=f"{self.fullid}:checked")