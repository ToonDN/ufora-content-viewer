from aiohttp import ClientSession
import globals as g
from datetime import datetime

class Assignment:
    def __init__(self, course_display_name,course_id, dic : dict) -> None:
        self.course_id = course_id
        self.course_display_name = course_display_name
        
        self.id = dic.get("Id")
        self.name = dic.get("Name")
        self.instructionsHtml = dic.get("CustomInstructions").get("Html")
        self.dueDate = datetime.strptime(dic.get("DueDate") or "2000-01-01T00:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ') 
        self.groupTypeId = dic.get("GroupTypeId")
        
    @property
    def url(self):
        return f"https://ufora.ugent.be/d2l/lms/dropbox/user/folders_list.d2l?ou={self.course_id}"
        # return f"https://ufora.ugent.be/d2l/lms/dropbox/user/folder_submit_files.d2l?db={self.id}&grpid={self.groupTypeId}&isprv=0&bp=0&ou={self.course_id}"

    @property
    def date_string(self):
        return datetime.strftime(self.dueDate, '%d-%m-%y %H:%M')

    def get_html(self, include_coursename=False):
        pre_title = "OPDRACHT"
        if include_coursename:
            pre_title += f"   {self.course_display_name}"
        pre_title += " - "

        return g.JINJA_ENV.get_template("assignment_tile.html").render(
            url=self.url,
            pre_title=pre_title,
            title=self.name, 
            subtitle=self.date_string, 
            content=self.instructionsHtml)
