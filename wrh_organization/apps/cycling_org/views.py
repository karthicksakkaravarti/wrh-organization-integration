import csv
import traceback
from PIL import Image
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import storage as ck_storage
from wrh_organization.helpers.utils import get_random_upload_path
from django.http import HttpResponse
from .forms import UploadValidateFile  


from .validators import usac_license_on_record, valid_usac_licenses, wrh_club_match, wrh_bc_member, \
    wrh_club_memberships, wrh_email_match, wrh_local_association, wrh_usac_clubs, usac_club_match, bc_race_ready, \
    bc_individual_cup_ready, bc_team_cup_ready

@require_http_methods(["POST"])
@login_required
def ckeditor_upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    try:
        Image.open(request.FILES["upload"]).verify()
    except OSError:
        traceback.print_exc()
        return JsonResponse({"error": {"message": "unexpected error on reading the file!"}})
    if form.is_valid():
        f = request.FILES["upload"]
        fs = ck_storage()
        file_path = get_random_upload_path(str(settings.CKEDITOR_5_STORAGE_BASE_PATH), f.name)
        file_name = fs.save(file_path, f)
        url = fs.url(file_name)
        return JsonResponse({"url": url})
# @login_required
@login_required
def validate(request):
    if request.method == 'POST':
        form = UploadValidateFile(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['validate_file'] # Form key
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            try:
                assert "License" in reader.fieldnames
                assert "First Name" in reader.fieldnames
                assert "Last Name" in reader.fieldnames
                assert "Gender" in reader.fieldnames
                assert "Club" in reader.fieldnames
            except AssertionError:
                return HttpResponse("Missing required field. Please check your CSV file and try again.")
            # Download CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachement; filename="download.csv" '
            # Creating CSV 
            added_fields = ['WRH_USAC_LICENSE_ON_RECORD', 'WRH_VALID_USAC_LICENCES', 'WRH_USAC_CLUB_MATCH',
                            'WRH_USAC_CLUBS', 'WRH_CLUB_MATCH', 'WRH_BC_MEMBER',
                            'WRH_CLUB_MEMBERSHIPS', 'WRH_LOCAL_ASSOCIATION', 'BC_RACE_READY', 'BC_INDIVIDUAL_CUP_READY',
                            'BC_TEAM_CUP_READY']
            if "Email" in reader.fieldnames:
                added_fields.append("WRH_EMAIL_MATCH")
                email = True
            else:
                email = False
            verified = csv.DictWriter(response, fieldnames=reader.fieldnames+added_fields)
            verified.writeheader()
            for row in reader:
                row['WRH_USAC_LICENSE_ON_RECORD'] = usac_license_on_record(row['License'])
                row['WRH_VALID_USAC_LICENCES'] = valid_usac_licenses(row['License'])
                row['WRH_USAC_CLUB_MATCH'] = usac_club_match(row['License'], row['Club'])
                row['WRH_USAC_CLUBS'] = wrh_usac_clubs(row['License'])
                row['WRH_CLUB_MATCH'] = wrh_club_match(row['License'], row['Club'])
                row['WRH_BC_MEMBER'] = wrh_bc_member(row['License'])
                row['WRH_CLUB_MEMBERSHIPS'] = wrh_club_memberships(row['License'])
                row['WRH_LOCAL_ASSOCIATION'] = wrh_local_association(row['License'])
                row['BC_RACE_READY'] = bc_race_ready(row['License'])
                row['BC_INDIVIDUAL_CUP_READY'] = bc_individual_cup_ready(row['License'])
                row['BC_TEAM_CUP_READY'] = bc_team_cup_ready(row['License'], row['Club'])
                if email:
                    row['WRH_EMAIL_MATCH'] = wrh_email_match(row['Email'])
                verified.writerow(row)
        return response
    else:
        # GET method - render upload form
        form = UploadValidateFile()
    return render(request, 'validate.html', {'form': form})
