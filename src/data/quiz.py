from datetime import datetime
import globals as g

class Quiz:
    def __init__(self, course_display_name, course_id, dic : dict) -> None:
        self.course_id = course_id
        self.course_display_name = course_display_name
        
        self.id = dic.get("QuizId")
        self.name = dic.get("Name")
        self.isActive = dic.get("IsActive")
        self.instructionsHtml = dic.get("Instructions").get("Html")
        self.descriptionHtml = dic.get("Description").get("Html")
        self.startDate = datetime.strptime(dic.get("EndDate") or "2000-01-01T00:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ') 
        self.endDate = datetime.strptime(dic.get("StartDate") or "2000-01-01T00:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ') 
        self.dueDate = datetime.strptime(dic.get("DueDate") or "2000-01-01T00:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ') 

    @property
    def url(self):
        return f"https://ufora.ugent.be/d2l/lms/quizzing/user/quiz_summary.d2l?qi={self.id}&ou={self.course_id}"

    
    @property
    def date_string(self):
        return datetime.strftime(self.dueDate, '%d-%m-%y %H:%M')

    def get_html(self, include_coursename=False):
        pre_title = "QUIZ"
        if include_coursename:
            pre_title += f"   {self.course_display_name}"
        pre_title += " - "

        return g.JINJA_ENV.get_template("assignment_tile.html").render(
            url=self.url,
            pre_title=pre_title, 
            title=self.name, 
            subtitle=self.date_string, 
            content=self.instructionsHtml)