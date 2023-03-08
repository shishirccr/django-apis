from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    currency = models.CharField(max_length=100)
    salary = models.IntegerField()
    department = models.CharField(max_length=100)
    sub_department = models.CharField(max_length=100)
    on_contract = models.CharField(max_length=5, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-name']