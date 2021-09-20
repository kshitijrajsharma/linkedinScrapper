# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, blank=True)
    Linkedin_Email = models.EmailField(max_length=254)
    password = models.CharField(('password'), max_length=128)
    
    Phone=models.CharField(max_length=100, blank=True)
    Address = models.CharField(max_length=30, blank=True)
    City = models.CharField(max_length=30, blank=True)    
    State = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
def set_password(self, raw_password):
    import random
    algo = 'sha1'
    salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(algo, salt, raw_password)
    self.password = '%s$%s$%s' % (algo, salt, hsh)
class scrapperprofile(models.Model):
    Contact = models.TextField(null=True,blank=True)
    name= models.TextField(null=True,blank=True)
    location= models.TextField(null=True,blank=True)
    Education= models.TextField(null=True,blank=True)
    Skills = models.TextField(null=True,blank=True)
    Interest = models.TextField(null=True,blank=True)
    Description = models.TextField(null=True,blank=True)

    profilelink= models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    scrapped_status = models.BooleanField(default=False)


    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    