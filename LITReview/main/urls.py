from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='flux'),
    path('createticket', views.create_ticket, name='new_ticket')
]

