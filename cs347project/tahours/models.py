from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)


DAYS_OF_WEEK = {
    1: 'Sunday',
    2: 'Monday',
    3: 'Tuesday',
    4: 'Wednesday',
    5: 'Thursday',
}


class DayOfWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(DAYS_OF_WEEK.items()))
        kwargs['max_length'] = 1
        super().__init__(*args, **kwargs)


class Course(models.Model):
    number = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['number']


class User(AbstractUser):
    pass


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    courses = models.ManyToManyField(Course, blank=True)

    def __repr__(self):
        return f"<Student {self.user.username}>"

    def __str__(self):
        return f"{self.user.username}"


class Professor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    courses = models.ManyToManyField(Course, blank=True)

    def __repr__(self):
        return f"<Professor {self.user.username}>"

    def __str__(self):
        return f"{self.user.username}"


class Availability(models.Model):
    dayOfWeek = DayOfWeekField()
    startTime = models.TimeField()
    endTime = models.TimeField()


class TaInfo(models.Model):
    courses = models.ManyToManyField(Course)
    min_hours = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    max_hours = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    availability = models.ManyToManyField(Availability)

    class Meta:
        ordering = ['ta']


class TA(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    ta_info = models.OneToOneField(TaInfo, on_delete=models.SET_NULL, null=True, blank=True)

    def __repr__(self):
        return f"<TA {self.user.username}>"

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "TA"
        verbose_name_plural = "TAs"


class Question(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    time = models.DateTimeField('time asked', auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)
    assignment = models.CharField(max_length=20)
    question = models.TextField(max_length=200)
    completed = models.BooleanField()

    class Meta:
        ordering = ['time']


class Shift(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(TA, on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField()

    def __str__(self):
        return f"<Shift {self.start} - {self.end}>"

    class Meta:
        ordering = ['start', 'end']


class ShiftSwap(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(TA, related_name='posted', on_delete=models.SET_NULL, null=True)
    picked_by = models.ForeignKey(TA, related_name='picked', on_delete=models.SET_NULL, null=True)
    approved_by = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"<ShiftSwap {self.shift}>"

    class Meta:
        ordering = ['shift']

