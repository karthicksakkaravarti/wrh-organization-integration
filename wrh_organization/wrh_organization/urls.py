"""wrh_photos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, re_path, path
from django.views.static import serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.cycling_org.ical_feed import WRHEventsIcalFeed
from apps.cycling_org.views import ckeditor_upload_file, validate, Events, EventDetails, \
    ProfileDetail, BCsignin, Index, SignInView, event_edit, SignInView, event_edit, SignupView, SignOutView, BCPasswordResetView, BCPasswordResetDoneView
from apps.cycling_org.views_clubs import Clubs, ClubDetails, ClubReport, join_club, edit_club
from apps.cycling_org.views_results import RaceResults, RaceSeriesList

# login url https://events.bicyclecolorado.org/static/vue/index.html#/auth?next=%2Fhome
# logout url https://events.bicyclecolorado.org/static/vue/index.html#/logout
#  https://events.bicyclecolorado.org/static/vue/index.html#/dashboard/member-profile


VERSION_PARAM = settings.REST_FRAMEWORK.get('VERSION_PARAM', 'version')
DEFAULT_VERSION = settings.REST_FRAMEWORK.get('DEFAULT_VERSION', 'v1')
API_ENDPOINT = 'api/(?P<{}>v\d+)'.format(VERSION_PARAM)

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    # re_path(r'^$', RedirectView.as_view(url=settings.VUE_STATIC_INDEX), name='index'),
    re_path(r'^{}/account/'.format(API_ENDPOINT), include('apps.wrh_account.urls', namespace='account_rest_api')),
    re_path(r'^{}/cycling_org/'.format(API_ENDPOINT),
            include('apps.cycling_org.urls', namespace='cycling_org_rest_api')),
    re_path(r'^{}/usacycling/'.format(API_ENDPOINT), include('apps.usacycling.urls', namespace='usacycling_rest_api')),
    re_path(r'^admin/', admin.site.urls),
    re_path('^ckeditor5/image_upload/', ckeditor_upload_file, name="ck_editor_5_upload_file"),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^token/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^accounts/constantcontact/', include('apps.constant_contact.urls')),  # CC integration
    re_path(r'^{}/constantcontact/'.format(API_ENDPOINT),
            include('apps.constant_contact.rest_api.urls', namespace='constant_contact_rest_api')),
    re_path(r'^feed/calendar/ics', WRHEventsIcalFeed(), name='ics'),
    # Django View - BC
    path('validator/', validate, name='validate'),
    path('bcsignin/', BCsignin.as_view(), name='bcsignin-dv'),
    path('Events/', Events.as_view(), name='events-dv'),
    path('Event/<int:pk>/', EventDetails.as_view(), name='events-details-dv'),
    path('Event/Form/', event_edit, name='event_edit-dv'),
    path('Event/Form/<int:id>/', event_edit, name='event_edit_id-dv'),
    path('Clubs/', Clubs.as_view(), name='clubs-dv'),
    path('Club/<int:pk>/', ClubDetails.as_view(), name='club-details-dv'),
    path('Club/Join/<int:pk>/', join_club, name='join-club-dv'),
    path('Club/Edit/', edit_club, name='edit-club-dv'),
    path('Club/Edit/<int:pk>/', edit_club, name='edit-club-dv'),
    path('Club/Report/<int:pk>/', ClubReport.as_view(), name='club-report-dv'),
    path('RaceResults/', RaceResults.as_view(), name='raceresults-dv'),
    path('RaceSeries/', RaceSeriesList.as_view(), name='RaceSeries'),
    path('ProfileDetail/<int:pk>/', ProfileDetail.as_view(), name='profile-detail-dv'),
    # BC - Authentication
    path('signin/', SignInView.as_view(), name='sign-in'),
    path('signup/', SignupView.as_view(), name='sign-up'),
    path('signout/', SignOutView.as_view(), name='sign-out'),
    path('password_reset/', BCPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', BCPasswordResetDoneView.as_view(), name='password_reset_done'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
