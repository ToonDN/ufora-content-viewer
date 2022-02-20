import asyncio
import json
import math
from aiohttp import ClientSession
import os
import aiofiles
import globals as g
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

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
            return 'downloads/' + [name for name in os.listdir(g.ED + 'public/downloads') if str(self.full_id) in name][0]

        if self.typeIdentifier == 'Link' and '/d2l/' not in self.url:
            return self.url
        else:
            return 'https://ufora.ugent.be' + self.url
        
    @property
    def full_id(self):
        return f"{self.course_id}_{self.id}"

    @property
    def is_downloaded(self):
        return str(self.full_id) in [name.split(".")[0] for name in os.listdir(g.DOWNLOADS_DIR)]

    async def convert_and_download(self, session : ClientSession, mapping : dict):
        if not self.is_downloaded and self.type in mapping.keys():
            in_ft = self.type
            out_ft = mapping.get(self.type)
            # Define filenames
            temp_file = f'{g.TEMP_DIR}/{self.full_id}.{in_ft}'
            final_file = f'{g.DOWNLOADS_DIR}/{self.full_id}.{out_ft}'
            print(f"--- Downloading {self.title}")

            # Download file
            async with session.get(self.usable_url) as resp:
                f = await aiofiles.open(temp_file, 'wb+')
                await f.write(await resp.read())
                await f.close()

            # Convert file
            if in_ft in ("ppt", "pptx") and out_ft == "pdf":
                os.system(f"libreoffice --headless --invisible --convert-to pdf {temp_file} --outdir {final_file} && rm {temp_file}")
            elif in_ft in ("mkv") and out_ft == "mp4":
                os.system(f"ffmpeg -i {temp_file} {final_file}")

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