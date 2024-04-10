# fileupload/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import pytz

class UploadedFile(models.Model):
    # file = models.FileField(upload_to='uploads/')
    # uploaded_at = models.DateTimeField(auto_now_add=True)

    file1 = models.FileField(upload_to='uploads/', null=True, blank=True)
    file2 = models.FileField(upload_to='uploads/', null=True, blank=True)
    # files = models.FileField(upload_to='uploads/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return self.file.name
        return f"{self.file1.name} / {self.file2.name}"
    
class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.username

class UploadData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    client = models.CharField(max_length=50,null=True, blank=True)
    agent = models.CharField(max_length=50,null=True, blank=True)
    custom_file = models.CharField(max_length=50,null=True, blank=True)
    dr_file = models.CharField(max_length=50,null=True, blank=True)
    excel_file = models.CharField(max_length=50,null=True, blank=True)


class UploadUserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    client = models.CharField(max_length=50,null=True, blank=True)
    agent = models.CharField(max_length=50,null=True, blank=True)
    custom_file = models.CharField(max_length=50,null=True, blank=True)
    dr_file = models.CharField(max_length=50,null=True, blank=True)
    excel_file = models.CharField(max_length=50,null=True, blank=True)


class SubmitUserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    booking_company = models.CharField(max_length=50, null=True, blank=True)
    shipping_company = models.CharField(max_length=50, null=True, blank=True)
    booking_no = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class SubmitUserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    booking_company = models.CharField(max_length=50, null=True, blank=True)
    shipping_company = models.CharField(max_length=50, null=True, blank=True)
    booking_no = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class PathInformation(models.Model):
    icm = models.CharField(max_length=50, null=True, blank=True)
    icm1 = models.CharField(max_length=50, null=True, blank=True)
    excel_download = models.CharField(max_length=100, null=True, blank=True)
    file = models.CharField(max_length=100000, null=True, blank=True)
    df1_json = models.CharField(max_length=100000, null=True, blank=True)
    excel_path = models.CharField(max_length=500, null=True, blank=True)

