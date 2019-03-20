from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views import generic

from .forms import (
    QuestionForm,
)

from .models import (
    Question,
)

# Create your views here.
def index(request):
    return render(request, 'tahours/index.html')

class QuestionListView(generic.ListView):
    model = Question

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.student = request.user.student
            question.save()
            return redirect('/tahours/questions')
    else:
        form = QuestionForm()

    return render(request, 'tahours/student/ask-question.html', {'form': form})

def help(request):
    return HttpResponse("TODO")
