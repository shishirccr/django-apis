from rest_framework import serializers
from .models import Employee
from json import JSONEncoder
import datetime
import json

class GenericEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class DateTimeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        return o.__dict__

class EmployeeSerializer(serializers.ModelSerializer):  # create class to serializer model

    class Meta:
        model = Employee
        fields = ('name', 'currency', 'salary', 'department', 'sub_department', 'on_contract')

def serialize_response_data(response):
    json_data = json.dumps(response, indent=4, cls=GenericEncoder)
    return json_data