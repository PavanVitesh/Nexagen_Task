from django.urls import path
from . import views

urlpatterns = [
    path('', views.fetch_unread_emails, name='fetch_emails'),
]
