from django_filters.rest_framework import DjangoFilterBackend
from rest_access_policy import AccessViewSetMixin
from rest_framework import mixins, filters, status, viewsets
from rest_framework.decorators import action, schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.viewsets import GenericViewSet
from apps.setup import models
from apps.setup.rest_api import serializers
from apps.setup.rest_api import access_policy
from django.apps import apps


class FormsModelViewset(AccessViewSetMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        GenericViewSet):
    pagination_class = None
    access_policy = access_policy.FormsPolicy
    permission_classes = []
    serializer_class = serializers.FormsModelSerializers
    queryset = models.FormsModel.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name']

    @action(detail=False, methods=['GET'])
    def get_form(self, request, version):
        """
        Get form layout by form name
        :param request:
        :return:
        """
        serializer_context = {'request': request.query_params}
        form = models.FormsModel.objects.get(name=request.query_params.get("form_name"))
        ser = serializers.FormsModelSerializers(form)
        print(ser.data)
        formser = serializers.LayoutSeralizers(data=ser.data['layout']['data'], many=True, context=serializer_context)
        formser.is_valid(raise_exception=True)
        return Response(formser.data)

    @action(detail=False, methods=['GET'])
    def get_model_filter(self, request):
        """
        Get model filter by form name
        :param request:
        :return:
        """
        serializer_context = {'request': request.query_params}
        model_list = []
        for model in apps.get_models():
            model_list.append(
                {
                    "model_name": model.__name__,
                    "fields": [field.name for field in model._meta.fields]
                }
            )
        return Response(model_list)


