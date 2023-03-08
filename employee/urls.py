from django.urls import path
from . import views


urlpatterns = [
    path('create', views.EmployeeView.as_view({'post': 'add_new_record'})),
    path('<str:emp_name>', views.EmployeeView.as_view({'delete': 'delete_employee'})),
    path('', views.EmployeeView.as_view({'get': 'get_statistic_info'})),
]