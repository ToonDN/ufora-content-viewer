import asyncio
import json
import math
from aiohttp import ClientSession
import os
import aiofiles
from data.module import Module
import globals as g
from datetime import datetime, timedelta
from data.announcement import Announcement
from data.quiz import Quiz
from data.assignment import Assignment
from data.topic import Topic
from globals import CONFIG as c

class Course:
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        self.toc : list(Module) = []
        self.announcements : list(Announcement) = []
        self.quizzes : list(Quiz) = []
        self.assignments : list(Assignment) = []
        

    @property
    def display_name(self) -> str:
        return self.name.split(' - ', 1)[1]

    def all_topics(self) -> "list[Topic]":
        # Returns a list of all topics in the course
        result = set()
        for module in self.toc:
            result = result.union(module.all_topics())
        return list(result)

    async def convert_and_download(self, session : ClientSession, convert_mapping : dict , download_list : tuple):
        for module in self.toc:
            await module.convert_and_download(session, convert_mapping, download_list)


    async def load_toc(self, session : ClientSession):
        url = f'https://ufora.ugent.be/d2l/api/le/1.26/{ self.id }/content/toc'
        r = await session.request(method="GET", url=url)

        if r.status == 200:
            self.toc = [Module(self.id, module_dict) for module_dict in json.loads(await r.read())['Modules']]

    def print(self):
        print(f'ID: {self.id}   -    NAME: {self.name}')

    async def get_announcements(self, session : ClientSession):
        r = await session.get(f'https://ufora.ugent.be/d2l/api/le/1.50/{ self.id }/news/')
        if r.status == 200:
            self.announcements = [Announcement(self.id, self.display_name, a_dict) for a_dict in json.loads(await r.read())]
            
    async def get_quizzes(self, session : ClientSession):
        r = await session.get(f'https://ufora.ugent.be/d2l/api/le/1.33/{ self.id }/quizzes/')
        if r.status == 200:
            
            self.quizzes = [Quiz(self.display_name, self.id, dic) for dic in json.loads(await r.read())["Objects"]]
            
    async def get_assignments(self, session : ClientSession):
        r = await session.get(f'https://ufora.ugent.be/d2l/api/le/1.33/{ self.id }/dropbox/folders/')
        if r.status == 200:
            self.assignments = [Assignment(self.display_name, self.id, dic) for dic in json.loads(await r.read())]
            
    @property
    def vtk_url(self):
        return c.custom_vtk_url_map.get(self.id, f'https://vtk.ugent.be/wiki/{ self.display_name.replace(" ", "-") }')


    def get_toc_html(self):
        content = ''.join([m.get_html() for m in self.toc])
        return g.JINJA_ENV.get_template("toc.html").render(display_name=self.display_name, content=content)

    def get_announcements_html(self):
        return "".join([a.get_html() for a in self.announcements])

    def get_html(self):
        return g.JINJA_ENV.get_template("course.html").render(
            id=self.id, 
            toc_html=self.get_toc_html(), 
            announcements_html=self.get_announcements_html(), 
            tasks_html=self.get_tasks_html()
            ) 

    def get_tasks_html(self):
        tasks = []
        [tasks.append(quiz) for quiz in self.quizzes]
        [tasks.append(assignments) for assignments in self.assignments]
            
        cutoff = datetime.now() - timedelta(days=1)
        tasks = [task for task in tasks if task.dueDate > cutoff]
        
        tasks.sort(key= lambda x: x.dueDate, reverse=False)
        content = "".join([task.get_html() for task in tasks])
        return content

    def get_bottom_html(self):
        return g.JINJA_ENV.get_template("bottom_links.html").render(
            id=self.id,
            tests_url= f"https://ufora.ugent.be/d2l/lms/quizzing/user/quizzes_list.d2l?ou={self.id}",
            assignments_url = f"https://ufora.ugent.be/d2l/lms/dropbox/user/folders_list.d2l?ou={self.id}",
            grades_url = f"https://ufora.ugent.be/d2l/lms/grades/my_grades/main.d2l?ou={self.id}",
            content_url= f"https://ufora.ugent.be/d2l/le/content/{self.id}/Home",
            groups_url = f"https://ufora.ugent.be/d2l/lms/group/user_group_list.d2l?ou={self.id}",
            announcements_url = f"https://ufora.ugent.be/d2l/lms/news/main.d2l?ou={self.id}",
            vtk_url = self.vtk_url,
            )