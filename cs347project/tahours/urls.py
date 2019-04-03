from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('help', views.help, name="help"),
    path('ask-question', views.AskQuestionView.as_view(), name='ask_question'),
    path('questions', views.QuestionListView.as_view(), name='questions'),
    path('shifts', views.ShiftListView.as_view(), name='shifts'),
    path('swap-shifts', views.ShiftSwapListView.as_view(), name='swap-shifts'),
    path('question-done', views.question_done, name='question-done'),
    path('pickup-shift', views.pickup_shift, name='pickup-shift'),
    path('approve-swap-process', views.approve_swap, name='approve-swap-process'),
    path('add-shift', views.CreateShiftView.as_view(), name='add-shift'),
    path('post-shift', views.post_shift, name='post-shift'),
    path('shift-taken', views.already_taken, name='shift-taken'),
    path('ta-onboard', views.TaInfoView.as_view(), name='ta-onboard'),
    path('approve-swap', views.ProfessorApproveSwap.as_view(), name='approve-swap'),
]
