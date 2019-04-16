import datetime

from django import forms
from django.forms import ModelForm

from .models import (
    Question,
    Shift,
    TaInfo,
)


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = [
            'course',
            'professor',
            'assignment',
            'question',
        ]


class OnboardForm(ModelForm):
    class Meta:
        model = TaInfo
        fields = [
          'min_hours',
          'max_hours',
          'sun_avail',
          'mon_avail',
          'tues_avail',
          'wed_avail',
          'thur_avail',
        ]
        labels = {
          'min_hours': 'Minimum Hours/Week',
          'max_hours': 'Maximum Hours/Week',
          'sun_avail': 'Sunday Availability (from 1pm - 11pm)',
          'mon_avail': 'Monday Availability (from 5pm - 11pm)',
          'tues_avail': 'Tuesday Availability (from 5pm - 11pm)',
          'wed_avail': 'Wednesday Availability (from 5pm - 11pm)',
          'thur_avail': 'Thursday Availability (from 5pm - 11pm)',
        }

class ShiftForm(ModelForm):

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    def clean(self):
        cleaned_data = super().clean()
        ta = cleaned_data.get('owner')
        course = cleaned_data.get('course')
        if course not in ta.courses.all():
            msg = f"{course} is not valid for {ta}"
            self.add_error('owner', msg)
            self.add_error('course', msg)

        date = cleaned_data.get('date')
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')

        if start > end:
            self.add_error('start_time', "Start must be before end")
            self.add_error('end_time', "End must be after start")

        cleaned_data['start'] = datetime.datetime.combine(date, start)
        cleaned_data['end'] = datetime.datetime.combine(date, end)

        return cleaned_data

    class Meta:
        model = Shift
        fields = [
            'date',
            'start_time',
            'end_time',
            'course',
            'owner',
        ]
