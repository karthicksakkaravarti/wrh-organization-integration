import requests
from apps.constant_contact.views import authorization_request, callback
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import path

urlpatterns = [
    path('login', authorization_request, name='constant_content_auth_request'),
    path('callback', callback, name='constant_content_callback'),

]
