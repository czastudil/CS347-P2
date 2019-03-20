from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('help', views.help, name="help"),
    path('ask-question', views.ask_question, name='ask_question'),
    path('questions', views.QuestionListView.as_view(), name='questions'),
    path('shifts', views.ShiftListView.as_view(), name='shifts'),
]
