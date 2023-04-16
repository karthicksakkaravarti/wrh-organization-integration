from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView

from .forms import JoinClubForm
from .models import Organization, OrganizationMember, Member
from ..usacycling.models import USACRiderLicense


def is_org_admin(org: Organization, user) -> bool:
    try:
        org_admin = OrganizationMember.objects.all().filter(
            Q(organization=org) & Q(member=user.member) & (Q(is_admin=True) | Q(is_master_admin=True))).exists()
        return org_admin or user.is_staff
    except:
        return None


def org_admins(org: Organization) -> list:
    return org.organizationmember_set.filter(Q(is_admin=True) | Q(is_master_admin=True))


def is_teammate(member1: Member, member2: Member) -> bool:
    """Org type must not be a Promoter"""
    org1 = OrganizationMember.objects.filter(member=member1).values_list('organization', flat=True)
    org2 = OrganizationMember.objects.filter(member=member2).values_list('organization', flat=True)
    return Organization.objects.filter(Q(id__in=org1) & Q(id__in=org2) & ~Q(type='Promoter')).exists()


def is_team_capatain(member: Member, captain: Member) -> bool:
    """Org type must not be a Promoter
    Org type must not be a Promoter"""
    org1 = OrganizationMember.objects.filter(member=member).values_list('organization', flat=True)
    org2 = OrganizationMember.objects.filter(Q(member=captain) and ~Q(organization__type='Promoter') and (
            Q(is_admin=True) | Q(is_master_admin=True))).values_list('organization', flat=True)
    return set(org1).intersection(set(org2))


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


@login_required
def join_club(request, pk=None):
    if request.method == 'POST':
        form = JoinClubForm(request.POST)
        if form.is_valid():
            # form.save()
            print(form)
            messages.success(request, 'TEST: You have successfully joined the club.')
        else:
            messages.error(request, 'Please correct the error below.')
    elif request.method == 'GET':
        if id:
            club = get_object_or_404(Organization, id=pk)
            context = {'Club': club}
            print(club.waiver_text)
            context['form'] = JoinClubForm(initial={'organization': club, 'member': request.user.member})
            print(context)
            return render(request, 'BCforms/JoinClub.html', context)


@login_required
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


@login_required
def edit_club(request, pk=None):
    """ This is for creating or editing a club """
    if request.method == 'POST':
        form = EditClub(request.POST)
        if form.is_valid():
            # form.save()
            print(form)
            messages.success(request, 'TEST: You have successfully joined the club.')
        else:
            messages.error(request, 'Please correct the error below.')
    elif request.method == 'GET':
        if pk:
            try:
                club = get_object_or_404(Organization, id=pk)
                context = {'Club': club,
                           'form': EditClub(initial={'organization': club, 'member': request.user.member})}
                context['ClubAdmin'] = is_org_admin(club, request.user)

            except AttributeError:
                context = None
            return render(request, 'BCforms/EditClub.html', context)


class ClubReport(LoginRequiredMixin, DetailView):
    template_name = 'BC/ClubReport.html'
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(ClubReport, self).get_context_data(**kwargs)
        context['ClubAdmin'] = is_org_admin(context['object'], self.request.user)
        if context['ClubAdmin']:
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
            return context
        else:
            return None
