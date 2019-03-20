from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins
from django.views import generic

from .forms import (
    QuestionForm,
)

from .models import (
    Question,
    Shift,
)

# Create your views here.
def index(request):
    return render(request, 'tahours/index.html')

def help(request):
    return render(request, 'tahours/help.html')

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

    return render(request, 'tahours/ask-question.html', {'form': form})

class ShiftListView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.ListView):
    model = Shift
    queryset = Shift.objects.filter(is_available=True)
    raise_exception = False
    permission_denied_message = (
        "Only TAs are able to access this page. Please talk to a professor to"
        " ensure that your TA access has been configured correctly."
    )

    def test_func(self):
        return hasattr(self.request.user, 'ta')

# def shift_swap(request):
#     if not hasattr(request.user, 'ta'):
#         return redirect('/accounts/login?next=/tahours/shifts')
#     return render(request, 'tahours/shift_list.html')
