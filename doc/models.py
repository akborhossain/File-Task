from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser, PermissionsMixin
#from django.contrib.postgres.fields import ArrayField

# Create your models here.

#class User(AbstractBaseUser):
#   class Role(models.TextChoices):
#       ADMIN= "ADMIN", 'Admin'
#       STAFF= "STAFF",'Staff'
#       USER= "USER",'User'




class DocFile(models.Model):
    title=models.CharField(max_length=50, blank=True, null=True)
    description=models.CharField(max_length=200, blank=True, null=True)
    #uploaded_files= models.FileField(upload_to="files/", blank=True, null=True)
    #if use multiple file then uncomment this and need postgres
    uploaded_files=models.FileField(upload_to="files/", blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_files', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_files', blank=True, null=True)
    updated_at=models.DateTimeField(auto_now=True, blank=True, null=True)
