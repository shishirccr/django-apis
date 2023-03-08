from employee.database_objects.employee_mgr import EmployeeManager
from django.http import Http404
import math

class StatisticsManager:
    """
    The class performs all the statistical operations on the employee
    records
    """

    def __init__(self, request_type):
        self.request_type = request_type
        self.emp_object = EmployeeManager()

    # The method reads the request type and based on that calls the appropriate calculation helper method
    def get_stat(self):
        if self.request_type == 'all':
            min_salary, max_salary, mean_salary = self.__get_stat_for_all()
        elif self.request_type == 'contract':
            min_salary, max_salary, mean_salary = self.__get_stat_for_contract()
        elif self.request_type == 'department':
            return self.__get_stat_for_all_department()
        elif self.request_type == 'sub_department':
            return self.__get_stat_for_department_sub_dept_combination()
        else:
            raise Http404
        return {
            'ss': {
                'min': min_salary,
                'max': max_salary,
                'mean': math.floor(mean_salary * 100)/100.0
            }
        }

    def __get_stat_for_all_department(self):
        departments = self.__get_records_for_each_dept()
        result = {}
        for current_dept in departments:
            min_salary, max_salary, mean_salary = self.__calculate_stat(departments[current_dept])
            result[current_dept] = {
                'ss': {
                    'min': min_salary,
                    'max': max_salary,
                    'mean': math.floor(mean_salary * 100)/100.0
                }
            }
        return result

    # Helper method that returns object of Department: [Records]
    def __get_records_for_each_dept(self):
        all_employee = self.emp_object.get_all_employee()
        departments = {}
        for emp_record in all_employee:
            current_dept = emp_record.department
            if current_dept not in departments:
                departments[current_dept] = []
            departments[current_dept].append(emp_record)
        return departments

    def __get_stat_for_department_sub_dept_combination(self):
        departments = self.__get_records_for_each_sub_dept()
        result = {}
        for current_dept in departments:
            result[current_dept] = {}
            for current_sub_dept in departments[current_dept]:
                min_salary, max_salary, mean_salary = self.__calculate_stat(departments[current_dept][current_sub_dept])
                result[current_dept][current_sub_dept] = {
                    'ss': {
                        'min': min_salary,
                        'max': max_salary,
                        'mean': math.floor(mean_salary * 100)/100.0
                    }
                }
        return result

    # Helper method that returns nested object of Department: {Sub Departments}
    def __get_records_for_each_sub_dept(self):
        all_employee = self.emp_object.get_all_employee()
        departments = {}
        for emp_record in all_employee:
            current_dept = emp_record.department
            current_sub_dept = emp_record.sub_department
            if current_dept not in departments:
                departments[current_dept] = {}
            if current_sub_dept not in departments[current_dept]:
                departments[current_dept][current_sub_dept] = []
            departments[current_dept][current_sub_dept].append(emp_record)
        return departments

    def __get_stat_for_contract(self):
        return self.__calculate_stat(self.emp_object.get_employee_on_contract())

    def __get_stat_for_all(self):
        return self.__calculate_stat(self.emp_object.get_all_employee())

    # helper method to calculate min, max and mean for set of records
    def __calculate_stat(self, records):
        salaries = []
        salaries_total = 0
        for emp_record in records:
            salaries.append(emp_record.salary)
            salaries_total = salaries_total + emp_record.salary
        min_salary = min(salaries)
        max_salary = max(salaries)
        mean_salary = salaries_total/len(salaries)
        return min_salary, max_salary, mean_salary