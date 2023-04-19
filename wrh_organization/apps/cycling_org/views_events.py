from datetime import date

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView
from dynamic_preferences.registries import global_preferences_registry

from .forms import EventEditForm
from .models import Event, OrganizationMember
from .views_results import races, race_results

global_pref = global_preferences_registry.manager()


@method_decorator(csrf_exempt, name='dispatch')
class EventDetails(DetailView):
    template_name = 'BC/EventDetails.html'
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GOOGLE_MAP_API_TOKEN'] = settings.GOOGLE_MAP_API_TOKEN
        context['Races'] = races(event=context['object'])
        context['RaceResults'] = race_results(event=context['object'])
        return context


def event_edit(request, pk=None):
    if request.method == 'POST':
        form = EventEditForm(request.POST)
        if form.is_valid():
            # form.save()
            print(form)
        else:
            messages.error(request, 'Please correct the error below.')
    elif request.method == 'GET':
        if pk:
            event = get_object_or_404(Event, id=pk)
            context = {'form': EventEditForm(instance=event), 'id': pk, 'OrgsAdmin': OrganizationMember.objects.filter(
                Q(member=request.user.member) and (Q(is_admin=True) or Q(is_master_admin=True)))}
            # print(context['OrgsAdmin'])
            return render(request, 'BCforms/EventForm.html', context)
    form = EventEditForm()
    return render(request, 'BCforms/EventForm.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class Events(TemplateView):
    template_name = 'BC/Events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Event'] = Event.objects.all().order_by('start_date').filter(end_date__gte=date.today())
        context['Featured'] = Event.objects.all().order_by('start_date').filter(
            Q(featured_event=True) & Q(end_date__gte=date.today()))
        context['EventTypes'] = global_pref['core_backend__event_tags']
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        query_set = Event.objects.all().order_by('start_date')
        query = Q(end_date__gte=date.today())
        if request.POST.get("filter", None) == 'usac_event':
            query &= Q(is_usac_permitted=True)
        if request.POST.get("filter", None) == 'featured':
            query &= Q(featured_event=True)
        if request.POST.get("event-type", None) and 'all' != request.POST.get("event-type", None):
            query &= Q(tags__contains=[request.POST.get("event-type", None)])
        # print(query)
        context['Event'] = query_set.filter(query)
        return self.render_to_response(context)
