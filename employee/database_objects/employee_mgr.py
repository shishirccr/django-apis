from employee.models import Employee
from django.http import Http404
from employee.serializers import EmployeeSerializer


class EmployeeManager:
    """
    The class interacts with the database and manages all Employee operations
    """
    model = Employee

    # the method returns an employee based on the name. The search is case insensitive
    def get_employee_by_name(self, emp_name):
        try:
            return EmployeeManager.model.objects.filter(name__iexact=emp_name)
        # Return 404 exception if the employee is not found. Will take care of validations
        # for get and delete request
        except Employee.DoesNotExist:
            raise Http404

    # The methos return all employees on contract
    def get_employee_on_contract(self):
        try:
            return EmployeeManager.model.objects.filter(on_contract="true")
        except Employee.DoesNotExist:
            raise Http404

    # The method deletes an employee based on the name. The search is case insensitive
    def delete_employee_by_name(self, emp_name):
        employee = self.get_employee_by_name(emp_name)
        employee.delete()

    # The method returns all the employee in the database
    def get_all_employee(self):
        return EmployeeManager.model.objects.all().iterator()

    # The method saves an employee record
    def save_employee_record(self, data):
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return True, 'record saved'
        else:
            return False, serializer.errors