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

from .forms import (
    QuestionForm,
)

from .models import (
    Question,
    Shift,
    ShiftSwap,
)


def index(request):
    return render(request, 'tahours/index.html')


def help(request):
    return render(request, 'tahours/help.html')


class QuestionListView(generic.ListView):
    model = Question
    queryset = Question.objects.filter(completed=False)


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
        question.completed = False
        question.save()
        return super().form_valid(form)

    def test_func(self):
        return hasattr(self.request.user, 'student')


class ShiftListView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.ListView):
    model = Shift
    raise_exception = False
    permission_denied_message = (
        "Only TAs are able to access this page. Please talk to a professor to"
        " ensure that your TA access has been configured correctly."
    )

    def get_queryset(self):
        return Shift.objects.filter(owner=self.request.user.ta)

    def test_func(self):
        return hasattr(self.request.user, 'ta')


class ShiftSwapListView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.ListView):
    model = ShiftSwap
    queryset = ShiftSwap.objects.filter(picked_by=None)
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

def pickup_shift(request):
    if request.method == 'POST':
        id = request.POST['shiftswap_id']
        swap = ShiftSwap.objects.get(pk=id)
        swap.picked_by = request.user.ta
        swap.save()
        return redirect('/tahours/swap-shifts')

def post_shift(request):
    if request.method == 'POST':
        shift_id = request.POST['shift_id']
        shift = Shift.objects.get(pk=shift_id)
        shift.is_available = True;
        shift.owner = None;
        swap = ShiftSwap()
        swap.posted_by = request.user.ta
        swap.shift = Shift.objects.get(pk=shift_id)
        # The swap must be saved first because if it fails then we must not
        # modify the original shift (so that the user can attempt to post the
        # shift again).
        swap.save()
        shift.save()

        return redirect('/tahours/shifts')

