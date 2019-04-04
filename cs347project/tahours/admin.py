from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Question,
    Course,
    Shift,
    ShiftSwap,
    Professor,
    Student,
    TA,
    TaInfo,
    Availability,
)

admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Course)
admin.site.register(Shift)
admin.site.register(ShiftSwap)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(TaInfo)
admin.site.register(Availability)
admin.site.register(TA)
