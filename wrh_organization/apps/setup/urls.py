from apps.setup.rest_api import router
app_name = 'Setup'

urlpatterns = [

]
# Api
urlpatterns += router.setup_router.urls
