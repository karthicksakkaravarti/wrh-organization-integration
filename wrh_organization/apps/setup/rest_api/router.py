from rest_framework.routers import DefaultRouter
from apps.setup.rest_api import viewset
setup_router = DefaultRouter()

setup_router.register('forms', viewset.FormsModelViewset)  # App Forms
