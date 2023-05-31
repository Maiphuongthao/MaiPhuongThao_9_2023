from django.urls import path
from django.contrib.auth import views as auth_views
from .views import DeleteSubscriptionView

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('subscriptions/', views.subscription, name='subscriptions'),
    path('subscriptions/<int:pk>/delete', DeleteSubscriptionView.as_view(), name="delete_subscription" )
]