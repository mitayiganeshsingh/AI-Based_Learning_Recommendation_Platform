from django.contrib import admin
from .models import Course, Skill, StudentProfile, Enrollment

admin.site.register(Course)
admin.site.register(Skill)
admin.site.register(StudentProfile)
admin.site.register(Enrollment)
