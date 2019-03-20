from django.forms import ModelForm

from .models import (
    Question,
    Shift,
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
