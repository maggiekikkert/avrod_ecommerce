from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Session(models.Model):
    session_key = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)


class License(models.Model):
    license_key = models.CharField(max_length=32, primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, license_key):
        license = cls(license_key=license_key)
        return license


class Customer(models.Model):
    customer_id = models.CharField(max_length=18, unique=True, primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    @classmethod
    def create(cls, customer_id, user_id):
        customer = cls(customer_id=customer_id, user_id=user_id)
        return customer


class Subscription(models.Model):
    sub_id = models.CharField(max_length=18, unique=True, primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    license_key = models.ForeignKey(License, on_delete=models.CASCADE, null=True)
    renewal_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, sub_id, customer_id, license_key, renewal_date):
        subscription = cls(sub_id=sub_id, customer_id=customer_id, license_key=license_key, renewal_date=renewal_date)
        return subscription
