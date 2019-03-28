from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins
from django.views import (
    generic,
    View
)

from .decorators import (
    check_role
)

from .forms import (
    QuestionForm,
)

from .models import (
    Question,
    Shift,
)


def index(request):
    return render(request, 'tahours/index.html')


def help(request):
    return render(request, 'tahours/help.html')


class QuestionListView(generic.ListView):
    model = Question


class AskQuestionView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.edit.FormView):
    raise_exception = False
    form_class = QuestionForm
    success_url = '/tahours/questions'
    template_name = 'tahours/ask-question.html'
    permission_denied_message = (
        "Only students are able to access this page. Please talk to a professor to"
        " ensure that your student access has been configured correctly."
    )

    def form_valid(self, form):
        question = form.save(commit=False)
        # Student must be saved from the user data since it is not an entry
        # on the form
        question.student = self.request.user.student
        question.save()
        return super().form_valid(form)

    def test_func(self):
        return hasattr(self.request.user, 'student')


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

def question_done(request):
    if request.method == 'POST':
        id = request.POST['question_id']
        question = Question.objects.get(pk=id)
        question.completed = True
        question.save()
        return redirect('/tahours/questions')

