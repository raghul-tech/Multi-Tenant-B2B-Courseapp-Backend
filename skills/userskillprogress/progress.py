from skills.models import UserSkillProgress,Skills,CourseSkill

class Create_or_update_progress():
    def create_progress(self,user,tenant,course):
        course_id = CourseSkill.objects.get(course = course)


        UserSkillProgress.objects.get_or_create(
            user = user,
            tenant = tenant,
        )
        pass

