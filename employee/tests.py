from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Employee


class BasicTest(APITestCase):

    def __set_up(self):
        User.objects.create_user(
            "ckent", "ckent@email.com", "password")
        user = User.objects.get(username='ckent')
        self.client.force_authenticate(user=user)
        Employee.objects.create(name= "Anurag", salary= "90000",
                                currency = "USD",
                                department= "Banking",
                                on_contract= "true",
                                sub_department= "Loan")
        Employee.objects.create(name= "Abhishek", salary= "145000",
                                currency = "USD",
                                department= "Engineering",
                                sub_department= "Platform")
        Employee.objects.create(name= "Himani", salary= "240000",
                                currency = "USD",
                                department= "Engineering",
                                sub_department= "Platform")
        Employee.objects.create(name= "Yatendra", salary= "30",
                                currency = "USD",
                                department= "Operations",
                                sub_department= "CustomerOnboarding")

    def test_get_all_stat(self):
        self.__set_up()
        result = {
            "ss": {
                "min": 30,
                "max": 240000,
                "mean": 118757.5
            }
        }
        response = self.client.get(f'/api/v1/employee/?type=all')
        self.assertEqual(response.json(), result)

    def test_create_new_record(self):
        self.__set_up()
        response = self.client.post(f'/api/v1/employee/create', {"name": "Vivek",
                                                         "salary": "145000",
                                                         "currency": "USD",
                                                         "department": "Engineering",
                                                         "sub_department": "Platform"
                                                         })
        self.assertEqual(response.json()['status'], "true")
        self.assertEqual(response.json()['message'], "Record created")
        self.assertEqual(Employee.objects.filter(name__iexact="Vivek").exists(), True)

    def test_delete_record(self):
        self.__set_up()
        user = 'Yatendra'
        response = self.client.delete(f'/api/v1/employee/' + user)
        self.assertEqual(response.json()['status'], "true")
        self.assertEqual(response.json()['message'], "Record for name " + user + " deleted")
        self.assertEqual(Employee.objects.filter(name__iexact=user).exists(), False)
