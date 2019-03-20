from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'tahours/index.html')

@login_required
def ask_question(request):
    return render(request, 'tahours/student/ask-question.html')

def help(request):
    return HttpResponse("TODO")
