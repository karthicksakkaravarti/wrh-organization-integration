import datetime
from dateutil.rrule import YEARLY, rrule, rruleset
from django.conf.locale import lt
from django.test import RequestFactory
from django.conf import settings
from django_cal.views import Events
from .models import Event

class WRHEventsIcalFeed(Events):
    """
    A WRH Event Calender
    """

    def get_object(self,request  ,*args, **kwargs):
        if request.GET.get('event_id', None):
            return Event.objects.filter(id=request.GET.get('event_id', None))
        return Event.objects.all().order_by('-create_datetime')

    def items(self, obj):
        return obj

    def filename(self, item):
        return "WRHEvent.ics"

    def item_description(self, item):
        return item.description

    def item_summary(self, item):
        return item.name

    def item_start(self, item):
        return item.start_date

    def item_url(self, item):
        return "/static/vue/#/event-profile/" + str(item.id)

    def item_end(self, item):
        return item.end_date

    def item_location(self, item):
        return f"{item.city if item.city else ''}  {item.state if item.state else ''}  {item.country if item.country else ''}"

    def item_categories(self, item):
        return ["Public"]

    def item_uid(self, item):
        return str(item.id) + "@events.bicyclecolorado.org"

