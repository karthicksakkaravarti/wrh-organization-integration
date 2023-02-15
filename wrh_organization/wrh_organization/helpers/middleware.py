import re
import sys
import traceback
import uuid
import datetime
import json
import rollbar
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.db import connection
from threading import local
from rollbar.contrib.django.middleware import RollbarNotifierMiddleware
from wrh_organization import __version__ as VERSION

_thread_locals = local()

settings.ROLLBAR['code_version'] = VERSION


def get_current_request():
    """ returns the request object for this thread """
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """ returns the current user, if exist, otherwise returns None """
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


class ThreadLocalMiddleware:
    """ Simple middleware that adds the request object in thread local storage."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        ex = None
        response = None
        try:
            response = self.get_response(request)
        except Exception as e:
            ex = e
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        if ex:
            raise ex
        return response


class DisableCSRFMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'CSRF_DISABLED', False):
            setattr(request, '_dont_enforce_csrf_checks', True)

        response = self.get_response(request)
        return response


class InjectUiVersionInHeadersMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def _get_ui_version(self):
        ui_packages_path = settings.BASE_DIR / 'FRONTEND' / 'wrh_organization_ui' / 'package.json'
        if not ui_packages_path.exists():
            return
        version = None
        try:
            with open(ui_packages_path) as f:
                data = json.load(f)
            version = data.get('version')
        except Exception:
            traceback.print_exc()
        return version

    def __call__(self, request):
        response = self.get_response(request)
        ui_version = self._get_ui_version()
        if ui_version:
            response['X-UI-Version'] = ui_version
        else:
            print('Cannot discover UI version!')
        return response


class InjectBackendVersionInHeadersMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Backend-Version'] = VERSION
        return response


class SqlQueryLogging:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        from sys import stdout
        if stdout.isatty() and settings.DEBUG:
            for query in connection.queries:
                print("\033[1;31m[%s]\033[0m \033[1m%s\033[0m" % (query['time'], " ".join(query['sql'].split())))
        return response


class RequestTimeLoggingMiddleware(object):
    """Middleware class logging request time to stderr.

    This class can be used to measure time of request processing
    within Django.  It can be also used to log time spent in
    middleware and in view itself, by putting middleware multiple
    times in INSTALLED_MIDDLEWARE.

    Static method `log_message' may be used independently of the
    middleware itself, outside of it, and even when middleware is not
    listed in INSTALLED_MIDDLEWARE.
    """

    @staticmethod
    def log_message(request, tag, message=''):
        """Log timing message to stderr.

        Logs message about `request' with a `tag' (a string, 10
        characters or less if possible), timing info and optional
        `message'.

        Log format is "timestamp tag uuid count path +delta message"
        - timestamp is microsecond timestamp of message
        - tag is the `tag' parameter
        - uuid is the UUID identifying request
        - count is number of logged message for this request
        - path is request.path
        - delta is timedelta between first logged message
          for this request and current message
        - message is the `message' parameter.
        """

        dt = datetime.datetime.utcnow()
        if not hasattr(request, '_logging_uuid'):
            request._logging_uuid = uuid.uuid1()
            request._logging_start_dt = dt
            request._logging_pass = 0

        request._logging_pass += 1
        print(
            u'%s %-10s %s %2d %s +%s %s' % (
                dt.isoformat(),
                tag,
                request._logging_uuid,
                request._logging_pass,
                request.path,
                dt - request._logging_start_dt,
                message,
            ), file=sys.stderr)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            self.log_message(request, 'request ')
        response = self.get_response(request)
        if settings.DEBUG:
            s = getattr(response, 'status_code', 0)
            r = str(s)
            if s in (300, 301, 302, 307):
                r += ' => %s' % response.get('Location', '?')
            elif getattr(response, 'content', None):
                r += ' (%db)' % len(response.content)
            self.log_message(request, 'response', r)
        return response


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):
    def get_payload_data(self, request, exc):
        payload_data = {}
        if request.user.is_authenticated:
            payload_data['person'] = {
                'id': request.user.id, 'username': request.user.username, 'email': request.user.email
            }
        return payload_data


class RequestLoggingRollbarNotifierMiddleware(object):
    IGNORE_STATUSES = ['^[2|3][0-9]{2}$']

    def __init__(self, get_response=None):
        self.get_response = get_response
        if getattr(settings, 'ROLLBAR_REQUEST_LOGGING_DISABLED', False):
            raise MiddlewareNotUsed

    def __call__(self, request):
        response = self.get_response(request)
        if self._check_logging_ignore_statuses(response.status_code):
            return response

        msg = f'[Request]: {request.method} {request.path_info}'
        payload_data = self.get_payload_data(request, response)
        extra_data = self.get_extra_data(request, response)
        rollbar.report_message(message=msg, level='info', request=request, payload_data=payload_data,
                               extra_data=extra_data)
        return response

    def _check_logging_ignore_statuses(self, status):
        IGNORE_STATUSES = getattr(settings, 'ROLLBAR_REQUEST_LOGGING_IGNORE_STATUSES', None)
        if IGNORE_STATUSES is None:
            IGNORE_STATUSES = self.IGNORE_STATUSES
        status = str(status)
        for p in IGNORE_STATUSES:
            p = str(p)
            if (not p.startswith('^')) and (p == status):
                return True
            elif p.startswith('^') and re.match(p, status):
                return True
        return False

    def get_extra_data(self, request, response):
        return

    def get_payload_data(self, request, response):
        payload_data = {
            'django_request_logging': True
        }
        payload_data['response'] = {
            f: getattr(response, f, None) for f in ('data', 'status_code', 'status_text', 'cookies', 'exception')
        }
        if request.user.is_authenticated:
            payload_data['person'] = {
                'id': request.user.id, 'username': request.user.username, 'email': request.user.email
            }
        return payload_data
