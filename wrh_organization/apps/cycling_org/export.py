import datetime

from django.http import HttpResponse
import csv
from dynamic_preferences.registries import global_preferences_registry
from operator import attrgetter

global_pref = global_preferences_registry.manager()


def download_csv(query_set, filename, type):
    """
    query_set: filter query set
    filename: export file name
    type: Type of export . eg: OrganizationMember
    """
    # Get the current date and time
    now = datetime.datetime.now()
    # specific format
    now_format = now.strftime("%Y-%m-%d %H:%M:%S")
    # Getting  dynamic_preference
    export_pref = global_pref["core_backend__global_export"]
    # Create the HttpResponse object with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"attachment; filename={filename}_{now_format}.csv"
    # Write CSV data to response
    writer = csv.writer(response)
    # CSV adding headers
    writer.writerow([i.get("text", "-") for i in export_pref[type]])
    for obj in query_set:
        writer.writerow([attrgetter(field.get("value"))(obj) for field in export_pref[type]])
    return response
