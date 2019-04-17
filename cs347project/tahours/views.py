import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import (
    PermissionDenied,
    ValidationError,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins
from django.views import (
    generic,
    View
)

from .forms import (
    QuestionForm,
    ShiftForm,
    OnboardForm,
)

from .models import (
    Question,
    Shift,
    ShiftSwap,
)

def user_has_role(user, role_name):
    return hasattr(user, role_name)


def index(request):
    """
    Renders the application index page
    """

    return render(request, 'tahours/index.html')


def help(request):
    """
    Renders the help/FAQ page
    """

    return render(request, 'tahours/help.html')


def already_taken(request):
    """
    Displays a message that the shift was already taken
    """

    # TODO: Do this cleaner
    return render(request, 'tahours/already-taken.html')


class QuestionListView(generic.ListView):
    """
    Lists all of the questions that have not been answered.
    """

    model = Question
    queryset = Question.objects.filter(completed=False)


class AskQuestionView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.edit.FormView):
    """
    Displays the form to ask a question but limits access to logged in users
    who have the 'student' role.
    """

    raise_exception = False
    form_class = QuestionForm
    success_url = '/questions'
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


class TaInfoView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.edit.FormView):
    """
    Ta onboarding view
    """

    raise_exception = False
    form_class = OnboardForm
    success_url = '/shifts'
    permission_denied_message = (
        "Only TAs are able to access this page. Please talk to a professor to"
        " ensure that your TA access has been configured correctly."
    )
    template_name = 'tahours/ta-onboard.html'
    
    def form_valid(self, form):
        info = form.save(commit=False)
        info.save()
        self.request.user.ta.ta_info = info
        self.request.user.ta.save()
        form.save_m2m()
        return super().form_valid(form)

    def test_func(self):
        return hasattr(self.request.user, 'ta')


class CreateShiftView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.edit.FormView):
    """
    Displays the form to add/create a shift. This page is only accessible by
    professors.
    """

    raise_exception = False
    form_class = ShiftForm
    success_url = "/shifts"
    template_name = 'tahours/create-shifts.html'
    permission_denied_message = (
        "Only professors are able to access this page. If you believe you have"
        " received this message in error, please contact a system administrator"
    )

    def form_valid(self, form):
        shift = form.save(commit=False)
        shift.start = form.cleaned_data['start']
        shift.end = form.cleaned_data['end']
        shift.is_available = False
        shift.save()
        return super().form_valid(form)

    def test_func(self):
        return hasattr(self.request.user, 'professor')


class ShiftListView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.ListView):
    """
    Displays all shifts currently assigned to the logged-in user. Limits access
    to TAs.
    """

    model = Shift
    raise_exception = False
    permission_denied_message = (
        "Only TAs are able to access this page. Please talk to a professor to"
        " ensure that your TA access has been configured correctly."
    )

    def get_queryset(self):
        if user_has_role(self.request.user, 'ta'):
            return Shift.objects.filter(owner=self.request.user.ta, start__gte=datetime.date.today())
        else:
            return Shift.objects.filter(start__gte=datetime.date.today())

    def test_func(self):
        user = self.request.user
        return user_has_role(user, 'ta') or user_has_role(user, 'professor')


class ProfessorApproveSwap(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.ListView):
    models = ShiftSwap
    raise_exception = False
    template_name = 'tahours/approve-swap.html'
    permission_denied_message = (
        "Only professors have access to view this page. Please talk to a system"
        " administrator if you believe you are receiving this message in error"
    )

    def get_queryset(self):
        return ShiftSwap.objects.filter(approved_by=None).exclude(picked_by=None)

    def test_func(self):
        return user_has_role(self.request.user, 'professor')


class ShiftSwapListView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.ListView):
    """
    Displays all shifts that are able to be picked up by a TA.
    """

    model = ShiftSwap
    #queryset = ShiftSwap.objects.filter(picked_by=None)
    raise_exception = False
    permission_denied_message = (
        "Only TAs are able to access this page. Please talk to a professor to"
        " ensure that your TA access has been configured correctly."
    )

    def get_queryset(self):
        return ShiftSwap.objects.filter(picked_by=None)

    def test_func(self):
        user = self.request.user
        return user_has_role(user, 'ta')


def question_done(request):
    """
    Handles the form when a question is marked as done. Redirects the user
    back to the question list.
    """

    # TODO: Limit access to TAs

    if request.method == 'POST':
        id = request.POST['question_id']
        question = Question.objects.get(pk=id)
        question.completed = True
        question.save()
        return redirect('/questions')


def pickup_shift(request):
    """
    Handles the form when a shift is picked up. Redirects the user back to the
    available shifts list.
    """

    if request.method == 'POST':
        id = request.POST['shiftswap_id']
        swap = ShiftSwap.objects.get(pk=id)
        if not swap.picked_by:
            swap.picked_by = request.user.ta
            swap.save()
            return redirect('/swap-shifts')
        else:
            return redirect('/shift-taken')
    return redirect('/swap-shifts')


def approve_swap(request):
    if request.method == 'POST':
        id = request.POST['shiftswap_id']
        swap = ShiftSwap.objects.get(pk=id)
        if not swap.approved_by:
            swap.approved_by = request.user.professor
            swap.shift.owner = swap.picked_by
            swap.shift.is_available = False
            swap.shift.save()
            swap.save()
            return redirect('/approve-swap')
        else:
            return redirect('/')
    return redirect('/approve-swap')


def post_shift(request):
    """
    Handles the form when a shift is marked as available. Redirects the user
    to the list of shifts currently assigned to them.
    """

    if request.method == 'POST':
        shift_id = request.POST['shift_id']
        shift = Shift.objects.get(pk=shift_id)
        shift.is_available = True;
        swap = ShiftSwap()
        swap.posted_by = request.user.ta
        swap.shift = Shift.objects.get(pk=shift_id)
        # The swap must be saved first because if it fails then we must not
        # modify the original shift (so that the user can attempt to post the
        # shift again).
        swap.save()
        shift.save()

        return redirect('/shifts')
