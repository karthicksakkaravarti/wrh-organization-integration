import json
from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from apps.setup.models import  FormsModel
from apps.setup import models


def get_value(request, value):
    return "Value"


class ValueField(serializers.Field):
    def get_attribute(self, instance):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return instance

    def to_representation(self, value):
        try:
            request = self.context.get('request', {})
            # If Project Id Found
            return []
        except Exception as e:
            print("Exception", str(e))
        return ""

    def to_internal_value(self, data):
        return data


class ValueList(serializers.Field):
    def get_attribute(self, instance):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return instance
    def to_representation(self, value):
        # All Custom Logic
        request = self.context.get('request', {})
        # Assigning Back values
        for query, query_value in request.items():
            if value.get('dbfield') == query:
                value['value'] = query_value
        return ""
    def to_internal_value(self, data):
        return data


class LayoutSeralizers(serializers.Serializer):
    name = serializers.CharField()
    fieldtype = serializers.CharField()
    sm = serializers.CharField()
    # valuelist = serializers.SerializerMethodField(read_only=True, required=False)
    valuelist = ValueList()
    value = ValueField()
    dbfield = serializers.CharField(allow_blank=True)
    customtable = serializers.BooleanField(required=False)
    customfieldname = serializers.CharField(required=False)
    required = serializers.BooleanField(required=False)
    max_length = serializers.IntegerField(required=False)
    other_rules = serializers.ListField(required=False)
    itemtext = serializers.CharField(required=False)
    itemvalue = serializers.CharField(required=False)
    prependicon = serializers.CharField(required=False)
    maxdate_field = serializers.CharField(required=False)
    mindate_field = serializers.CharField(required=False)
    menu = serializers.BooleanField(required=False)
    clearable = serializers.BooleanField(required=False)
    conditioncheck = serializers.BooleanField(required=False)
    conditionfield = serializers.CharField(required=False)
    conditionfield1 = serializers.CharField(required=False)
    conditionvalue = serializers.CharField(required=False)
    conditionvalue1 = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    rows = serializers.IntegerField(required=False)
    prefix = serializers.CharField(required=False)
    appendicon = serializers.CharField(required=False)
    readonly = serializers.BooleanField(required=False)
    prependinnericon = serializers.CharField(required=False)
    rowheight = serializers.IntegerField(required=False)
    error_message = serializers.CharField(required=False, default=None, allow_null=True, allow_blank=True)
    outlined = serializers.BooleanField(required=False)
    dbtable = serializers.CharField(required=False)
    hint = serializers.CharField(required=False)


class FormsSerializers(serializers.Serializer):
    layout = LayoutSeralizers(many=True)


class FormsModelSerializers(QueryFieldsMixin, serializers.ModelSerializer):

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # try :
        #     if response and response['layout'] :
        #         layoutdata = response['layout'].replace("\'", "\"")
        #         response['layout'] = json.loads(layoutdata)['data']
        # except Exception as e:
        #     print("Exception", str(e))

        return response

    class Meta:
        model = FormsModel
        fields = '__all__'


class CriteriaSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Criteria
        fields = "__all__"


class CustomViewSerializers(serializers.ModelSerializer):
    criteria = CriteriaSerializers()

    class Meta:
        model = models.CustomView
        fields = "__all__"

