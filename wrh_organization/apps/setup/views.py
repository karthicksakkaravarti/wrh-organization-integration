import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from backend1.helpers.Exception import exception

from apps.Setup.models import AppBasic
from django.views.generic import TemplateView

log = logging.getLogger('apps')


class SetupGuard(View):
    """
    Initital Setup
    """
    def get(self, request, *args, **kwargs):
        try:
            try:
                AppBasic.objects.get(config_name='AppName')
                return HttpResponseRedirect(reverse('home'))
            except Exception as e:
                log.warning(f"AppName not found. Redirecting to Setup Page")
                return HttpResponseRedirect(reverse('Setup:setup-inital'))

        except Exception as e:
            exception(e)


class Setupinitial(TemplateView):
    template_name = 'InitialSetup.html'

    def post(self, request, *args, **kwargs):

        try:
            AppBasic.objects.create(config_name='AppName', value=request.POST.get('appname'))
            return HttpResponseRedirect(reverse('home'))
        except Exception as e:
            exception(e)
        return render(request, self.template_name, context={})