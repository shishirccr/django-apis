from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import logging
import traceback
from django.http.response import JsonResponse
import json
from employee.database_objects.employee_mgr import EmployeeManager
from .serializers import serialize_response_data
from employee.statistics.stat_calculator import StatisticsManager
from rest_framework.exceptions import ValidationError, ParseError
from employee.validations.validator import ValidationManager


logger = logging.getLogger(__name__)

class EmployeeView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    # Get method for all the SS operations
    def get_statistic_info(self, request):
        q_param = request.query_params

        if 'type' not in q_param:
            logger.error('Missing required parameters')
            raise ValidationError('Missing required parameters')

        statistic_request_type = q_param.get('type')

        stat_mgr = StatisticsManager(statistic_request_type)
        response = stat_mgr.get_stat()
        return JsonResponse(json.loads(serialize_response_data(response)))

    
    # Delete method to delete an employee
    def delete_employee(self, request, emp_name):
        try:
            emp_object = EmployeeManager()
            emp_object.delete_employee_by_name(emp_name)
        except Exception as e:
            logger.error(traceback.format_exc())
            raise ParseError('Unable to delete the employer record')
        response = {
            'status': 'true',
            'message': 'Record for name ' + emp_name + ' deleted'
        }
        return JsonResponse(json.loads(serialize_response_data(response)))


    # POST method to create a new employee
    def add_new_record(self, request):
        validator = ValidationManager()
        validator.validate_create_request(request.data)
        try:
            emp_object = EmployeeManager()
            status, msg_obj = emp_object.save_employee_record(request.data)
            if not status:
                logger.error("Unable to save the employer record")
                logger.error(msg_obj)
                return JsonResponse(status=500,
                                    data=json.loads(serialize_response_data(
                                        {'status': 'false', 'message': msg_obj.get('name')[0]})))
        except Exception as e:
            logger.error(traceback.format_exc())
            raise ParseError('Unable to save the employer record')
        response = {
            'status': 'true',
            'message': 'Record created'
        }
        return JsonResponse(json.loads(serialize_response_data(response)))

