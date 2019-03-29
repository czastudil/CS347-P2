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
]
