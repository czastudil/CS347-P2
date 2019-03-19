from django.contrib import admin

from .models import (
    Question,
    Course,
    Professor,
    Student,
    TA,
)

admin.site.register(Question)
admin.site.register(Course)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(TA)
