from django.urls import path
from . import views

app_name = 'bc_events'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('sign-in/', views.SignInView.as_view(), name='sign-ins'),
]