import csv
import traceback
from datetime import date

from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import storage as ck_storage
from dynamic_preferences.registries import global_preferences_registry

from apps.cycling_org.models import User
from jwt.utils import force_bytes
from wrh_organization.helpers.utils import get_random_upload_path
from .forms import UploadValidateFile, EventEditForm, SignInForm, SignUpForm, CustomPasswordResetForm
from .models import Organization, OrganizationMember, Event, Member, RaceSeries
from .rest_api.views import _send_activation_email
from .validators import usac_license_on_record, valid_usac_licenses, wrh_club_match, wrh_bc_member, \
    wrh_club_memberships, wrh_email_match, wrh_local_association, wrh_usac_clubs, usac_club_match, bc_race_ready, \
    bc_individual_cup_ready, bc_team_cup_ready
from .views_clubs import is_teammate, is_team_capatain
from .views_results import races, race_results
from ..usacycling.models import USACRiderLicense
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from wrh_organization.helpers.utils import account_activation_token, send_sms, IsAdminOrganizationOrReadOnlyPermission, account_password_reset_token, to_dict, IsMemberPermission, random_id, \
    APICodeException, check_turnstile_request
global_pref = global_preferences_registry.manager()


def is_org_admin(org: Organization, user) -> bool:
    try:
        return user.is_staff or org.organizationmember_set.filter(
            Q(member=user) & (Q(is_admin=True) | Q(is_master_admin=True))).exists()
    except:
        return None
def user_profile_permissions(profile: Member, user: User):
    """What is the user allowed to see?
    returns a list:
    - public: Public
    - user: logged in user
    - teammate: Teammate: (in the same club)
    - teamcaptain: Club/org Admin: Admin of a club the user is a member of
    - bcadmin: BC admin: Admin of the BC
    - iam: The user is the profile owner
    """
    permissions = ['public']
    if user.is_authenticated:
        permissions.append('user')
    if user.is_staff:
        permissions.append('bcadmin')
    if user == profile.user:
        permissions.append('iam')
    if is_teammate(profile, user.member):
        permissions.append('teammate')
    if is_team_capatain(profile, user.member):
        permissions.append('team_captain')
    if user.member == profile:
        permissions.append('iam')
    return permissions


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


class Index(TemplateView):
    template_name = 'BC/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Banner'] = global_pref['site_ui__banner_image']
        context['InfoBoard'] = global_pref['site_ui__home_information_board']
        context['Featured'] = Event.objects.all().order_by('start_date').filter(
            Q(featured_event=True) & Q(end_date__gte=date.today()))
        # print(context['Featured'])
        # print(context['Banner'].url)
        return context


# @login_required
@login_required
def validate(request):
    if request.method == 'POST':
        form = UploadValidateFile(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['validate_file']  # Form key
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            try:
                assert "License" in reader.fieldnames
                assert "First Name" in reader.fieldnames
                assert "Last Name" in reader.fieldnames
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
            verified = csv.DictWriter(response, fieldnames=reader.fieldnames + added_fields)
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
    return render(request, 'BCforms/validate.html', {'form': form})


class BCsignin(TemplateView):
    template_name = 'BC/BCsignin.html'
    pass


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


def event_edit(request, id=None):
    if request.method == 'POST':
        form = EventEditForm(request.POST)
        if form.is_valid():
            form.save()
            print(form)
        else:
            messages.error(request, 'Please correct the error below.')
    elif request.method == 'GET':
        if id:
            event = get_object_or_404(Event, id=id)
            context = {'form': EventEditForm(instance=event), 'id': id}
            print(context)
            return render(request, 'BCforms/EventForm.html', context)
    form = EventEditForm()
    return render(request, 'BCforms/EventForm.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class Clubs(TemplateView):
    template_name = 'BC/Clubs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Org'] = Organization.objects.all()
        # TODO: make this faster
        club_counts = USACRiderLicense.objects.values('data__club').annotate(count=Count('id'))
        context['USACclub'] = {row['data__club']: row['count'] for row in club_counts if row['data__club']}
        # context['USACclub'] = dict()
        # for u in USACRiderLicense.objects.all():
        #     if u.data['club']:
        #         if u.data['club'] in context['USACclub'].keys():
        #             context['USACclub'][u.data['club']] += 1
        #         else:
        #             context['USACclub'][u.data['club']] = 1
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['Org'] = Organization.objects.filter(name__icontains=request.POST.get('org'))
        return self.render_to_response(context)


class ClubDetails(DetailView):
    template_name = 'BC/ClubDetails.html'
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(ClubDetails, self).get_context_data(**kwargs)
        usacriders = USACRiderLicense.objects.filter(data__club=context['object'].name)
        context['USACrider'] = usacriders
        context['USACcount'] = usacriders.count()
        context['ClubAdmin'] = is_org_admin(context['object'], self.request.user)
        return context


class ClubReport(DetailView):
    template_name = 'BC/ClubReport.html'
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(ClubReport, self).get_context_data(**kwargs)
        member_usac = context['object'].members.all().order_by('usac_license_number').filter(
            Q(usac_license_number_verified=True) | Q(usac_license_number__isnull=False)).values_list(
            'usac_license_number', flat=True)
        usacriders = USACRiderLicense.objects.filter(data__club=context['object'].name)
        matching = set(member_usac).intersection(set(usacriders.values_list('license_number', flat=True)))
        context['member_no_match'] = member_usac.exclude(usac_license_number__in=matching)
        context['usac_no_match'] = usacriders.exclude(license_number__in=matching)
        context['member_no_license'] = context['object'].members.all().order_by('usac_license_number').filter(
            Q(usac_license_number_verified=False) | Q(usac_license_number__isnull=True))
        context['member_not_verified'] = context['object'].members.all().order_by('usac_license_number').filter(
            Q(usac_license_number_verified=False) & Q(usac_license_number__isnull=False))
        context['USACrider'] = usacriders
        context['USACcount'] = usacriders.count()
        context['ClubAdmins'] = OrganizationMember.objects.all().filter(
            Q(organization=context['object']) & (Q(is_admin=True) | Q(is_master_admin=True)))
        # print(context['ClubAdmins'])
        # TODO: this is not the right way to do this.
        # context['ClubAdminsId'] = OrganizationMember.objects.filter(
        #     Q(organization=context['object']) & (Q(is_admin=True) | Q(is_master_admin=True))).values_list('member', flat=True)
        context['ClubAdmin'] = is_org_admin(context['object'], self.request.user)
        return context


class RaceSeriesList(TemplateView):
    template_name = 'BC/RaceSeries.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RaceSeries'] = RaceSeries.objects.all().order_by('name')
        return context


