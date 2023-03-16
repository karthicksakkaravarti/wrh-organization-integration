from django_ckeditor_5.widgets import CKEditor5Widget
from dynamic_preferences.preferences import Section
from dynamic_preferences import types
from dynamic_preferences.registries import global_preferences_registry

from wrh_organization.helpers.utils import PatchedGlobalPrefFileSerializer, JSONPreference

site_ui = Section('site_ui')
rollbar_client = Section('rollbar_client')
user_account = Section('user_account')
core_backend = Section('core_backend')

types.FilePreference.serializer_class = PatchedGlobalPrefFileSerializer


@global_preferences_registry.register
class UserAccountDisabledSignup(types.BooleanPreference):
    field_kwargs = {
        'required': False,
        'help_text': 'user account disabled signup',
    }
    section = user_account
    name = 'disabled_signup'
    verbose_name = 'Disabled Signup?'
    default = False


@global_preferences_registry.register
class CoreBackendDefaultOrgId(types.IntegerPreference):
    field_kwargs = {
        'required': False,
        'help_text': 'default organization id',
    }
    section = core_backend
    name = 'default_org_id'
    verbose_name = 'Default Org id'
    default = 1


@global_preferences_registry.register
class CoreBackendDisabledCreateOrg(types.BooleanPreference):
    field_kwargs = {
        'required': False,
        'help_text': 'Disabled to create organization by anybody',
    }
    section = core_backend
    name = 'disabled_create_org'
    verbose_name = 'Disabled create org?'
    default = False


@global_preferences_registry.register
class RollbarClientAccessToken(types.StringPreference):
    field_kwargs = {
        'required': False,
        'help_text': 'rollbar post client token',
    }
    section = rollbar_client
    name = 'access_token'
    verbose_name = 'Client Access Token'
    default = ''


@global_preferences_registry.register
class RollbarClientEnvironment(types.ChoicePreference):
    choices = [
        ('production', 'Production'),
        ('development', 'Development'),
    ]
    field_kwargs = {
        'required': False,
        'help_text': 'rollbar client environment',
    }
    section = rollbar_client
    name = 'environment'
    verbose_name = 'Client Environment'
    default = 'development'


@global_preferences_registry.register
class RollbarClientEnabled(types.BooleanPreference):
    field_kwargs = {
        'required': False,
        'help_text': 'rollbar client enabled?',
    }
    section = rollbar_client
    name = 'enabled'
    verbose_name = 'Client Enabled?'
    default = True


@global_preferences_registry.register
class SiteUiTermsOfService(types.LongStringPreference):
    field_kwargs = {
        'required': False,
        'help_text': 'terms of service content',
        'widget': CKEditor5Widget()
    }
    section = site_ui
    name = 'terms_of_service'
    verbose_name = 'Terms of Service'
    default = ''


@global_preferences_registry.register
class SiteUiUserAgreementWaver(types.LongStringPreference):
    field_kwargs = {
        'required': False,
        'help_text': 'user agreement and waver ',
        'widget': CKEditor5Widget()
    }
    section = site_ui
    name = 'user_agreement_waver'
    verbose_name = 'User Agreement Waver'
    default = ''


@global_preferences_registry.register
class SiteUiBannerImage(types.FilePreference):
    field_kwargs = {
        'required': False,
        'help_text': 'banner image of home site',
    }
    section = site_ui
    name = 'banner_image'
    verbose_name = 'Banner Image'


@global_preferences_registry.register
class SiteUiDefaultEventBannerImage(types.FilePreference):
    field_kwargs = {
        'required': False,
        'help_text': 'default banner image of event page',
    }
    section = site_ui
    name = 'default_event_banner_image'
    verbose_name = 'Default Event Banner Image'


@global_preferences_registry.register
class SiteUiSignupPageTitle(types.StringPreference):
    field_kwargs = {
        'required': False,
        'help_text': 'signup page title',
    }
    section = site_ui
    name = 'signup_page_title'
    verbose_name = 'Signup Page title'
    default = 'Sign up on Bicycle Colorado'


@global_preferences_registry.register
class SiteUiSignupPageCaption(types.StringPreference):
    field_kwargs = {
        'required': False,
        'help_text': 'signup page caption',
    }
    section = site_ui
    name = 'signup_page_caption'
    verbose_name = 'Signup Page caption'
    default = 'Create your account and enjoy!'


@global_preferences_registry.register
class SiteUiHomeInfomationBoard(types.LongStringPreference):
    field_kwargs = {
        'required': False,
        'help_text': 'home information board',
        'widget': CKEditor5Widget(config_name='awesome')
    }
    section = site_ui
    name = 'home_information_board'
    verbose_name = 'Home Information Board'
    default = ''


@global_preferences_registry.register
class RaceTemplate(JSONPreference):
    section = core_backend
    name = 'global_race_template'
    verbose_name = 'Global Race Template'
    default = {"Template 1": ["Race 1"]}


# 138  Global setting to edit event tags
@global_preferences_registry.register
class CoreBackendEventTags(JSONPreference):
    section = core_backend
    name = 'event_tags'
    verbose_name = 'Event Tags on ORG event page'
    default = [
        'bike tour', 'bmx freestyle', 'bmx race', 'bmx racing', 'camp', 'chariot race', 'clinic', 'club membership',
        'criterium', 'cross country', 'cx race', 'cycling camp', 'cyclocross', 'cyclocross racing', 'derny race',
        'downhill', 'dual slalom', 'elimination', 'enduro', 'fat bike', 'freestyle', 'fun rides', 'gran fondo',
        'gravel', 'gravel grinder', 'handicap', 'hill climb', 'international omnium', 'italian pursuit', 'keirin',
        'longest lap', 'madison', 'match sprint', 'miss n out', 'motorpaced scratch', 'mountain bike racing', 'mtb',
        'mtb enduro', 'multisport', 'nebra', 'off road', 'omnium', 'other', 'point a lap', 'points race', 'pursuit',
        'recreational', 'road', 'road race', 'road race or circuit race', 'road racing', 'scratch race', 'series',
        'snowball', 'special event', 'stage race', 'team pursuit', 'team sprint', 'tempo', 'time trial', 'track',
        'track racing', 'training rides', 'training series', 'trials', 'unknown distance', 'virtual',
        'virtual challenge', 'virtual race', 'virtual road race', 'win n out'
    ]


@global_preferences_registry.register
class SiteUiDefaultEventLogo(types.FilePreference):
    section = site_ui
    name = 'default_event_logo'
    verbose_name = 'Default Event Logo'
    default = ''
