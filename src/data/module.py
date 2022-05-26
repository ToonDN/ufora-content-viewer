import asyncio
import json
import math
from aiohttp import ClientSession
import os
import aiofiles
from data.topic import Topic
import globals as g
from datetime import datetime

class Module:
    def __init__(self, course_id, dic : dict) -> None:
        self.course_id = course_id
        self.modules = [Module(course_id, mod) for mod in dic.get('Modules', [])]
        self.topics = [Topic(course_id, top) for top in dic.get('Topics', [])]
        self.sortOrder = dic.get('SortOrder', -math.inf)
        self.title = dic.get('Title')
        self.id = dic.get('ModuleId')

    
    async def convert_and_download(self, session : ClientSession, convert_mapping : dict, download_list : tuple):
        for module in self.modules:
            await module.convert_and_download(session, convert_mapping, download_list)
        
        for topic in self.topics:
            await topic.convert_and_download(session, convert_mapping, download_list)

    
    @property
    def items(self):
        items = self.topics + self.modules
        items.sort(key=lambda x: x.sortOrder)
        return items

    def all_topics(self) -> set:
        result = set()
        for module in self.modules:
            result = result.union(module.all_topics())
        
        for topic in self.topics:
            result.add(topic)

        return result

    def get_html(self):
        content = ''

        for item in self.items:
            if type(item) == Module:
                content += item.get_html()
            else:
                content += item.get_html()
        return g.JINJA_ENV.get_template("module_tile.html").render(title=self.title, content=content)