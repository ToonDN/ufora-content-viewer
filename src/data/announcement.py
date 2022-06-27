from aiohttp import ClientSession
import globals as g
from datetime import datetime


class Announcement:
    def __init__(self, course_id, course_display_name, dic : dict) -> None:
        self.course_id = course_id
        self.course_display_name = course_display_name
        self.id = dic['Id']
        self.title = dic['Title']
        self.html = dic['Body']['Html']
        # print(dic["CreatedDate"])
        self.datetime = datetime.strptime(dic['CreatedDate'] or "2000-01-01T00:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ')
        self.fullid = f"{self.course_id}:ann{self.id}"
        

    @property
    def date_string(self):
        return datetime.strftime(self.datetime, '%d-%m-%y %H:%M')

    def get_html(self, include_coursename = False):
        title = self.title
        if include_coursename:
            title = f"<b> {self.course_display_name} - </b>" + title
        return g.JINJA_ENV.get_template("announcement_tile.html").render(title=title, date_string=self.date_string, content=self.html, id=g.UNIQUE_ID(), localstoragekey=self.fullid)