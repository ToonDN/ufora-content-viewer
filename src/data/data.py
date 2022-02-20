from requests.cookies import cookiejar_from_dict
from data.course import Course
import globals as g
import requests
import json
import asyncio
import pickle
import aiohttp
from datetime import datetime, timedelta
import globals as g
from session.browser_cookies import browser_cookies
from data.announcement import Announcement


class Data:
    def __init__(self) -> None:
        self.init()

    def init(self):
        self.cookies = browser_cookies()
        self.time = datetime.now()

        self.update_courses()

    def update_courses(self):
        if not hasattr(self, "courses"):
            self.courses : "list[Course]"= []

        current_ids = set([c.id for c in self.courses])
        config_ids = set(g.courses)

        to_add = config_ids.difference(current_ids)
        to_remove = current_ids.difference(config_ids)
        
        self.add_courses(list(to_add))
        [self.remove_course(i) for i in list(to_remove)]
        
    
    def r_session(self):
        s = requests.session()
        s.cookies = cookiejar_from_dict(self.cookies)
        return s

    #* =============== Table of contents ====================
    def load_toc(self):
        asyncio.run(self.load_toc_async())

    async def load_toc_async(self):
        # try:
        session = aiohttp.ClientSession(cookies=self.cookies)
        futures = [course.load_toc(session) for course in self.courses]
        await asyncio.gather(*futures)
        await session.close()
        # except:
        #     print('Failed to refresh, make sure you are logged in.')
        #     await session.close()


    #* =============== Download content ======================
    def convert_and_download(self, mapping):
        # Mapping takes {"pptx": "pdf", "mkv": "mp4"}
        asyncio.run(self.convert_and_download_async(mapping))
    
    async def convert_and_download_async(self, mapping):
        session = aiohttp.ClientSession(cookies=self.cookies)
        futures = [course.convert_and_download(session, mapping) for course in self.courses]

        await asyncio.gather(*futures)
        await session.close()


    #* =============== Announcements ===========================
    async def load_announcements_async(self):
        session = aiohttp.ClientSession(cookies=self.cookies)
        futures = [course.get_announcements(session) for course in self.courses]

        await asyncio.gather(*futures)
        await session.close()

        
    #* =============== Quizzes =================================
    async def load_quizzes_async(self):
        session = aiohttp.ClientSession(cookies=self.cookies)
        futures = [course.get_quizzes(session) for course in self.courses]

        await asyncio.gather(*futures)
        await session.close()
        

    #* =============== Assignments =============================
    async def load_assignments_async(self):
        session = aiohttp.ClientSession(cookies=self.cookies)
        futures = [course.get_assignments(session) for course in self.courses]

        await asyncio.gather(*futures)
        await session.close()

    #* =============== Basics ==================================

    async def load_basics_async(self):
        futures = [self.load_announcements_async(), self.load_toc_async(), self.load_assignments_async(), self.load_quizzes_async()]
        await asyncio.gather(*futures)

    def load_basics(self):
        asyncio.run(self.load_basics_async())

    
    #* =============== Manage courses ==========================
    def remove_course(self, id):
        for i, course in enumerate(self.courses):
            if course.id == id:
                self.courses.pop(i)
                return True
        return False

    def add_courses(self, ids):
        params = {}

        while True:
            r = requests.get('https://ufora.ugent.be/d2l/api/lp/1.26/enrollments/myenrollments/', cookies=self.cookies, params=params)
        
            if r.status_code == 200:
                txt = json.loads(r.text)
                paging_info = txt.get("PagingInfo", {})
                items = txt['Items']
                items = [item for item in items if item['OrgUnit']['Id'] in ids]
                self.courses = [Course(item['OrgUnit']['Name'], item['OrgUnit']['Id']) for item in items]

                if paging_info.get("HasMoreItems", False):
                    params = {"bookmark": paging_info.get("Bookmark")}
                else:
                    return True
            else:
                return False

    def load_pinned(self):
        items = []
        r = requests.get('https://ufora.ugent.be/d2l/api/lp/1.26/enrollments/myenrollments/', cookies=self.cookies)

        while True:
            if r.status_code == 200:
                data = json.loads(r.text)
                items += data['Items']
            
                paging_info = data.get("PagingInfo", {})
                if paging_info.get("HasMoreItems", False):
                    bookmark = paging_info.get("Bookmark")
                    
                    if bookmark != None:
                        r = requests.get(f'https://ufora.ugent.be/d2l/api/lp/1.26/enrollments/myenrollments/?bookmark={bookmark}', cookies=self.cookies)
                    else:
                        break
                else:
                    break
            else:
                return False
        
        items = [item for item in items if item['PinDate'] != None]
        self.courses = [Course(item['OrgUnit']['Name'], item['OrgUnit']['Id']) for item in items]
        return True
    

    #* =============== Other ===================================
    @property
    def time_string(self):
        return self.time.strftime("%d/%m/%Y, %H:%M:%S")

    def save(self):
        f = open(g.WD + "data.obj", 'wb+')
        pickle.dump(self, f)
        f.close()


    #* ============== HTML =====================================

    def get_announcements_html(self):
        announcements : "list[Announcement]"= []
        for course in self.courses:
            [announcements.append(announcement) for announcement in course.announcements]
            
        announcements.sort(key= lambda x: x.datetime, reverse=True)

        return "".join([ann.get_html(include_coursename=True) for ann in announcements])

    def get_bottom_links_html(self):
        return  "".join([c.get_bottom_html() for c in self.courses])

    def get_tasks_html(self):
        tasks = []
        for course in self.courses:
            [tasks.append(quiz) for quiz in course.quizzes]
            [tasks.append(assignments) for assignments in course.assignments]
            
        cutoff = datetime.now() - timedelta(days=1)
        tasks = [task for task in tasks if task.dueDate > cutoff]
        
        tasks.sort(key= lambda x: x.dueDate, reverse=False)
        return "".join([t.get_html(include_coursename=True) for t in tasks])
    

    def get_html(self):
        courses_content = "".join([c.get_html() for c in self.courses])
        

        return g.JINJA_ENV.get_template("index.html").render(
            courses_content=courses_content,
            bottom_items=self.get_bottom_links_html(),
            vakken=self.courses, 
            announcements_content=self.get_announcements_html(),
            tasks_content=self.get_tasks_html(),
            lastupdated=self.time_string,
            ) 




            