class ProfileDetail(DetailView):
    template_name = 'BC/ProfileDetail.html'
    model = Member

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['ViewPermissions'] = user_profile_permissions(context['object'], self.request.user)
        if context['object'].usac_license_number and context['object'].usac_license_number_verified:
            lic = context['object'].usac_license_number  # Get and use it to query USACRider
            context['USACData'] = USACRiderLicense.objects.filter(license_number=lic)
        else:
            context['USACData'] = None
        return context


def member_joined_org_email(user, org):
    subject = 'New Member Notification'
    message = render_to_string('cycling_org/email/member_joined_org_email.html', {
        'user': user,
        'org': org,
        'host': settings.HOSTNAME
    })
    # TODO: Fix the to address, send to all org admins plus developer@bicyclecolorado.org
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ["developer@bicyclecolorado.org"], html_message=message,
              fail_silently=False)


class SignInView(TemplateView):
    template_name = 'BC/SignIn.html'

    @method_decorator(user_passes_test(lambda user: not user.is_authenticated, login_url='index'))
    def dispatch(self, *args, **kwargs):
        return super(SignInView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return self.render_to_response({'form': form})

class SignupView(TemplateView):
    template_name = 'BC/SignUp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SignUpForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        if global_pref.get('user_account__disabled_signup'):
            raise PermissionDenied({'detail': 'Signup is disabled by admin'})
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create the user account
            # Create a new user instance and save it
            waiver = request.POST.get('waiver', False) == 'on'
            terms_of_service = request.POST.get('terms_of_service', False) == 'on'
            opt_out_email = request.POST.get('opt_out_email', False) == 'on'

            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # Assuming 'email' is the field name for email
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],  # Assuming 'password' is the field name for password
                first_name=form.cleaned_data['first_name'],  # Assuming 'first_name' is the field name for first name
                last_name=form.cleaned_data['last_name'],  # Assuming 'last_name' is the field name for last name
                gender=form.cleaned_data['gender'],
                birth_date=form.cleaned_data['date_of_birth'],
            )
            user.more_data = {"member_data": {"country": "US", "usac_license_number": str(form.cleaned_data['usac_number'])}}
            user.opt_in_email = opt_out_email
            user.user_agreement_waiver = waiver
            user.terms_of_service = terms_of_service
            user.save()

            # Sending Activation mal
            _send_activation_email(user, request)

            # Redirect to a success page or the user's dashboard
            return redirect(reverse('sign-in'))
        return self.render_to_response(self.get_context_data())


class SignOutView(TemplateView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


class BCPasswordResetView(PasswordResetView):
    template_name = 'BC/PasswordReset.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.POST.get('email')).first()
        if not user:
            return HttpResponse({'error': 'A User with this email does not exists!'})
        if not user.is_active:
            return HttpResponse({'error': 'A User with this email is inactive.'})

        subject = 'Reset Your Password'
        message = render_to_string('cycling_org/email/user_recover_password.html', {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_password_reset_token.make_token(user),
            'request': self.request
        })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message,
                  fail_silently=False)
        return redirect(reverse('password_reset_done'))

class BCPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'BC/PasswordResetDone.html'