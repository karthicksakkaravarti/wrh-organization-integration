from django.http import HttpResponse
import csv

from dynamic_preferences.registries import global_preferences_registry

global_pref = global_preferences_registry.manager()
from operator import attrgetter

def download_csv(query_set, filename, type):
    writer = None
    export_pref = global_pref["core_backend__global_export"]  # dynamic_preference
    try:
        with open('temp_file.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[i.get("text", "-") for i in export_pref[type]])
            writer.writeheader()
            for obj in query_set:
                try:
                    writer.writerow(
                        {field.get("text"): attrgetter(field.get("value"))(obj) for field in export_pref[type]}
                    )
                except Exception as e:
                    print(str(e))
                    continue
    except Exception as e: print(e)
    with open('temp_file.csv', 'rb') as infile:
        response = HttpResponse(infile, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={filename}.csv'
        return response