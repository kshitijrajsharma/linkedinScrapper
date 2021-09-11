# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
# Create your models here.

class scrapperprofile(models.Model):
    profilelink= models.URLField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    scrapped_status = models.BooleanField(default=False)
    
    Interest = models.TextField(null=True,blank=True)
    Accomplishments = models.TextField(null=True,blank=True)
    Skills = models.TextField(null=True,blank=True)
    Education= models.TextField(null=True,blank=True)
    Experience = models.TextField(null=True,blank=True)
    Contact = models.TextField(null=True,blank=True)
    Description = models.TextField(null=True,blank=True)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    