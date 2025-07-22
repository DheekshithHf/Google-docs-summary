from django.urls import path
from . import views

app_name = 'slackdoc'

urlpatterns = [
    path('events/', views.slack_events, name='slack_events'),
]
